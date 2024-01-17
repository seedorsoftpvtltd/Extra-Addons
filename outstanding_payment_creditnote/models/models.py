from odoo import api, fields, models, _

class Res_Partner(models.Model):
    _inherit = 'res.partner'

    oustanding_invoice_ids = fields.One2many('account.payment', 'partner_id', 'Customer move lines', readonly='False',
                                             domain=[('has_invoices', '=', False), ('partner_type', '=', 'customer'),
                                                     ('payment_type', '=', 'inbound'), ('state', 'in', ['posted'])])
    oustanding_credit_ids = fields.One2many('account.payment', 'partner_id', 'Customer move lines', readonly='False',
                                            domain=[('has_invoices', '=', False), ('partner_type', '=', 'customer'),
                                                    ('payment_type', '=', 'outbound'), ('state', 'in', ['posted'])])
    supplier_paymnet_ids = fields.One2many('account.payment', 'partner_id', 'Customer move lines', readonly='False',
                                             domain=[('has_invoices', '=', False), ('partner_type', '=', 'supplier'),
                                                     ('payment_type', '=', 'outbound'), ('state', 'in', ['posted'])])
    supplier_credit_ids = fields.One2many('account.payment', 'partner_id', 'Customer move lines', readonly='False',
                                            domain=[('has_invoices', '=', False), ('partner_type', '=', 'supplier'),
                                                    ('payment_type', '=', 'inbound'), ('state', 'in', ['posted'])])


class Accountpayment(models.Model):
    _inherit='account.payment'


    has_invoices = fields.Boolean(string='Has Invoices',store=True,readonly=False)
    flag= fields.Boolean(string='Flag',related='has_invoices')
