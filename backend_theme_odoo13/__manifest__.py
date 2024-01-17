# -*- coding: utf-8 -*-
# Copyright 2019, 2020 Odoo VietNam - WinERP
# Website winerp.vn, odoovietnam.com.vn
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Material Backend Theme Odoo 13 Community",
    "version": "13.0.0.8",
    "summary": "Material Backend Theme Odoo 13 Community - Support Mobile Web Responsive",
    "category": "Web/Backend",
    "author": "Odoo VietNam - WinERP",
    "support": "info@winerp.vn",
    "website": "https://winerp.vn",
    "license": "LGPL-3",
	'description': """
		Material Backend theme for Odoo 13 Community and support Mobile Web Responsive.
    """,
    'depends': [
        'web',
        'backend_theme_web_responsive_odoo13'

    ],
    'data': [
        'views/assets.xml',
		'views/res_company_view.xml'
    ],
    'images':[
        'static/description/module-cover.jpg',
        'static/description/screenshot1.png',
        'static/description/screenshot2.png'
	],
    'installable': True,
    'auto_install': False,
    'application': True
}

