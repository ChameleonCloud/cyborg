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
from oslo_concurrency import processutils

from cyborg.accelerator.drivers.peripheral.base import BasePeripheralDriver
import cyborg.privsep


LOG = logging.getLogger(__name__)
USERLAND_DIR = "/opt/vc"

class PiCameraDriver(BasePeripheralDriver):
    def discover_peripherals(self):
        """Discover camera information.

        :return: List of Raspberry Pi camera devices
        """

        try:
            stdout, _ = _call_vcgencmd(["get_camera"])
            stdout_lines = stdout.split("\n")
            output = stdout_lines[0].split()
            if not ("supported=1" in output and "detected=1" in output):
                LOG.info((
                    "Software support for RPi camera found, but camera module "
                    "is not connected or is disabled in BIOS."))
                return []
        except processutils.ProcessExecutionError as exc:
            LOG.error(f"Failed to get camera status: {exc.cmd} failed with {exc.exit_code}")
            LOG.debug(exc.stderr.split("\n"))
            return []

        return [{
            "name": "pi_camera",
            "vendor": "Raspberry Pi",
            "model": "", # get from vcgencmd vcos version (?)
            "traits": ["CUSTOM_CAMERA", "CUSTOM_CAMERA_RASPBERRY_PI"],
            "oci_runtime": {
                "process": {
                    "env": [
                        f"LD_LIBRARY_PATH={USERLAND_DIR}/lib",
                    ],
                },
                "mounts": [
                    {"destination": USERLAND_DIR, "source": USERLAND_DIR, "mode": "ro"}
                ],
                "linux": {
                    "devices": [
                        {"type": "c", "path": "/dev/vchiq"},
                        {"type": "c", "path": "/dev/vcsm"},
                    ],
                }
            }
        }]


@cyborg.privsep.sys_admin_pctxt.entrypoint
def _call_vcgencmd(cmd_args):
    cmd = [f"{USERLAND_DIR}/bin/vcgencmd"]
    cmd.extend(cmd_args)
    return processutils.execute(*cmd, env_variables={
        "LD_LIBRARY_PATH": f"{USERLAND_DIR}/lib",
    })
