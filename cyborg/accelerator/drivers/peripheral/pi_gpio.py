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

GPIO_DEVICE = "/dev/gpiomem"
LOG = logging.getLogger(__name__)

class PiGPIODriver(BasePeripheralDriver):
    def discover_peripherals(self):
        """Discover camera information.

        :return: List of Raspberry Pi camera devices
        """

        if os.path.exists(GPIO_DEVICE):
            LOG.error(f"Could not find expected GPIO device at {GPIO_DEVICE}")
            return []

        if not S_ISCHR(os.stat(GPIO_DEVICE).st_mode):
            LOG.error((
                f"GPIO device at {GPIO_DEVICE} was not a character special "
                "device file"
            ))
            return []

        return [{
            "name": "pi_gpio",
            "vendor": "Raspberry Pi",
            "model": "", # ??
            "traits": ["CUSTOM_GPIO", "CUSTOM_GPIO_RASPBERRY_PI"],
            "oci_runtime": {
                "linux": {
                    "devices": [
                        {"type": "c", "path": GPIO_DEVICE},
                    ],
                }
            }
        }]
