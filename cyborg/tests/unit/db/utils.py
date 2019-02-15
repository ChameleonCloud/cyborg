# Copyright 2017 Huawei Technologies Co.,LTD.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Cyborg db test utilities."""


def get_test_accelerator(**kw):
    return {
        'name': kw.get('name', 'name'),
        'description': kw.get('description', 'description'),
        'device_type': kw.get('device_type', 'device_type'),
        'acc_type': kw.get('acc_type', 'acc_type'),
        'acc_capability': kw.get('acc_capability', 'acc_capability'),
        'vendor_id': kw.get('vendor_id', 'vendor_id'),
        'product_id': kw.get('product_id', 'product_id'),
        'remotable': kw.get('remotable', 1),
        'project_id': kw.get('project_id', 'b492a6fb12964ae3bd291ce585107d48'),
        'user_id': kw.get('user_id', '7009409e21614d1db1ef7a8c5ee101d8'),
    }


def get_test_deployable(**kw):
    return {
        'uuid': kw.get('uuid', '10efe63d-dfea-4a37-ad94-4116fba5098'),
        'deleted': False,
        'name': kw.get('name', 'name'),
        'parent_uuid': kw.get('parent_uuid', None),
        'address': kw.get('address', '00:7f:0b.2'),
        'host': kw.get('host', 'host'),
        'board': kw.get('board', 'KU115'),
        'vendor': kw.get('vendor', 'Xilinx'),
        'version': kw.get('version', '1.0'),
        'type': kw.get('type', '1.0'),
        'interface_type': 'pci',
        'assignable': True,
        'instance_uuid': None,
        'availability': 'Available',
        'accelerator_id': kw.get('accelerator_id', 1),
    }


def get_test_extarq(**kwargs):
    return {
        'uuid': kwargs.get('uuid', '10efe63d-dfea-4a37-ad94-4116fba5098'),
        'id': kwargs.get('id', 1),
        'state': kwargs.get('state', 'bound'),
        'device_profile_id': kwargs.get('id', 1),
        'hostname': kwargs.get('hostname', 'testnode1'),
        'device_rp_uuid': kwargs.get('device_rp_uuid',
                                     'f2b96c5f-242a-41a0-a736-b6e1fada071b'),
        'device_instance_uuid':
            kwargs.get('device_rp_uuid',
                       '6219e0fb-2935-4db2-a3c7-86a2ac3ac84e'),
        'attach_handle_id': kwargs.get('id', 1),
        'created_at': kwargs.get('created_at', None),
        'updated_at': kwargs.get('updated_at', None)
    }


def get_test_arq(**kwargs):
    return {
        'uuid': kwargs.get('uuid', '10efe63d-dfea-4a37-ad94-4116fba5098'),
        'id': kwargs.get('id', 1),
        'state': kwargs.get('state', 'Initial'),
        'device_profile': kwargs.get('device_profile', None),
        'hostname': kwargs.get('hostname', 'testnode1'),
        'device_rp_uuid': kwargs.get('device_rp_uuid',
                                     'f2b96c5f-242a-41a0-a736-b6e1fada071b'),
        'device_instance_uuid':
            kwargs.get('device_rp_uuid',
                       '6219e0fb-2935-4db2-a3c7-86a2ac3ac84e'),
        'attach_handle': kwargs.get('attach_handle', None),
        'created_at': kwargs.get('created_at', None),
        'updated_at': kwargs.get('updated_at', None),
        'substate': kwargs.get('substate', 'Initial'),
    }
