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

SERIAL_DEVICE = "/dev/ttyACM0"
LOG = logging.getLogger(__name__)


class PiSerialDriver(BasePeripheralDriver):
    def discover_peripherals(self):
        """Discover serial dev information.

        :return: List of Raspberry Pi serial devices
        """

        if os.path.exists(SERIAL_DEVICE):
            LOG.error(f"Could not find expected Serial device at {SERIAL_DEVICE}")
            return []

        if not S_ISCHR(os.stat(SERIAL_DEVICE).st_mode):
            LOG.error(
                (
                    f"Serial device at {SERIAL_DEVICE} was not a character special "
                    "device file"
                )
            )
            return []

        return [
            {
                "name": "pi_serial",
                "vendor": "Raspberry Pi",
                "model": "",  # ??
                "traits": ["CUSTOM_SERIAL", "CUSTOM_SERIAL_RASPBERRY_PI"],
                "oci_runtime": {
                    "linux": {
                        "devices": [
                            {"type": "c", "path": SERIAL_DEVICE},
                        ],
                    }
                },
            }
        ]
