# -*- coding: utf-8 -*-

{
	'name' : 'Letters and Certificate Management',
	'author': "Edge Technologies",
	'version' : '13.0.1.1',
	'live_test_url':'https://youtu.be/zx3ZlV9-7EE',
	"images":["static/description/main_screenshot.png"],
	'category' : 'Extra Tools',
	'summary' : 'Letters and Certificate employee Certificate system letter management system print Certificate print employee certificate generate letters generate certificates generate employee certificates partner certificate customer certification  business letters',
	'description' : """	
		This app helps user to create a letter and certificate.
	""",
	'depends' : ['base','mail','hr'],
    "license" : "OPL-1",
	'data' : [
		'security/ir.model.access.csv',
		'views/certificate.xml',
		'views/letter.xml',
		'views/email_template.xml',
	],
	'qweb' : [],
	'demo' : [],
	'installable' : True,
	'auto_install' : False,
	'price': 15,
	'currency': "EUR",
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
