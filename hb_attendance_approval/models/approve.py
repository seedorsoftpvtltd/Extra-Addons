from odoo import api, fields, models, _


class HrAttendanceApproval(models.Model):
    _inherit = 'hr.attendance'

    state = fields.Selection([('draft', 'Draft'),
                              ('approved', 'Approved'),
                              ('refused', 'Refused')], string="state",
                             default="draft")

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super(HrAttendanceApproval, self).create(vals_list)
    #     for rec in res:
    #         if rec.check_out:
    #             rec.state = 'approved'
    #         return res

    def approve(self):
        for approve in self:
            approve['state'] = 'approved'

    def refuse(self):
        for reject in self:
            reject['state'] = 'refused'