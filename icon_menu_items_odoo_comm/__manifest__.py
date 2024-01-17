# -*- coding: utf-8 -*-
# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Icons for Submenu Items',
    'version' : '2.1.2',
    'price' : 49.0,
    'currency': 'EUR',
    'category': 'Tools',
    'license': 'Other proprietary',
    'live_test_url': 'http://probuseappdemo.com/probuse_apps/icon_menu_items_odoo_comm/226',#'https://youtu.be/yLCLU51DxfA',
    'images': [
        'static/description/img.jpg',
    ],
    'summary': 'This app allows you to show menu icons on the sub menu list.',
    'description': """
This app allows you to show menu icons on the sub menu list.You have to first configure it on menu form for every menu you want to see icons.
This app allows you to see icons on the submenu of odoo menu items. You can first select the icon on the menu item form under technical settings of Odoo then only the icon will appear for the specific menu.
For more details please check below screenshots and watch the video.
    """,
    'author' : 'Probuse Consulting Service Pvt. Ltd.',
    'website' : 'wwww.probuse.com',
    'depends' : [
        'web',
    ],
    'support': 'contact@probuse.com',
    'data' : [
    ],
    'qweb': [
        "static/src/xml/menu.xml",
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
