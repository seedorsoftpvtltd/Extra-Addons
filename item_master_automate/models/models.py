from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import datetime


class itemmaster(models.Model):
    _inherit = "item.master"

    weight = fields.Float(string="Weight", related='product_id.weight')
    length = fields.Float(string="Length", related='product_id.product_length')
    height = fields.Float(string="Height", related='product_id.product_height')
    width = fields.Float(string="Width", related='product_id.product_width')
    volume = fields.Float(string="Volume", related='product_id.volume')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    partner_id = fields.Many2one('res.partner', string="Customer", required=True,related='product_id.customer_id')
    description = fields.Char(string="Description", required=True,related='product_id.description')
    sku_no = fields.Char(string="Product Code", required=True, store=True,related='product_id.name')
    name = fields.Char(string="Name", store=True, readonly=True,related='product_id.name')

class ProductTemplate(models.Model):
    _inherit = "product.template"

    customer_id = fields.Many2one('res.partner', string='Customer')
    flag = fields.Boolean(string="Created")
    country_id = fields.Many2one('res.country', 'COO',help="Country Of Origin", readonly=False)
    remarks = fields.Char(string='Remarks', copy=False)
    description = fields.Char(string='Description', copy=False)
    #prod_code = fields.Char(string='Product Code')
    #_sql_constraints = [("prod_code_unique", "UNIQUE(prod_code)", "Product Code Must Be Unique!")]

    @api.constrains('name')
    def _check_name(self):
        for rec in self:
           if rec.type == 'product':
            domain = [('name', '=', rec.name)]
            count = self.sudo().search_count(domain)
            if count > 1:
                raise ValidationError(_("Product Code Must Be Unique."))

class ProductProduct(models.Model):
    _inherit = "product.product"
    def itemautomate(self):
        for rec in self:
            if rec.type == 'product' and rec.x_medium.name == 'Warehouse':
                if not rec.customer_id or not rec.description:
                    raise ValidationError(_("Please Fill Customer Name And Description."))
                else:

                    vals = {'product_id': rec.id,
                            'name': rec.name,
                            'sku_no': rec.name,
                            'description': rec.description,
                            'partner_id': rec.customer_id.id,
                            'height': rec.product_height,
                            'length': rec.product_length,
                            'width': rec.product_width,
                            'volume': rec.volume,
                            'weight': rec.weight,
                            }
                    # print(vals)
                    ins = self.env['item.master'].create(vals)
                    rec.item = ins.id

        return True
