# -*- coding: utf-8 -*-
{
    'name': "Vendor Invoice Number in Dynamic Reports View",

    'summary': """Vendor Invoice Number in Dynamic Reports View""",

    'description': """Vendor Invoice Number in Dynamic Reports View""",

    'author': " Fousia Banu A.R ",
    'website': "https://www.facebook.com/groups/246493319957599/",
    'category': 'Sale',
    'version': '13.0',
    "license": "AGPL-3",
    'images': ['static/description/3.png'],
    'depends': ['account_dynamic_reports','dynamic_xlsx','as_on_filter_dynamic_reports'],
    'data': [
    ],
     'qweb':
         ['static/src/xml/view.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,

}
