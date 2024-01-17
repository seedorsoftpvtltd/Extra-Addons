from odoo import api, fields, models, modules, _

class ResUsers(models.Model):    
    _inherit = 'res.users'
    
    attendance_face_recognition = fields.Boolean(string="Attendances Face Recognition", default=False)
    log_attendance_geolocation = fields.Boolean(string="Log Attendances Geolocation", default=False)

    def __init__(self, pool, cr):
        init_res = super(ResUsers, self).__init__(pool, cr)
        # duplicate list to avoid modifying the original reference
        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(["attendance_face_recognition"])
        type(self).SELF_WRITEABLE_FIELDS.extend(["log_attendance_geolocation"])
        # duplicate list to avoid modifying the original reference
        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend(["attendance_face_recognition"])
        type(self).SELF_READABLE_FIELDS.extend(["log_attendance_geolocation"])        
        return init_res
    
    def attendance_face_recognition_reload(self):
        return {
            "type": "ir.actions.client",
            "tag": "reload_context"
        }
    
    def log_attendance_geolocation_reload(self):
        return {
            "type": "ir.actions.client",
            "tag": "reload_context"
        }

