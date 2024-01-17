from odoo.http import request
from odoo import api, fields, models, tools, osv, http, _


class partner_fix(models.Model):
    _inherit = "res.partner"

    def create(self, vals):
        res = super(partner_fix, self).create(vals)
        print(self.env.company, self.env.context, 'self.env.context')
        company_id = self.env.company
        res['company_id'] = company_id
        return res


class compaany_fix(models.Model):
    _inherit = "res.company"

    def create(self, vals):
        res = super(compaany_fix, self).create(vals)
        print(self.env.company, self.env.context, 'self.env.context')
        res.partner_id.write({'company_id': res.id})
        return res


    # company_id = fields.Many2one(
    #     'res.company',
    #     string='Company',
    #     default=lambda self: self.env.company,
    #     readonly=True,
    #     store=True,
    # )

    # @api.onchange('company_id')
    # def _onchange_company_id(self):
    #     if not self.id and self.company_id:
    #         self.parent_id = False



