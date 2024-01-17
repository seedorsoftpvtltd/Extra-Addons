from odoo import models, fields, api, _


class TransferServiceTab(models.Model):
    _name = "picking.services"

    picking_id = fields.Many2one('stock.picking', string="Transfer ID")
    product_id = fields.Many2one("product.product", string="Product")
    price = fields.Float(string="Price")
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure', required=True)
    qty = fields.Integer(string="Quantity")
    taxes_id = fields.Many2many('account.tax', string='Taxes')
    container_type = fields.Many2one('freight.container', string='Container')



# class uommaster(models.Model):
#     _name = "inv.meth"
#
#     name = fields.Char('Name')
#     uom = fields.Many2one('uom.uom', string='UOM')

class Picking(models.Model):
    _inherit = "stock.picking"

    service_id = fields.One2many("picking.services", "picking_id", string="Service")


# class uommaster(models.Model):
#     _inherit = "uom.uom"
#
#     inv_meth = fields.Selection(selection=[('cbm', 'CBM'), ('pallet', 'Pallet'), ('weight', 'Weight'),
#                                            ('carton_units', 'Carton/Units'), ('square', 'Square Units')],
#                                 string="Invoice Method")
