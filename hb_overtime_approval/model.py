from odoo import models, api, fields


class OvertimeInherit(models.Model):
    _inherit = 'hr.overtime'

    state = fields.Selection([('draft', 'Draft'),
                              ('f_approve', 'Waiting'),
                              ('approved1', 'First Level Approved'),
                              ('approved', 'Approved'),
                              ('refused', 'Refused')], string="state",
                             default="draft")

    def firstapprove(self):
        for rec in self:
            if rec.state == 'f_approve':
                return self.sudo().write({
                    'state': 'approved1',

                })
