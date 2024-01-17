from odoo import api, fields, models
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Photon


class AttendInh(models.Model):
    _inherit = "hr.attendance"

    check_in_address = fields.Text(string="Check In Address", compute="get_checkin_loc", store=True)
    check_out_address = fields.Text(string="Check Out Address", compute="get_checkout_loc", store=True)
    checkin_status = fields.Char(string='Check In Status')
    checkout_status = fields.Char(string='Check Out Status')

    
    @api.depends('check_in_latitude', 'check_in_longitude')
    def get_checkin_loc(self, geolocator=Nominatim(user_agent="geoapiExercises")):
        for record in self:
            latitudein = str(record.check_in_latitude)
            longitudein = str(record.check_in_longitude)
            record.check_in_address = False

            # if latitudein == "0.0" and longitudein == "0.0":
            #     record.check_in_address = False  # or assign a default value
            # else:
            #     try:
            #         location = geolocator.reverse((latitudein, longitudein), exactly_one=True)
            #         if location:
            #             record.check_in_address = location.address
            #         else:
            #             record.check_in_address = "Address not found"
            #     except GeocoderTimedOut:
            #         record.get_checkin_loc_except()
            #         # record.check_in_address = "Geocoding request timed out"
            #     except Exception as e:
            #         record.get_checkin_loc_except()
            #         # record.check_in_address = "Geocoding error: " + str(e)

    @api.depends('check_out_latitude', 'check_out_longitude')
    def get_checkout_loc(self, geolocator=Nominatim(user_agent="geoapiExercises")):
        for record in self:
            latitudeout = str(record.check_out_latitude)
            longitudeout = str(record.check_out_longitude)

            record.check_out_address = False

            # if latitudeout == "0.0" and longitudeout == "0.0":
            #     record.check_out_address = False
            # else:
            #     try:
            #         location = geolocator.reverse((latitudeout, longitudeout), exactly_one=True)
            #         if location:
            #             record.check_out_address = location.address
            #         else:
            #             record.check_out_address = "Address not found"
            #     except GeocoderTimedOut:
            #         record.get_checkout_loc_except()
            #         # record.check_out_address = "Geocoding request timed out"
            #     except Exception as e:
            #         record.get_checkout_loc_except()
            #         # record.check_out_address = "Geocoding error: " + str(e)

    # def get_checkin_loc_except(self, geolocator=Photon(user_agent="geoapiExercises")):
    #     for record in self:
    #         latitudein = str(record.check_out_latitude)
    #         longitudein = str(record.check_out_longitude)
    #
    #         print(latitudein)
    #         print(longitudein)
    #
    #         if latitudein == "0.0" and longitudein == "0.0":
    #             record.check_in_address = False
    #             return record.check_in_address
    #         else:
    #             try:
    #                 record.check_in_address = geolocator.geocode(latitudein + "," + longitudein)
    #                 print(record.check_in_address)
    #                 return record.check_in_address
    #             except:
    #                 record.check_in_address = False


    # def get_checkout_loc_except(self, geolocator=Photon(user_agent="geoapiExercises")):
    #     for record in self:
    #         latitudeout = str(record.check_out_latitude)
    #         longitudeout = str(record.check_out_longitude)
    #
    #         print(latitudeout)
    #         print(longitudeout)
    #
    #         if latitudeout == "0.0" and longitudeout == "0.0":
    #             record.check_out_address = False
    #             return record.check_out_address
    #         else:
    #             try:
    #                 record.check_out_address = geolocator.geocode(latitudeout + "," + longitudeout)
    #                 print(record.check_out_address)
    #                 return record.check_out_address
    #             except:
    #                 record.check_in_address = False



#    @api.depends('check_in_latitude','check_in_longitude')
#    def get_checkin_loc(self, geolocator = Nominatim(user_agent="geoapiExercises")):
#        for record in self:
#            latitudein = str(record.check_in_latitude)
#            longitudein = str(record.check_in_longitude)

#            print(latitudein)
#            print(longitudein)
#            if latitudein == "0.0" and longitudein == "0.0":
#                record.check_in_address = False
#            else:
#                record.check_in_address = geolocator.geocode(latitudein + "," + longitudein)
#                print(record.check_in_address)
#                return record.check_in_address

    # @api.depends('check_out_latitude', 'check_out_longitude')
    # def get_checkout_loc(self, geolocator=Nominatim(user_agent="geoapiExercises")):
    #     for record in self:
    #         latitudeout = str(record.check_out_latitude)
    #         longitudeout = str(record.check_out_longitude)
    #
    #         print(latitudeout)
    #         print(longitudeout)
    #
    #         if latitudeout == "0.0" and longitudeout == "0.0":
    #             record.check_out_address = False
    #         else:
    #             record.check_out_address = geolocator.geocode(latitudeout + "," + longitudeout)
    #             print(record.check_out_address)
    #             return record.check_out_address




