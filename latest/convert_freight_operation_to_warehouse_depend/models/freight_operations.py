from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime

class freight(models.Model):
    _inherit='freight.operation'


    def action_create_asn(self):

        self.ensure_one()
        res = self.env['warehouse.order']

        war = res.search(
            [
                ("main_id", "=", self.id),

            ]
        )

        for rec in self.operation_line_ids:
            print(rec.partner_id)
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




