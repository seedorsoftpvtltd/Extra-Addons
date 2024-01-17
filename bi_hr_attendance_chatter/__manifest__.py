# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
	"name" : "HR Attendance Chatter and Activity",
	"version" : "13.0.0.0",
	"category" : "Human Resources",
	'summary': 'HR Attendance Chatter Odoo App helps to user can use attendance chatter in form view. User can use attendance chatter with using 3 options like send message, log note and schedule activity.',
	"description": """
			
			HR Attendance Chatter in odoo,
			Attendance Chatter in odoo,
			Chatter in Attendance form view in odoo,
			Send Message in chatter in odoo,
			Log Note in chatter in odoo,
			Schedule Activity in chatter in odoo,

	""",
	"author": "BrowseInfo",
	"website" : "https://www.browseinfo.in",
	"price": 10,
	"currency": 'EUR',
	"depends" : ['base','mail', 'hr_attendance'],
	"data": [	
				"views/hr_attendance.xml",
			],
	"auto_install": False,
	"installable": True,
	'live_test_url':'https://youtu.be/fi4xaLlpZ68',
    "images":["static/description/Banner.png"],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
