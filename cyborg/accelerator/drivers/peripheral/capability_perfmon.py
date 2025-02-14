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

from cyborg.accelerator.drivers.peripheral.base import BasePeripheralDriver


class CapabilityPerfmonDriver(BasePeripheralDriver):
    def discover_peripherals(self):
        return [{
            "name": "cap_perfmon",
            "vendor": "N/A",
            "model": "PERFMON capability",
            "traits": ["CUSTOM_CAPABILITY", "CUSTOM_PERFMON"],
            "oci_runtime": {
                "linux": {
                    "capabilities": {
                        "permitted": ["CAP_PERFMON"],
                        "effective": ["CAP_PERFMON"],
                        "inherited": ["CAP_PERFMON"],
                        "bounding": ["CAP_PERFMON"],
                    },
                }
            }
        }]
