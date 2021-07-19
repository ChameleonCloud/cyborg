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
import os
from stat import S_ISCHR

from cyborg.accelerator.drivers.peripheral.base import BasePeripheralDriver

# TODO: maybe this needs to support multiple slots?
CSI_DEVICE = "/dev/video0"
SOCKETS_TO_MOUNT = ["/tmp/argus_socket"]
LOG = logging.getLogger(__name__)

class JetsonCSIDriver(BasePeripheralDriver):
    def discover_peripherals(self):
        """Discover camera information.

        :return: List of Jetson Nano CSI devices
        """

        if not os.path.exists(CSI_DEVICE):
            LOG.error(f"Could not find expected camera device at {CSI_DEVICE}")
            return []

        if not S_ISCHR(os.stat(CSI_DEVICE).st_mode):
            LOG.error((
                f"Camera device at {CSI_DEVICE} was not a character special "
                "device file"))
            return []

        return [{
            "name": "jetson_csi",
            "vendor": "N/A",
            "model": "Generic CSI Camera", # get from vcgencmd vcos version (?)
            "traits": ["CUSTOM_CAMERA", "CUSTOM_CAMERA_JETSON_CSI"],
            "oci_runtime": {
                "mounts": [
                    {"destination": sock, "source": sock, "mode": "rw"}
                    for sock in SOCKETS_TO_MOUNT
                ],
                "linux": {
                    "devices": [
                        {"type": "c", "path": CSI_DEVICE},
                    ],
                }
            }
        }]
