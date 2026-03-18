# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from aim.api import resource as api_res
from aim import aim_manager
from aim.tests import base


class TestUsegModels(base.TestAimDBBase):
    """Tests for uSeg microsegmentation AIM resource models."""

    def setUp(self):
        super(TestUsegModels, self).setUp()
        self.mgr = aim_manager.AimManager()

    def test_create_endpoint_group_criteria(self):
        criteria = api_res.EndpointGroupCriteria(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1', match='any')
        self.mgr.create(self.ctx, criteria)

        retrieved = self.mgr.get(self.ctx, criteria)
        self.assertIsNotNone(retrieved)
        self.assertEqual('t1', retrieved.tenant_name)
        self.assertEqual('ap1', retrieved.app_profile_name)
        self.assertEqual('epg1', retrieved.epg_name)
        self.assertEqual('any', retrieved.match)

    def test_update_endpoint_group_criteria(self):
        criteria = api_res.EndpointGroupCriteria(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1', match='any')
        self.mgr.create(self.ctx, criteria)
        self.mgr.update(self.ctx, criteria, match='all')

        retrieved = self.mgr.get(self.ctx, criteria)
        self.assertEqual('all', retrieved.match)

    def test_delete_endpoint_group_criteria(self):
        criteria = api_res.EndpointGroupCriteria(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1')
        self.mgr.create(self.ctx, criteria)
        self.mgr.delete(self.ctx, criteria)

        retrieved = self.mgr.get(self.ctx, criteria)
        self.assertIsNone(retrieved)

    def test_create_endpoint_group_ip_attr(self):
        ip_attr = api_res.EndpointGroupIpAttr(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1', name='match1',
            ip='10.0.1.0/24')
        self.mgr.create(self.ctx, ip_attr)

        retrieved = self.mgr.get(self.ctx, ip_attr)
        self.assertIsNotNone(retrieved)
        self.assertEqual('10.0.1.0/24', retrieved.ip)
        self.assertFalse(retrieved.use_subnet)

    def test_create_endpoint_group_ip_attr_with_subnet(self):
        ip_attr = api_res.EndpointGroupIpAttr(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1', name='match1',
            ip='10.0.1.0/24', use_subnet=True)
        self.mgr.create(self.ctx, ip_attr)

        retrieved = self.mgr.get(self.ctx, ip_attr)
        self.assertTrue(retrieved.use_subnet)

    def test_update_endpoint_group_ip_attr(self):
        ip_attr = api_res.EndpointGroupIpAttr(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1', name='match1',
            ip='10.0.1.0/24')
        self.mgr.create(self.ctx, ip_attr)
        self.mgr.update(self.ctx, ip_attr, ip='10.0.2.0/24')

        retrieved = self.mgr.get(self.ctx, ip_attr)
        self.assertEqual('10.0.2.0/24', retrieved.ip)

    def test_delete_endpoint_group_ip_attr(self):
        ip_attr = api_res.EndpointGroupIpAttr(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1', name='match1', ip='10.0.1.0/24')
        self.mgr.create(self.ctx, ip_attr)
        self.mgr.delete(self.ctx, ip_attr)

        retrieved = self.mgr.get(self.ctx, ip_attr)
        self.assertIsNone(retrieved)

    def test_find_endpoint_group_ip_attrs(self):
        for i in range(3):
            self.mgr.create(self.ctx, api_res.EndpointGroupIpAttr(
                tenant_name='t1', app_profile_name='ap1',
                epg_name='epg1', name='match%d' % i,
                ip='10.0.%d.0/24' % i))

        found = self.mgr.find(
            self.ctx, api_res.EndpointGroupIpAttr,
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1')
        self.assertEqual(3, len(found))

    def test_create_endpoint_group_mac_attr(self):
        mac_attr = api_res.EndpointGroupMacAttr(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1', name='mac1',
            mac='00:11:22:33:44:55')
        self.mgr.create(self.ctx, mac_attr)

        retrieved = self.mgr.get(self.ctx, mac_attr)
        self.assertIsNotNone(retrieved)
        self.assertEqual('00:11:22:33:44:55', retrieved.mac)

    def test_delete_endpoint_group_mac_attr(self):
        mac_attr = api_res.EndpointGroupMacAttr(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1', name='mac1', mac='00:11:22:33:44:55')
        self.mgr.create(self.ctx, mac_attr)
        self.mgr.delete(self.ctx, mac_attr)

        retrieved = self.mgr.get(self.ctx, mac_attr)
        self.assertIsNone(retrieved)

    def test_create_endpoint_group_vm_attr(self):
        vm_attr = api_res.EndpointGroupVmAttr(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1', name='vm1',
            type='vm-name', operator='contains',
            value='web-server')
        self.mgr.create(self.ctx, vm_attr)

        retrieved = self.mgr.get(self.ctx, vm_attr)
        self.assertIsNotNone(retrieved)
        self.assertEqual('vm-name', retrieved.type)
        self.assertEqual('contains', retrieved.operator)
        self.assertEqual('web-server', retrieved.value)

    def test_update_endpoint_group_vm_attr(self):
        vm_attr = api_res.EndpointGroupVmAttr(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1', name='vm1',
            type='vm-name', operator='equals', value='old')
        self.mgr.create(self.ctx, vm_attr)
        self.mgr.update(self.ctx, vm_attr, value='new-value',
                        operator='startsWith')

        retrieved = self.mgr.get(self.ctx, vm_attr)
        self.assertEqual('new-value', retrieved.value)
        self.assertEqual('startsWith', retrieved.operator)

    def test_delete_endpoint_group_vm_attr(self):
        vm_attr = api_res.EndpointGroupVmAttr(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1', name='vm1',
            type='vm-name', operator='equals', value='test')
        self.mgr.create(self.ctx, vm_attr)
        self.mgr.delete(self.ctx, vm_attr)

        retrieved = self.mgr.get(self.ctx, vm_attr)
        self.assertIsNone(retrieved)

    def test_criteria_with_multiple_children(self):
        """Verify a criteria can have IP, MAC and VM attrs simultaneously."""
        criteria = api_res.EndpointGroupCriteria(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1', match='all')
        self.mgr.create(self.ctx, criteria)

        self.mgr.create(self.ctx, api_res.EndpointGroupIpAttr(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1', name='ip1', ip='10.0.0.0/8'))
        self.mgr.create(self.ctx, api_res.EndpointGroupMacAttr(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1', name='mac1', mac='AA:BB:CC:DD:EE:FF'))
        self.mgr.create(self.ctx, api_res.EndpointGroupVmAttr(
            tenant_name='t1', app_profile_name='ap1',
            epg_name='epg1', name='vm1',
            type='hv', operator='equals', value='host-1'))

        ip_attrs = self.mgr.find(
            self.ctx, api_res.EndpointGroupIpAttr, epg_name='epg1')
        mac_attrs = self.mgr.find(
            self.ctx, api_res.EndpointGroupMacAttr, epg_name='epg1')
        vm_attrs = self.mgr.find(
            self.ctx, api_res.EndpointGroupVmAttr, epg_name='epg1')

        self.assertEqual(1, len(ip_attrs))
        self.assertEqual(1, len(mac_attrs))
        self.assertEqual(1, len(vm_attrs))
