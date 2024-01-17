from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime


class Job(models.Model):
    _inherit = "warehouse.order"

    main_id = fields.Many2one('freight.operation', string='Freight', store=True)
    master_bl = fields.Char(string="Master BL", readonly=True, copy=False)
    war_line_id = fields.Many2one('freight.operation.line', string='War Line Id')

class freightoperation(models.Model):
        _inherit = 'warehouse.order.line'

        freight_operation_line_link = fields.Many2one('freight.operation.line', string='Warehouse Line Link')


class freightline(models.Model):
    _inherit = 'freight.operation.line'

    partner_id = fields.Many2one('res.partner', string='Customer')
    freight_operation_l_link = fields.Many2one('warehouse.order.line', string='Warehouse Link')

class freight(models.Model):
    _inherit='freight.operation'

    freight_operation_link = fields.Many2one('warehouse.order',string='Warehouse Link')
    asn_cnt = fields.Integer('ASN Count', compute='_compute_asn_cnt')




    def _compute_asn_cnt(self):
        obj = self.env['warehouse.order']
        for serv in self:
            cnt = obj.search_count([
                ('main_id', '=', serv.id)])
            if cnt != 0:

                serv['asn_cnt'] = cnt
            else:

                serv['asn_cnt'] = 0

    def action_create_asn(self):

        self.ensure_one()
        res = self.env['warehouse.order']

        war = res.search(
            [
                ("main_id", "=", self.id),

            ]
        )

        for rec in self.operation_line_ids:
            if not rec.freight_operation_l_link:
                val = []
                val.append([0, 0, {
                    'product_id': rec.product_id.id,
                    'name': rec.product_id.name,
                    'product_qty': rec.qty,
                    'product_uom': rec.product_id.uom_id.id,
                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'taxes_id': rec.product_id.supplier_taxes_id.ids,
                    'price_unit': rec.price,
                    'freight_operation_line_link': rec.id,
                    'order_id': rec.id,
                }])
                war=res.create({
                    'partner_id': rec.partner_id.id,
                    'main_id': self.id,
                    'order_line': val,
                    'war_line_id': rec.id,
                })
                rec['freight_operation_l_link'] = war.order_line[0]

            else:
                for war1 in war:
                    if war1.war_line_id == rec:
                        val = []
                        val.append([0, 0, {
                            'product_id': rec.product_id.id,
                            'name': rec.product_id.name,
                            'product_qty': rec.qty,
                            'product_uom': rec.product_id.uom_id.id,
                            'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                            'taxes_id': rec.product_id.supplier_taxes_id.ids,
                            'price_unit': rec.price,
                            'freight_operation_line_link': rec.id,
                            'order_id': rec.id,
                        }])
                        war1.order_line.unlink()
                        war1.write({
                            'partner_id': rec.partner_id.id,
                            'main_id': self.id,
                            'order_line': val,
                            'war_line_id': rec.id,
                        })
                        rec['freight_operation_l_link'] = war1.order_line

        return res


class saleorder(models.Model):
    _inherit = 'warehouse.order'

    house_bl = fields.Char(string="House BL", copy=False)


