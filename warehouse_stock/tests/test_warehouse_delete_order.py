# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import UserError
from .common import Testwarehouse


class TestDeleteOrder(Testwarehouse):

    def test_00_delete_order(self):
        ''' Testcase for deleting warehouse order with warehouse user group'''

        # In order to test delete process on warehouse order,tried to delete a confirmed order and check Error Message.
        warehouse_order_1 = self.env.ref('warehouse.warehouse_order_1').with_user(self.res_users_warehouse_user)
        with self.assertRaises(UserError):
            warehouse_order_1.unlink()

        # Delete 'cancelled' warehouse order with user group
        warehouse_order_7 = self.env.ref('warehouse.warehouse_order_7').with_user(self.res_users_warehouse_user)
        warehouse_order_7.button_cancel()
        self.assertEqual(warehouse_order_7.state, 'cancel', 'PO is cancelled!')
        warehouse_order_7.unlink()

        # Delete 'draft' warehouse order with user group
        warehouse_order_5 = self.env.ref('warehouse.warehouse_order_5').with_user(self.res_users_warehouse_user)
        self.assertEqual(warehouse_order_5.state, 'draft', 'PO in draft state!')
        warehouse_order_5.button_cancel()
        self.assertEqual(warehouse_order_5.state, 'cancel', 'PO is cancelled!')
        warehouse_order_5.unlink()
