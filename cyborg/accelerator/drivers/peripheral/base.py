# Copyright 2021 University of Chicago
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import hashlib

from oslo_config import cfg
from oslo_serialization import jsonutils
from oslo_utils import dictutils

from cyborg.common import constants
from cyborg.objects.driver_objects import driver_attach_handle
from cyborg.objects.driver_objects import driver_attribute
from cyborg.objects.driver_objects import driver_controlpath_id
from cyborg.objects.driver_objects import driver_deployable
from cyborg.objects.driver_objects import driver_device

CONF = cfg.CONF

class BasePeripheralDriver(object):
    def discover(self):
        """Discover peripherals.

        Actual discovery of peripherals is delegated to
        ``discover_peripherals``, which is expected to return a list of
        peripheral objects that can be exposed as DriverDevices.
        """
        peripherals = self.discover_peripherals()
        if not peripherals:
            return []

        device_list = []
        for peripheral in peripherals:
            driver_device_obj = driver_device.DriverDevice()
            driver_device_obj.vendor = peripheral.get("vendor")
            driver_device_obj.model = peripheral.get("model")
            driver_device_obj.std_board_info = jsonutils.dumps({})
            driver_device_obj.vendor_board_info = ""
            driver_device_obj.type = constants.DEVICE_PERIPHERAL
            driver_device_obj.stub = False
            driver_device_obj.controlpath_id = (
                _generate_controlpath_id(peripheral))
            driver_device_obj.deployable_list = _generate_dep_list(peripheral)
            device_list.append(driver_device_obj)

        return device_list

    def discover_peripherals(self):
        """Provide information about attache peripherals.

        This should return a list of peripheral dicts, which have the following
        keys:
          - ``name``: the name of the peripheral, which is used internally to
            identity the peripheral, e.g., "go_pro_camera" or "sdr".
          - ``vendor``: a human-readable string describing the periph. vendor
          - ``model``: a human-readable string describing the periph. model
          - ``driver_name``: a human-readable string describing the periph.
            driver name. Defaults to vendor.
          - ``traits``: a list of trait names. In general this is how
            peripherals are differentiated; device profiles are used to target
            a specific peripheral by targeting one or more traits. A trait can
            be general like "CUSTOM_CAMERA", describing any camera, or can be
            specific like "CUSTOM_CAMERA_GO_PRO". All traits should be prefixed
            with "CUSTOM_" prefix to differentiate them from standardized
            traits maintained in os_traits.
          - ``resource_class``: an optional resource class. This defaults to
            CUSTOM_PERIPHERAL, and should only be overridden if "peripheral"
            doesn't seem to adequately describe the resource.
          - ``oci_runtime``: a partial OCI runtime configuration, following the
            `specification <https://github.com/opencontainers/runtime-spec/blob/master/config.md>`_.
            This is used to aid in attaching peripherals to containers launched
            via Zun.
        """
        return []


def _generate_controlpath_id(peripheral):
    driver_cpid = driver_controlpath_id.DriverControlPathID()
    # It is almost certain that not all peripherals will be PCI.
    # This controlpath object isn't really used yet though.
    # NOTE(jason): The most important part is that this is at least unique
    # across types of devices; set() is used for comparisons in the conductor,
    # which will drop duplicates. So, two peripherals exposed from a single
    # host must have different control path IDs.
    driver_cpid.cpid_type = "PCI"
    pci_info = peripheral.get("pci")
    if not pci_info:
        # Create random values to prevent collisions; as this is not a real
        # PCI device (and won't be used as such) these values will not matter.
        desc = (
            hashlib.sha256(peripheral.get("name").encode("utf-8")).hexdigest())
        pci_info = {
            "domain": "0000",
            "bus": desc[:2],
            "device": desc[2:4],
            "function": desc[4],
        }
    driver_cpid.cpid_info = jsonutils.dumps(pci_info)
    return driver_cpid


def _generate_dep_list(peripheral):
    dep_list = []
    driver_dep = driver_deployable.DriverDeployable()
    driver_dep.name = ".".join([CONF.host, peripheral.get("name")])
    driver_dep.driver_name = peripheral.get(
        "driver_name",
        peripheral.get("vendor", "unknown")
    )
    driver_dep.num_accelerators = 1
    driver_dep.attribute_list = _generate_dep_attr_list(peripheral)
    driver_dep.attach_handle_list = [_generate_attach_handle(peripheral)]
    dep_list.append(driver_dep)
    return dep_list


def _generate_dep_attr_list(peripheral):
    dep_attrs = []

    rc_attr = driver_attribute.DriverAttribute()
    rc_attr.key = "rc"
    rc_attr.value = peripheral.get("resource_class",
        constants.RESOURCES["PERIPHERAL"])
    dep_attrs.append(rc_attr)

    for i, trait in enumerate(peripheral.get("traits", [])):
        trait_attr = driver_attribute.DriverAttribute()
        trait_attr.key = f"trait{i}"
        trait_attr.value = trait
        dep_attrs.append(trait_attr)

    return dep_attrs


def _generate_attach_handle(peripheral):
    driver_ah = driver_attach_handle.DriverAttachHandle()
    driver_ah.attach_type = constants.AH_TYPE_OCI_RUNTIME
    driver_ah.in_use = False
    attach_info = _to_dot_notation(peripheral.get("oci_runtime", {}))
    driver_ah.attach_info = jsonutils.dumps(attach_info)
    return driver_ah


def _to_dot_notation(in_dict):
    out_dict = {}
    for key, value in in_dict.items():
        if isinstance(value, list):
            value = dict(enumerate(value))
        if isinstance(value, dict):
            out_dict.update({
                f"{key}.{_subkey}": _subval
                for _subkey, _subval in _to_dot_notation(value).items()
            })
        else:
            out_dict[key] = value
    return out_dict
