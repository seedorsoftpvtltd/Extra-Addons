from odoo import api, fields, models, _


class HrAttendanceApproval(models.Model):
    _inherit = 'hr.attendance'

    state = fields.Selection([('draft', 'Draft'),
                              ('validated', 'Validated'),
                              ('approved', 'Approved'),
                              ('refused', 'Refused')], string="state",
                             default="draft")

    def validate(self):
        for approve in self:
            approve['state'] = 'validated'

    @api.constrains('checkin_status', 'checkout_status')
    def attendance_approve_reject(self):
        for rec in self:
            if str(rec.checkin_status).__contains__('Success') and str(rec.checkout_status).__contains__('Success'):
                rec.validate()
            if rec.checkout_status == False and str(rec.checkin_status).__contains__('Success'):
                rec.validate()
            if str(rec.checkin_status).__contains__('Success') and str(rec.checkout_status).__contains__('Failed'):
                rec['state'] = 'draft'

            # elif str(rec.checkin_status).__contains__('Failed') and str(rec.checkout_status).__contains__('Success'):
            #     rec.refuse()
            # elif str(rec.checkin_status).__contains__('Success') and str(rec.checkout_status).__contains__('Failed'):
            #     rec.refuse()
            # elif str(rec.checkin_status).__contains__('Failed') and str(rec.checkout_status).__contains__('Failed'):
            #     rec.refuse()
