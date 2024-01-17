from odoo import api, models, _

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def attendance_manual(self, next_action, entered_pin=None, location=False):
        res = super(HrEmployee, self.with_context(attendance_geolocation=location)).attendance_manual(next_action, entered_pin)        
        return res

    def _attendance_action_change(self):
        res = super()._attendance_action_change()
        geolocation = self.env.context.get('attendance_geolocation', False)
        if geolocation:            
            if self.attendance_state == 'checked_in':
                vals = {
                    'check_in_latitude': geolocation[0],
                    'check_in_longitude': geolocation[1],
                }
                res.write(vals)
            else:
                vals = {
                    'check_out_latitude': geolocation[0],
                    'check_out_longitude': geolocation[1],
                }
                res.write(vals)
        return res