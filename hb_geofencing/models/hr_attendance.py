from odoo import api, fields, models
from geopy.geocoders import Nominatim


class AttendInh(models.Model):
    _inherit = "hr.attendance"

    check_in_address = fields.Text(string="Check In Address", compute="get_checkin_loc")
    check_out_address = fields.Text(string="Check Out Address", compute="get_checkout_loc")

    @api.depends('check_in_latitude','check_in_longitude')
    def get_checkin_loc(self, geolocator = Nominatim(user_agent="geoapiExercises")):
        for record in self:
            latitudein = str(record.check_in_latitude)
            longitudein = str(record.check_in_longitude)

            print(latitudein)
            print(longitudein)
            if latitudein == "0.0" and longitudein == "0.0":
                record.check_in_address
            else:
                record.check_in_address = geolocator.geocode(latitudein + "," + longitudein)
                print(record.check_in_address)
                return record.check_in_address

    @api.depends('check_out_latitude', 'check_out_longitude')
    def get_checkout_loc(self, geolocator=Nominatim(user_agent="geoapiExercises")):
        for record in self:
            latitudeout = str(record.check_out_latitude)
            longitudeout = str(record.check_out_longitude)

            print(latitudeout)
            print(longitudeout)

            if latitudeout == "0.0" and longitudeout == "0.0":
                record.check_out_address
            else:
                record.check_out_address = geolocator.geocode(latitudeout + "," + longitudeout)
                print(record.check_out_address)
                return record.check_out_address




