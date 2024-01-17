from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Column Section
    # standard_price_tax_included = fields.Float(
    #     compute='_compute_standard_price_tax_included',
    #     string='Cost Price Tax Included', company_dependent=True,
    #     digits=dp.get_precision('Product Price'),
    #     help="Cost Price of the product, All Tax Included:\n"
    #     "This field will be computed with the 'Cost Price', taking into"
    #     " account Sale Taxes setting.")
    standard_price_tax_included = fields.Float(
        compute='_compute_standard_price_tax_included',
        string='Cost Price Tax Included',
        digits=dp.get_precision('Product Price'))
    price_included = fields.Text(string="Price Included", compute='_compute_tax_type')

    @api.depends('taxes_id')
    def _compute_tax_type(self):
        for rec in self:
            print('000000000000')
            if rec.taxes_id:
                for tax in rec.taxes_id:
                    print('111111111111')
                    if tax.children_tax_ids:
                        print('2222222222')
                        for child in tax.children_tax_ids:
                            print('3333333333')
                            if child:
                                if child.price_include == True:
                                    rec['price_included'] = 'Tax Included'
                                else:
                                    rec['price_included'] = 'Tax Excluded'
                            else:
                                rec['price_included'] = 'Tax Excluded'
                    else:
                        print('44444444444')
                        if rec.price_included == True:
                            rec['price_included'] = 'Tax Included'
                        else:
                            rec['price_included'] = 'Tax Excluded'
            else:
                rec['price_included'] = ''






    # @api.multi
    @api.depends('list_price')
        # 'standard_price', 'taxes_id', 'taxes_id.type', 'taxes_id.amount')
    def _compute_standard_price_tax_included(self):
        for template in self:
            info = template.taxes_id.compute_all(
                template.list_price)
            template.standard_price_tax_included = info['total_included']
            print(template.standard_price_tax_included,'standard_price_tax_included')
