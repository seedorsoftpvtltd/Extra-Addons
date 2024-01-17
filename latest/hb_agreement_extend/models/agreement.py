from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF


class agreementcharge(models.Model):
    _inherit = "agreement"

    charge_lines = fields.One2many('agreement.charges', 'agreement_id', readonly=False, copy=True)
    charge_lines_new = fields.One2many('agree.charges', 'agree_id', readonly=False, copy=True)
    type = fields.Selection(string="Agreement Type", selection=[('cfs', 'CFS'), ('warehouse', 'Warehouse')])

    @api.model
    def create(self, vals):
        res = super(agreementcharge, self).create(vals)
        for rec in self:
            for line in rec.charge_lines:
                line.agreement_id = rec.id
        return res

    @api.constrains('name')
    def _agreement(self):
        for rec in self:
            domain = [('partner_id', '=', rec.partner_id.id)]
            count = self.sudo().search_count(domain)
            if count > 1:
                raise UserError(_("You are not allow to create more than agreement for a customer"))


class servicecharge(models.Model):
    _name = "agree.charges"
    _description = "Sevices"

    product_id = fields.Many2one("product.product", string="Service")
    agree_id = fields.Many2one("agreement", string="Agreement")
    partner_id = fields.Many2one("res.partner", string="Partner")
    charge_unit_type = fields.Selection(string="Uom",
                                        selection=[('cbm', 'Per CBM'), ('shipment', 'Per Shipment')])
    list_price = fields.Float(string="Price")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id)
    charge_type = fields.Selection(string="Charge Type",
                                   selection=[('fixed', 'Fixed Charges'), ('storage', 'Storage')])
    fromm = fields.Integer(string="from")
    to = fields.Integer(string="To")
    duration = fields.Integer(string="Duration")
    storage_type = fields.Selection(string="Storage Type",
                                    selection=[('hazardous', 'Harardous Storage'),
                                               ('non_hazardous', 'Non  Harardous Storage')])


class servicechargeagree(models.Model):
    _name = "agreement.charges"
    _description = "Sevices"

    product_id = fields.Many2one("product.product", string="Service")
    agreement_id = fields.Many2one("agreement", string="Agreement")
    partner_id = fields.Many2one("res.partner", string="Partner")
    invoice_id = fields.Many2one("account.move", string="Invoice")
    inv_line_id = fields.Many2one("account.move.line", string="Invoice Line")
    charge_unit_type = fields.Selection(string="Charge Type",
                                        selection=[('cbm', 'CBM'), ('pallet', 'Pallet'), ('weight', 'Weight'),
                                                   ('square', 'Square Units'), ('custom','Custom')])
    # bill_id = fields.Many2one("account.move", string="Bill")
    # bill_line_id = fields.Many2one("account.move.line", string="Bill Line")
    # qty = fields.Integer(string="QTY", default=1)
    uom_id = fields.Many2one("uom.uom", string="Unit of Measure")
    list_price = fields.Float(string="Price", )

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    charge_type = fields.Selection(string="Charge Unit Type",
                                   selection=[('inbound', 'Handling Inbound'), ('outbound', 'Handling Outbound'),
                                              ('storage', 'Storage'), ('value_added', 'Value Added Services'),
                                              ('inventory_mgmnt', 'Inventory Management Services')], default='storage')
    storage_type = fields.Many2one('storage.type', string="Storage Type", store=True)
    # storage_type = fields.Selection(string="Storage Type",
    #                                selection=[('temperatue', 'Temperature control'), ('outbound', 'Handling Outbound'),
    #                                           ('storage', 'Storage'), ('value_added', 'Value Added Services'),
    #                                           ('inventory_mgmnt', 'Inventory Management Services')])
    added_service = fields.Many2one('added.service', string="Added service")
    container = fields.Many2one('freight.container', string="Container")
    storage_uom = fields.Selection(string="Storage UOM", selection=[('day', 'Per Day'), ('month', 'Per Month')])
    tax_id = fields.Many2many('account.tax', string='Tax')

