import werkzeug
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp

GEOLOCATION = dp.get_precision("Gelocation")

class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    check_in_latitude = fields.Float("Check-in Latitude", digits=GEOLOCATION, readonly=True)
    check_in_longitude = fields.Float("Check-in Longitude", digits=GEOLOCATION, readonly=True)
    check_out_latitude = fields.Float("Check-out Latitude", digits=GEOLOCATION, readonly=True)
    check_out_longitude = fields.Float("Check-out Longitude", digits=GEOLOCATION, readonly=True)
    check_in_location_link = fields.Char('Check In Location', compute='_compute_check_in_location_url')
    check_out_location_link = fields.Char('Check Out Location', compute='_compute_check_out_location_url')

    @api.depends('check_in_latitude','check_in_longitude')
    def _compute_check_in_location_url(self):
        for attendance in self:
            params = {
                'q': '%s,%s' % (attendance.check_in_latitude or '',attendance.check_in_longitude or ''),'z': 10,
            }
            attendance.check_in_location_link = werkzeug.Href('https://maps.google.com/maps')(params or None)

    @api.depends('check_out_latitude','check_out_longitude')
    def _compute_check_out_location_url(self):
        for attendance in self:
            params = {
                'q': '%s,%s' % (attendance.check_out_latitude or '',attendance.check_out_longitude or ''),'z': 10,
            }
            attendance.check_out_location_link = werkzeug.Href('https://maps.google.com/maps')(params or None)