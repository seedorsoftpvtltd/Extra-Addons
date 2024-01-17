from odoo import api, fields, models, _

class servicetypes(models.Model):
    _name='service.types'
    _rec_name = 'types'
    types=fields.Char(string='Scope Of Service',store=True)
    # title=fields.Char(string='Name')
    terms = fields.Text(string='Terms and Conditions', required=True,store=True)


class sale(models.Model):
    _inherit='sale.order'

    x_service_type=fields.Many2one('service.types',string='Scope Of Service')
    term=fields.Text(string='Term',compute='_terms')

    def _terms(self):
        for rec in self:
            print("qqqqqqqqqqqqqqqq")
            if rec.x_service_type:
                print("diiiiiiiiiiiiiiii")
                rec['term']=rec.x_service_type.terms
            else:
                rec['term']=''