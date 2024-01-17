# -*- coding: utf-8 -*-
#################################################################################
# Author      : CFIS (<https://www.cfis.store/>)
# Copyright(c): 2017-Present CFIS.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://www.cfis.store/>
#################################################################################

{
    "name": "Attendance Geolocation - Attendance Location",
    "summary": """
        This module helps you to capture the employees attendance check in / check out Geolocation Coordinates information and 
        generate a direct links to Google Maps from Employee Attendance.
    """,
    "version": "13.0.1",
    "description": """
        This module helps you to capture the employees attendance check in / check out Geolocation Coordinates information and 
        generate a direct links to Google Maps from Employee Attendance.
        HR Attendance Geolocation.
        Attendance Geolocation.
        Attendance check in / check out location.
        Attendance Location.
        Attendance latitude and longitude.
        HR Attendance Location.
        Attendance Google Map.
        check in / check out location.        
        latitude and longitude.
        Google Map.                
    """,    
    "author": "CFIS",
    "maintainer": "CFIS",
    "license" :  "Other proprietary",
    "website": "https://www.cfis.store",
    "images": ["images/attendance_geolocation_log.png"],
    "category": "eCommerce",
    "depends": [
        "base",
        "hr_attendance",
    ],
    "data": [
        "data/geolocation_data.xml",
        "views/assets.xml",
        "views/res_users.xml",
        "views/hr_attendance_views.xml",
    ],
    "qweb": [
        "static/src/xml/*.xml"
    ],
    "installable": True,
    "application": True,
    "price"                 :  20.00,
    "currency"              :  "EUR",
    "pre_init_hook"         :  "pre_init_check",
}
