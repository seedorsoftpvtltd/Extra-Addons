# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.account.tests.account_test_no_chart import TestAccountNoChartCommon
from odoo.exceptions import AccessError
from odoo.tests import Form, tagged


@tagged('post_install', '-at_install')
class TestwarehouseInvoice(TestAccountNoChartCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create a users
        group_warehouse_user = cls.env.ref('warehouse.group_warehouse_user')
        group_employee = cls.env.ref('base.group_user')

        cls.warehouse_user = cls.env['res.users'].with_context(
            no_reset_password=True
        ).create({
            'name': 'warehouse user',
            'login': 'warehouseUser',
            'email': 'pu@odoo.com',
            'groups_id': [(6, 0, [group_warehouse_user.id, group_employee.id])],
            'property_account_payable_id': cls.account_payable.id,
            'property_account_receivable_id': cls.account_receivable.id,
        })

        cls.vendor = cls.env['res.partner'].create({
            'name': 'Supplier',
            'email': 'supplier.serv@supercompany.com',
        })

        user_type_expense = cls.env.ref('account.data_account_type_expenses')
        cls.account_expense_product = cls.env['account.account'].create({
            'code': 'EXPENSE_PROD111',
            'name': 'Expense - Test Account',
            'user_type_id': user_type_expense.id,
        })
        # Create category
        cls.product_category = cls.env['product.category'].create({
            'name': 'Product Category with Expense account',
            'property_account_expense_categ_id': cls.account_expense_product.id
        })
        cls.product = cls.env['product.product'].create({
            'name': "Product",
            'standard_price': 200.0,
            'list_price': 180.0,
            'type': 'service',
        })

        cls.setUpAdditionalAccounts()
        cls.setUpAccountJournal()

    def test_create_warehouse_order(self):
        """Check a warehouse user can create a vendor bill from a Warehouse Booking but not post it"""
        warehouse_order_form = Form(self.env['warehouse.order'].with_user(self.warehouse_user))
        warehouse_order_form.partner_id = self.vendor
        with warehouse_order_form.order_line.new() as line:
            line.name = self.product.name
            line.product_id = self.product
            line.product_qty = 4
            line.price_unit = 5

        warehouse_order = warehouse_order_form.save()
        warehouse_order.button_confirm()

        action = warehouse_order.with_user(self.warehouse_user).action_view_invoice()
        invoice_form = Form(self.env['account.move'].with_user(self.warehouse_user).with_context(
            action['context']
        ))
        invoice = invoice_form.save()
        with self.assertRaises(AccessError):
            invoice.post()

    def test_read_warehouse_order(self):
        """ Check that a warehouse user can read all Warehouse Booking and 'in' invoices"""
        warehouse_user_2 = self.warehouse_user.copy({
            'name': 'warehouse user 2',
            'login': 'warehouseUser2',
            'email': 'pu2@odoo.com',
        })

        warehouse_order_form = Form(self.env['warehouse.order'].with_user(warehouse_user_2))
        warehouse_order_form.partner_id = self.vendor
        with warehouse_order_form.order_line.new() as line:
            line.name = self.product.name
            line.product_id = self.product
            line.product_qty = 4
            line.price_unit = 5

        warehouse_order_user2 = warehouse_order_form.save()
        action = warehouse_order_user2.with_user(warehouse_user_2).action_view_invoice()
        invoice_form = Form(self.env['account.move'].with_user(warehouse_user_2).with_context(action['context']))
        vendor_bill_user2 = invoice_form.save()

        # open warehouse_order_user2 and vendor_bill_user2 with `self.warehouse_user`
        warehouse_order_user1 = Form(warehouse_order_user2.with_user(self.warehouse_user))
        warehouse_order_user1 = warehouse_order_user1.save()
        vendor_bill_user1 = Form(vendor_bill_user2.with_user(self.warehouse_user))
        vendor_bill_user1 = vendor_bill_user1.save()

    def test_read_warehouse_order_2(self):
        """ Check that a 2 warehouse users with open the vendor bill the same
        way even with a 'own documents only' record rule. """

        # edit the account.move record rule for warehouse user in order to ensure
        # a user can only see his own invoices
        rule = self.env.ref('warehouse.warehouse_user_account_move_rule')
        rule.domain_force = "['&', ('type', 'in', ('in_invoice', 'in_refund', 'in_receipt')), ('invoice_user_id', '=', user.id)]"

        # create a warehouse and make a vendor bill from it as warehouse user 2
        warehouse_user_2 = self.warehouse_user.copy({
            'name': 'warehouse user 2',
            'login': 'warehouseUser2',
            'email': 'pu2@odoo.com',
        })

        warehouse_order_form = Form(self.env['warehouse.order'].with_user(warehouse_user_2))
        warehouse_order_form.partner_id = self.vendor
        with warehouse_order_form.order_line.new() as line:
            line.name = self.product.name
            line.product_id = self.product
            line.product_qty = 4
            line.price_unit = 5

        warehouse_order_user2 = warehouse_order_form.save()
        action = warehouse_order_user2.with_user(warehouse_user_2).action_view_invoice()
        invoice_form = Form(self.env['account.move'].with_user(warehouse_user_2).with_context(action['context']))
        vendor_bill_user2 = invoice_form.save()

        # check user 1 cannot read the invoice
        with self.assertRaises(AccessError):
            Form(vendor_bill_user2.with_user(self.warehouse_user))

        # Check that calling 'action_view_invoice' return the same action despite the record rule
        action_user_1 = warehouse_order_user2.with_user(self.warehouse_user).action_view_invoice()
        warehouse_order_user2.invalidate_cache()
        action_user_2 = warehouse_order_user2.with_user(warehouse_user_2).action_view_invoice()
        self.assertEqual(action_user_1, action_user_2)
