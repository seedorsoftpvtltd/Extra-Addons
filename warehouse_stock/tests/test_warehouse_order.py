# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons.account.tests.account_test_classes import AccountingTestCase
from odoo.tests import Form, tagged


@tagged('post_install', '-at_install')
class TestwarehouseOrder(AccountingTestCase):

    def setUp(self):
        super(TestwarehouseOrder, self).setUp()
        # Useful models
        self.warehouseOrder = self.env['warehouse.order']
        self.warehouseOrderLine = self.env['warehouse.order.line']
        self.partner_id = self.env.ref('base.res_partner_1')
        self.product_id_1 = self.env.ref('product.product_product_8')
        self.product_id_2 = self.env.ref('product.product_product_11')

        (self.product_id_1 | self.product_id_2).write({'warehouse_method': 'warehouse'})
        self.po_vals = {
            'partner_id': self.partner_id.id,
            'order_line': [
                (0, 0, {
                    'name': self.product_id_1.name,
                    'product_id': self.product_id_1.id,
                    'product_qty': 5.0,
                    'product_uom': self.product_id_1.uom_po_id.id,
                    'price_unit': 500.0,
                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                }),
                (0, 0, {
                    'name': self.product_id_2.name,
                    'product_id': self.product_id_2.id,
                    'product_qty': 5.0,
                    'product_uom': self.product_id_2.uom_po_id.id,
                    'price_unit': 250.0,
                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                })],
        }

    def test_00_warehouse_order_flow(self):
        # Ensure product_id_2 doesn't have res_partner_1 as supplier
        if self.partner_id in self.product_id_2.seller_ids.mapped('name'):
            id_to_remove = self.product_id_2.seller_ids.filtered(lambda r: r.name == self.partner_id).ids[0] if self.product_id_2.seller_ids.filtered(lambda r: r.name == self.partner_id) else False
            if id_to_remove:
                self.product_id_2.write({
                    'seller_ids': [(2, id_to_remove, False)],
                })
        self.assertFalse(self.product_id_2.seller_ids.filtered(lambda r: r.name == self.partner_id), 'warehouse: the partner should not be in the list of the product suppliers')

        self.po = self.warehouseOrder.create(self.po_vals)
        self.assertTrue(self.po, 'warehouse: no warehouse order created')
        self.assertEqual(self.po.invoice_status, 'no', 'warehouse: PO invoice_status should be "Not warehoused"')
        self.assertEqual(self.po.order_line.mapped('qty_received'), [0.0, 0.0], 'warehouse: no product should be received"')
        self.assertEqual(self.po.order_line.mapped('qty_invoiced'), [0.0, 0.0], 'warehouse: no product should be invoiced"')

        self.po.button_confirm()
        self.assertEqual(self.po.state, 'warehouse', 'warehouse: PO state should be "warehouse"')
        self.assertEqual(self.po.invoice_status, 'to invoice', 'warehouse: PO invoice_status should be "Waiting Invoices"')

        self.assertTrue(self.product_id_2.seller_ids.filtered(lambda r: r.name == self.partner_id), 'warehouse: the partner should be in the list of the product suppliers')

        seller = self.product_id_2._select_seller(partner_id=self.partner_id, quantity=2.0, date=self.po.date_planned, uom_id=self.product_id_2.uom_po_id)
        price_unit = seller.price if seller else 0.0
        if price_unit and seller and self.po.currency_id and seller.currency_id != self.po.currency_id:
            price_unit = seller.currency_id._convert(price_unit, self.po.currency_id, self.po.company_id, self.po.date_order)
        self.assertEqual(price_unit, 250.0, 'warehouse: the price of the product for the supplier should be 250.0.')

        self.assertEqual(self.po.picking_count, 1, 'warehouse: one picking should be created"')
        self.picking = self.po.picking_ids[0]
        self.picking.move_line_ids.write({'qty_done': 5.0})
        self.picking.button_validate()
        self.assertEqual(self.po.order_line.mapped('qty_received'), [5.0, 5.0], 'warehouse: all products should be received"')

        move_form = Form(self.env['account.move'].with_context(default_type='in_invoice'))
        move_form.partner_id = self.partner_id
        move_form.warehouse_id = self.po
        self.invoice = move_form.save()

        self.assertEqual(self.po.order_line.mapped('qty_invoiced'), [5.0, 5.0], 'warehouse: all products should be invoiced"')

    def test_02_po_return(self):
        """
        Test a PO with a product on Incoming shipment. Validate the PO, then do a return
        of the picking with Refund.
        """
        # Draft warehouse order created
        self.po = self.env['warehouse.order'].create(self.po_vals)
        self.assertTrue(self.po, 'warehouse: no warehouse order created')
        self.assertEqual(self.po.order_line.mapped('qty_received'), [0.0, 0.0], 'warehouse: no product should be received"')
        self.assertEqual(self.po.order_line.mapped('qty_invoiced'), [0.0, 0.0], 'warehouse: no product should be invoiced"')

        self.po.button_confirm()
        self.assertEqual(self.po.state, 'warehouse', 'warehouse: PO state should be "warehouse"')
        self.assertEqual(self.po.invoice_status, 'to invoice', 'warehouse: PO invoice_status should be "Waiting Invoices"')

        # Confirm the warehouse order
        self.po.button_confirm()
        self.assertEqual(self.po.state, 'warehouse', 'warehouse: PO state should be "warehouse')
        self.assertEqual(self.po.picking_count, 1, 'warehouse: one picking should be created"')
        self.picking = self.po.picking_ids[0]
        self.picking.move_line_ids.write({'qty_done': 5.0})
        self.picking.button_validate()
        self.assertEqual(self.po.order_line.mapped('qty_received'), [5.0, 5.0], 'warehouse: all products should be received"')

        #After Receiving all products create vendor bill.
        move_form = Form(self.env['account.move'].with_context(default_type='in_invoice'))
        move_form.partner_id = self.partner_id
        move_form.warehouse_id = self.po
        self.invoice = move_form.save()
        self.invoice.post()

        self.assertEqual(self.po.order_line.mapped('qty_invoiced'), [5.0, 5.0], 'warehouse: all products should be invoiced"')

        # Check quantity received
        received_qty = sum(pol.qty_received for pol in self.po.order_line)
        self.assertEqual(received_qty, 10.0, 'warehouse: Received quantity should be 10.0 instead of %s after validating incoming shipment' % received_qty)

        # Create return picking
        pick = self.po.picking_ids
        stock_return_picking_form = Form(self.env['stock.return.picking']
            .with_context(active_ids=pick.ids, active_id=pick.ids[0],
            active_model='stock.picking'))
        return_wiz = stock_return_picking_form.save()
        return_wiz.product_return_moves.write({'quantity': 2.0, 'to_refund': True})  # Return only 2
        res = return_wiz.create_returns()
        return_pick = self.env['stock.picking'].browse(res['res_id'])

        # Validate picking
        return_pick.move_line_ids.write({'qty_done': 2})
        
        return_pick.button_validate()

        # Check Received quantity
        self.assertEqual(self.po.order_line[0].qty_received, 3.0, 'warehouse: delivered quantity should be 3.0 instead of "%s" after picking return' % self.po.order_line[0].qty_received)
        #Create vendor bill for refund qty
        move_form = Form(self.env['account.move'].with_context(default_type='in_refund'))
        move_form.partner_id = self.partner_id
        move_form.warehouse_id = self.po
        self.invoice = move_form.save()
        move_form = Form(self.invoice)
        with move_form.invoice_line_ids.edit(0) as line_form:
            line_form.quantity = 2.0
        with move_form.invoice_line_ids.edit(1) as line_form:
            line_form.quantity = 2.0
        self.invoice = move_form.save()
        self.invoice.post()

        self.assertEqual(self.po.order_line.mapped('qty_invoiced'), [3.0, 3.0], 'warehouse: Billed quantity should be 3.0')

    def test_03_po_return_and_modify(self):
        """Change the picking code of the delivery to internal. Make a PO for 10 units, go to the
        picking and return 5, edit the PO line to 15 units.
        The purpose of the test is to check the consistencies across the received quantities and the
        procurement quantities.
        """
        # Change the code of the picking type delivery
        self.env['stock.picking.type'].search([('code', '=', 'outgoing')]).write({'code': 'internal'})

        # Sell and deliver 10 units
        item1 = self.product_id_1
        uom_unit = self.env.ref('uom.product_uom_unit')
        po1 = self.env['warehouse.order'].create({
            'partner_id': self.partner_id.id,
            'order_line': [
                (0, 0, {
                    'name': item1.name,
                    'product_id': item1.id,
                    'product_qty': 10,
                    'product_uom': uom_unit.id,
                    'price_unit': 123.0,
                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                }),
            ],
        })
        po1.button_confirm()

        picking = po1.picking_ids
        wiz_act = picking.button_validate()
        wiz = self.env[wiz_act['res_model']].browse(wiz_act['res_id'])
        wiz.process()

        # Return 5 units
        stock_return_picking_form = Form(self.env['stock.return.picking'].with_context(
            active_ids=picking.ids,
            active_id=picking.ids[0],
            active_model='stock.picking'
        ))
        return_wiz = stock_return_picking_form.save()
        for return_move in return_wiz.product_return_moves:
            return_move.write({
                'quantity': 5,
                'to_refund': True
            })
        res = return_wiz.create_returns()
        return_pick = self.env['stock.picking'].browse(res['res_id'])
        wiz_act = return_pick.button_validate()
        wiz = self.env[wiz_act['res_model']].browse(wiz_act['res_id'])
        wiz.process()

        self.assertEqual(po1.order_line.qty_received, 5)

        # Deliver 15 instead of 10.
        po1.write({
            'order_line': [
                (1, po1.order_line[0].id, {'product_qty': 15}),
            ]
        })

        # A new move of 10 unit (15 - 5 units)
        self.assertEqual(po1.order_line.qty_received, 5)
        self.assertEqual(po1.picking_ids[-1].move_lines.product_qty, 10)

    def test_04_multi_company(self):
        company_a = self.env.user.company_id
        company_b = self.env['res.company'].create({
            "name": "Test Company",
            "currency_id": self.env['res.currency'].with_context(active_test=False).search([
                ('id', '!=', company_a.currency_id.id),
            ], limit=1).id
        })
        self.env.user.write({
            'company_id': company_b.id,
            'company_ids': [(4, company_b.id), (4, company_a.id)],
        })
        po = self.warehouseOrder.create(dict(company_id=company_a.id, partner_id=self.partner_id.id))

        self.assertEqual(po.company_id, company_a)
        self.assertEqual(po.picking_type_id.warehouse_id.company_id, company_a)
        self.assertEqual(po.currency_id, po.company_id.currency_id)
