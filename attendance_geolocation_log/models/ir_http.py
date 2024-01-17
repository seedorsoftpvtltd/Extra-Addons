  
from odoo import models
from odoo.http import request

class Http(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        user = self.env.user
        result = super(Http, self).session_info()
        if self.env.user.has_group('base.group_user'):
            result['log_attendance_geolocation'] = user.log_attendance_geolocation
        return result