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
    "name": "HR Attendance Face Recognition",
    "summary": "This module allows you to log employee attendance check-ins and check-outs utilizing Face Recognition. This functionality works in conjunction with Record Employees Photograph while check in/out.",
    "version": "13.0.1",
    "description": """
        This module helps you to log the employees attendance check in / check out using Face Recognition.      
    """,    
    "author": "CFIS",
    "maintainer": "CFIS",
    "license" :  "Other proprietary",
    "website": "https://www.cfis.store",
    "images": ["images/team_attendance_face_recognition.png"],
    "category": "Employees",
    "depends": [
        "base",
        "hr",
        "hr_attendance",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/geolocation_data.xml",
        "views/assets.xml",
        "views/res_users.xml",
        "views/hr_employee_views.xml",
        "views/res_config_settings.xml",
        "views/hr_attendance_views.xml",        
    ],
    "qweb": [
        "static/src/xml/*.xml"
    ],
    "installable": True,
    "application": True,
    "price"                :  75,
    "currency"             :  "EUR",
    "pre_init_hook"        :  "pre_init_check", 
}
