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
import logging
from pathlib import Path
from stat import S_ISCHR

from cyborg.accelerator.drivers.peripheral.base import BasePeripheralDriver

LOG = logging.getLogger(__name__)

class GenericUVCCameraDriver(BasePeripheralDriver):
    def discover_peripherals(self):
        """Discover camera information.

        :return: List of UVC camera devices.
        """
        found_devices = []

        for dev_path in Path("/dev").glob("video*"):
            if not S_ISCHR(dev_path.stat().st_mode):
                LOG.warning((
                    f"Camera device at {dev_path} was not a character special "
                    "device file"))
                continue
            found_devices.append(dev_path)

        if not found_devices:
            LOG.error(f"Could not find any camera devices in /dev/video*")
            return []

        return [{
            "name": "generic_uvc_camera",
            "vendor": "N/A",
            "model": "Generic UVC Camera",
            "traits": ["CUSTOM_CAMERA", "CUSTOM_CAMERA_GENERIC_UVC"],
            "oci_runtime": {
                "linux": {
                    "devices": [
                        {"type": "c", "path": str(device_path)}
                        for device_path in found_devices
                    ],
                }
            }
        }]
