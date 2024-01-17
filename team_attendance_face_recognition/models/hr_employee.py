from odoo import fields, models, api, _

class HrEmployee(models.Model):
    _inherit = "hr.employee"
    
    user_faces = fields.One2many("hr.employee.faces", "employee_id", "Faces")

    def attendance_manual(self, next_action, entered_pin=None, img=False, location=False):
        print ("===================location", location)
        res = super(HrEmployee, self.with_context(attendance_image=img,attendance_geolocation=location)).attendance_manual(next_action, entered_pin)        
        return res

    def _attendance_action_change(self):
        res = super()._attendance_action_change()
        attendance_image = self.env.context.get('attendance_image', False)
        attendance_geolocation = self.env.context.get('attendance_geolocation', False)
        print ("===================", attendance_geolocation)
        if attendance_image:
            if self.attendance_state == 'checked_in':
                res.write({
                    'check_in_image': attendance_image,
                })
            else:
                res.write({
                    'check_out_image': attendance_image,
                })
        
        if attendance_geolocation:            
            if self.attendance_state == 'checked_in':
                vals = {
                    'check_in_latitude': attendance_geolocation[0],
                    'check_in_longitude': attendance_geolocation[1],
                }
                res.write(vals)
            else:
                vals = {
                    'check_out_latitude': attendance_geolocation[0],
                    'check_out_longitude': attendance_geolocation[1],
                }
                res.write(vals)        
        return res
    
    @api.model
    def attendance_kiosk_recognition(self, id, img):
        employee = self.sudo().search([('id', '=', id)], limit=1)
        if employee:
            return employee.with_context(attendance_image=img)._attendance_action('hr_attendance.hr_attendance_action_kiosk_mode')
        return {'warning': _('No employee corresponding to face id %(employee)s') % {'employee': id}}

class HrEmployeeFaces(models.Model):
    _name = "hr.employee.faces"
    _description = "Face Recognition Images"
    _inherit = ['image.mixin']
    _order = 'id'

    name = fields.Char("Name", related='employee_id.name')
    image = fields.Binary("Images")
    descriptor = fields.Text(string='Face Descriptor')
    has_descriptor = fields.Boolean(string="Has Face Descriptor",default=False, compute='_compute_has_descriptor', readonly=True, store=True)
    employee_id = fields.Many2one("hr.employee", "User", index=True, ondelete='cascade')

    @api.depends('descriptor')
    def _compute_has_descriptor(self):
        for rec in self:
            rec.has_descriptor = True if rec.descriptor else False

