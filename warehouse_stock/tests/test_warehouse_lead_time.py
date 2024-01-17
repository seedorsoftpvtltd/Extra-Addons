# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import fields
from .common import Testwarehouse


class TestwarehouseLeadTime(Testwarehouse):

    def test_00_product_company_level_delays(self):
        """ To check dates, set product's Delivery Lead Time
            and company's warehouse Lead Time."""

        company = self.env.ref('base.main_company')

        # Update company with warehouse Lead Time
        company.write({'po_lead': 3.00})

        # Make procurement request from product_1's form view, create procurement and check it's state
        date_planned = fields.Datetime.to_string(fields.datetime.now() + timedelta(days=10))
        self._create_make_procurement(self.product_1, 15.00, date_planned=date_planned)
        warehouse = self.env['warehouse.order.line'].search([('product_id', '=', self.product_1.id)], limit=1).order_id
        

        # Confirm warehouse order
        warehouse.button_confirm()

        # Check order date of warehouse order
        order_date = fields.Datetime.from_string(date_planned) - timedelta(days=company.po_lead) - timedelta(days=self.product_1.seller_ids.delay)
        self.assertEqual(warehouse.date_order, order_date, 'Order date should be equal to: Date of the procurement order - warehouse Lead Time - Delivery Lead Time.')

        # Check scheduled date of warehouse order
        schedule_date = order_date + timedelta(days=self.product_1.seller_ids.delay)
        self.assertEqual(warehouse.order_line.date_planned, schedule_date, 'Schedule date should be equal to: Order date of warehouse order + Delivery Lead Time.')

        # check the picking created or not
        self.assertTrue(warehouse.picking_ids, "Picking should be created.")

        # Check scheduled date of In Type shipment
        self.assertEqual(warehouse.picking_ids.scheduled_date, schedule_date, 'Schedule date of In type shipment should be equal to: schedule date of warehouse order.')

    def test_01_product_level_delay(self):
        """ To check schedule dates of multiple warehouse order line of the same warehouse order,
            we create two procurements for the two different product with same vendor
            and different Delivery Lead Time."""

        # Make procurement request from product_1's form view, create procurement and check it's state
        date_planned1 = fields.Datetime.to_string(fields.datetime.now() + timedelta(days=10))
        self._create_make_procurement(self.product_1, 10.00, date_planned=date_planned1)
        warehouse1 = self.env['warehouse.order.line'].search([('product_id', '=', self.product_1.id)], limit=1).order_id

        # Make procurement request from product_2's form view, create procurement and check it's state
        date_planned2 = fields.Datetime.to_string(fields.datetime.now() + timedelta(days=10))
        self._create_make_procurement(self.product_2, 5.00, date_planned=date_planned2)
        warehouse2 = self.env['warehouse.order.line'].search([('product_id', '=', self.product_2.id)], limit=1).order_id

        # Check warehouse order is same or not
        self.assertEqual(warehouse1, warehouse2, 'warehouse orders should be same for the two different product with same vendor.')

        # Confirm warehouse order
        warehouse1.button_confirm()

        # Check order date of warehouse order
        order_line_pro_1 = warehouse2.order_line.filtered(lambda r: r.product_id == self.product_1)
        order_line_pro_2 = warehouse2.order_line.filtered(lambda r: r.product_id == self.product_2)
        order_date = fields.Datetime.from_string(date_planned1) - timedelta(days=self.product_1.seller_ids.delay)
        self.assertEqual(warehouse2.date_order, order_date, 'Order date should be equal to: Date of the procurement order - Delivery Lead Time.')

        # Check scheduled date of warehouse order line for product_1
        schedule_date_1 = order_date + timedelta(days=self.product_1.seller_ids.delay)
        self.assertEqual(order_line_pro_1.date_planned, schedule_date_1, 'Schedule date of warehouse order line for product_1 should be equal to: Order date of warehouse order + Delivery Lead Time of product_1.')

        # Check scheduled date of warehouse order line for product_2
        schedule_date_2 = order_date + timedelta(days=self.product_2.seller_ids.delay)
        self.assertEqual(order_line_pro_2.date_planned, schedule_date_2, 'Schedule date of warehouse order line for product_2 should be equal to: Order date of warehouse order + Delivery Lead Time of product_2.')

        # Check scheduled date of warehouse order
        po_schedule_date = min(schedule_date_1, schedule_date_2)
        self.assertEqual(warehouse2.order_line[1].date_planned, po_schedule_date, 'Schedule date of warehouse order should be minimum of schedule dates of warehouse order lines.')

        # Check the picking created or not
        self.assertTrue(warehouse2.picking_ids, "Picking should be created.")

        # Check scheduled date of In Type shipment
        self.assertEqual(warehouse2.picking_ids.scheduled_date, po_schedule_date, 'Schedule date of In type shipment should be same as schedule date of warehouse order.')

    def test_02_product_route_level_delays(self):
        """ In order to check dates, set product's Delivery Lead Time
            and warehouse route's delay."""

        # Update warehouse_1 with Incoming Shipments 3 steps
        self.warehouse_1.write({'reception_steps': 'three_steps'})

        # Set delay on push rule
        for push_rule in self.warehouse_1.reception_route_id.rule_ids:
            push_rule.write({'delay': 2})

        rule_delay = sum(self.warehouse_1.reception_route_id.rule_ids.mapped('delay'))

        date_planned = fields.Datetime.to_string(fields.datetime.now() + timedelta(days=10))
        # Create procurement order of product_1
        self.env['procurement.group'].run([self.env['procurement.group'].Procurement(
            self.product_1, 5.000, self.uom_unit, self.warehouse_1.lot_stock_id, 'Test scheduler for Booking', '/', self.env.company,
            {
                'warehouse_id': self.warehouse_1,
                'date_planned': date_planned,  # 10 days added to current date of procurement to get future schedule date and order date of warehouse order.
                'rule_id': self.warehouse_1.buy_pull_id,
                'group_id': False,
                'route_ids': [],
            }
        )])

        # Confirm warehouse order

        warehouse = self.env['warehouse.order.line'].search([('product_id', '=', self.product_1.id)], limit=1).order_id
        warehouse.button_confirm()

        # Check order date of warehouse order
        order_date = fields.Datetime.from_string(date_planned) - timedelta(days=self.product_1.seller_ids.delay + rule_delay)
        self.assertEqual(warehouse.date_order, order_date, 'Order date should be equal to: Date of the procurement order - Delivery Lead Time(supplier and pull rules).')

        # Check scheduled date of warehouse order
        schedule_date = order_date + timedelta(days=self.product_1.seller_ids.delay + rule_delay)
        self.assertEqual(date_planned, str(schedule_date), 'Schedule date should be equal to: Order date of warehouse order + Delivery Lead Time(supplier and pull rules).')

        # Check the picking crated or not
        self.assertTrue(warehouse.picking_ids, "Picking should be created.")

        # Check scheduled date of Internal Type shipment
        incoming_shipment1 = self.env['stock.picking'].search([('move_lines.product_id', 'in', (self.product_1.id, self.product_2.id)), ('picking_type_id', '=', self.warehouse_1.int_type_id.id), ('location_id', '=', self.warehouse_1.wh_input_stock_loc_id.id), ('location_dest_id', '=', self.warehouse_1.wh_qc_stock_loc_id.id)])
        incoming_shipment1_date = order_date + timedelta(days=self.product_1.seller_ids.delay)
        self.assertEqual(incoming_shipment1.scheduled_date, incoming_shipment1_date, 'Schedule date of Internal Type shipment for input stock location should be equal to: schedule date of warehouse order + push rule delay.')

        incoming_shipment2 = self.env['stock.picking'].search([('picking_type_id', '=', self.warehouse_1.int_type_id.id), ('location_id', '=', self.warehouse_1.wh_qc_stock_loc_id.id), ('location_dest_id', '=', self.warehouse_1.lot_stock_id.id)])
        incoming_shipment2_date = schedule_date - timedelta(days=incoming_shipment2.move_lines[0].rule_id.delay)
        self.assertEqual(incoming_shipment2.scheduled_date, incoming_shipment2_date, 'Schedule date of Internal Type shipment for quality control stock location should be equal to: schedule date of Internal type shipment for input stock location + push rule delay..')

    def test_merge_po_line(self):
        """Chage that merging po line for same procurement is done depending on
        propagate_date and propagate_date_minimum_delta"""

        # create a product with manufacture route
        product_1 = self.env['product.product'].create({
            'name': 'AAA',
            'route_ids': [(4, self.route_buy)],
            'seller_ids': [(0, 0, {'name': self.partner_1.id, 'delay': 5})]
        })

        # create a move for product_1 from stock to output and reserve to trigger the
        # rule
        move_1 = self.env['stock.move'].create({
            'name': 'move_1',
            'product_id': product_1.id,
            'product_uom': self.ref('uom.product_uom_unit'),
            'propagate_date': True,
            'propagate_date_minimum_delta': 1,
            'location_id': self.ref('stock.stock_location_stock'),
            'location_dest_id': self.ref('stock.stock_location_output'),
            'product_uom_qty': 10,
            'procure_method': 'make_to_order'
        })

        move_1._action_confirm()
        po_line = self.env['warehouse.order.line'].search([
            ('product_id', '=', product_1.id),
        ])
        self.assertEqual(len(po_line), 1, 'the warehouse order line is not created')
        self.assertEqual(po_line.product_qty, 10, 'the warehouse order line has a wrong quantity')

        move_2 = self.env['stock.move'].create({
            'name': 'move_2',
            'product_id': product_1.id,
            'product_uom': self.ref('uom.product_uom_unit'),
            'propagate_date': True,
            'propagate_date_minimum_delta': 1,
            'location_id': self.ref('stock.stock_location_stock'),
            'location_dest_id': self.ref('stock.stock_location_output'),
            'product_uom_qty': 5,
            'procure_method': 'make_to_order'
        })

        move_2._action_confirm()
        po_line = self.env['warehouse.order.line'].search([
            ('product_id', '=', product_1.id),
        ])
        self.assertEqual(len(po_line), 1, 'the warehouse order lines should be merged')
        self.assertEqual(po_line.product_qty, 15, 'the warehouse order line has a wrong quantity')

    def test_merge_po_line_2(self):
        """Chage that merging po line for same procurement is done depending on
        propagate_date and propagate_date_minimum_delta"""

        # create a product with manufacture route
        product_1 = self.env['product.product'].create({
            'name': 'AAA',
            'route_ids': [(4, self.route_buy)],
            'seller_ids': [(0, 0, {'name': self.partner_1.id, 'delay': 5})]
        })

        # create a move for product_1 from stock to output and reserve to trigger the
        # rule
        move_1 = self.env['stock.move'].create({
            'name': 'move_1',
            'product_id': product_1.id,
            'product_uom': self.ref('uom.product_uom_unit'),
            'propagate_date': True,
            'propagate_date_minimum_delta': 1,
            'location_id': self.ref('stock.stock_location_stock'),
            'location_dest_id': self.ref('stock.stock_location_output'),
            'product_uom_qty': 10,
            'procure_method': 'make_to_order'
        })

        move_1._action_confirm()
        po_line = self.env['warehouse.order.line'].search([
            ('product_id', '=', product_1.id),
        ])
        self.assertEqual(len(po_line), 1, 'the warehouse order line is not created')
        self.assertEqual(po_line.product_qty, 10, 'the warehouse order line has a wrong quantity')
        po_line.propagate_date = not po_line.propagate_date
        move_2 = self.env['stock.move'].create({
            'name': 'move_2',
            'product_id': product_1.id,
            'product_uom': self.ref('uom.product_uom_unit'),
            'propagate_date': True,
            'propagate_date_minimum_delta': 1,
            'location_id': self.ref('stock.stock_location_stock'),
            'location_dest_id': self.ref('stock.stock_location_output'),
            'product_uom_qty': 5,
            'procure_method': 'make_to_order'
        })

        move_2._action_confirm()
        po_line = self.env['warehouse.order.line'].search([
            ('product_id', '=', product_1.id),
        ])
        self.assertEqual(len(po_line), 2, 'the warehouse order lines are not merged')
        self.assertEqual(po_line[0].product_qty, 10, 'the warehouse order line has a wrong quantity')
        self.assertEqual(po_line[1].product_qty, 5, 'the warehouse order line has a wrong quantity')