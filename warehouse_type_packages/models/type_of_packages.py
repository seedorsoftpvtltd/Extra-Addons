from odoo import models, fields, api, _


class TypeofPackages(models.Model):
    _name = "warehouse.packages"
    _description = "WareHouse Package"

    # name = fields.Char(string="", )
    name = fields.Char(string="Code", store=True)
    description = fields.Char(string="Description", store=True)
    short_description = fields.Char(string="Short Description", store=True)


class WarehouseOrder(models.Model):
    _inherit = "warehouse.order"

    type_of_package = fields.Many2many('warehouse.packages', string='Type of Pkgs', )


class Picking(models.Model):
    _inherit = "stock.picking"

    type_of_package = fields.Many2many('warehouse.packages', string='Type of Pkgs', readonly=False,
                                       related='warehouse_id.type_of_package')



# class ProductProduct(models.Model):
#     _inherit = "product.product"
#
#     ware_tax_id = fields.Many2many('account.tax', 'ware_taxes_rel', 'prod_id', 'tax_id', string='Taxes',
#                                    domain=[('type_tax_use', '=', 'none')])
