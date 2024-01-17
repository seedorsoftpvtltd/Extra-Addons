from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ResConfigSettingsrem(models.TransientModel):
    _inherit = ['res.config.settings']

    alert_rem = fields.Integer(string='Reminder for Vehicle', default=30,
                               config_parameter='hb_fleet_template.alert_rem')


class VehreqReminder(models.Model):
    _inherit = "employee.fleet"

    def action_rem(self):
        print('hlooooooo')
        #if self.env['ir.config_parameter'].sudo().get_param('hb_fleet_template.alert_rem'):
        request_ids = self.env['employee.fleet'].search([('state', '=', 'confirm')])
        today = datetime.now().date()
        print(request_ids)
        for req in request_ids:
            params = self.env['ir.config_parameter'].sudo()
            d = int(params.get_param('hb_fleet_template.alert_rem', default=2))
            print(d)
            # dd = relativedelta(days=+d)
            # print(dd)
            dbefore = datetime.strptime(str(req.date_to), "%Y-%m-%d %H:%M:%S") - relativedelta(days=+d)
            before = dbefore.date()
            print(req.id, req.date_to, 'before', before, 'today', today,)
            if today == before:
                # for vehicle in req.filtered(lambda v: v.employee and req.employee.work_email):
                print("sent mail")
                res = self.env.ref('hb_fleet_template.emp_fleet_due_template')
                res.send_mail(req.id, force_send=True)
        return True







