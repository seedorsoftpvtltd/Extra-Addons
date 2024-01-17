from odoo import models, fields, api


class importbugfix(models.Model):
    _inherit = 'product.template'

    description = fields.Char('Description', related='product_description.name', store=True, readonly=False)

    @api.constrains('description')
    def prod_desc(self):
        for rec in self:
            if rec.description and not rec.product_description:
                packages_list = self.env['product.description'].search([('name', '=', rec.description)])
                if packages_list:
                    packages = packages_list[0]['name']
                    if not packages:
                        desc = self.env['product.description'].create({'name': rec.description})
                        rec['product_description'] = desc
                    else:
                        # for des in packages:
                        if rec.description in packages:
                            rec['product_description'] = self.env['product.description'].search([('name', '=', packages)])[0]
                        else:
                            desc = self.env['product.description'].create({'name': rec.description})
                            rec['product_description'] = desc
                else:
                    desc = self.env['product.description'].create({'name': rec.description})
                    rec['product_description'] = desc


class importbugfixstock(models.Model):
    _inherit = 'stock.move.line'

    pack_name = fields.Char('Pallet Name', store=True)

    @api.constrains('pack_name')
    def prod_desc(self):
        for rec in self:
            if rec.pack_name and not rec.result_package_id:
                packages_list = self.env['stock.quant.package'].search([('name', '=', rec.pack_name)])
                if packages_list:
                    packages = packages_list[0]['name']
                    if not packages:
                        pal = self.env['stock.quant.package'].create({'name': rec.pack_name})
                        rec['result_package_id'] = pal
                    else:
                        # for des in packages:
                        if rec.pack_name in packages:
                            rec['result_package_id'] = self.env['stock.quant.package'].search([('name', '=', packages)])[0]
                        else:
                            pal = self.env['stock.quant.package'].create({'name': rec.pack_name})
                            rec['result_package_id'] = pal
                else:
                    pal = self.env['stock.quant.package'].create({'name': rec.pack_name})
                    rec['result_package_id'] = pal


