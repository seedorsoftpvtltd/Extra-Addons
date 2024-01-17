# pylint: disable=missing-docstring,manifest-required-author
{
    'name': 'Account Purchase Menu',
    'summary': 'Account Purchase Menu',
    'author': 'CORE B.P.O',
    'maintainer': 'Abdalla Mohamed',
    'website': 'http://www.core-bpo.com',
    'version': '13.0.1.0.0',
    'category': 'Accounting/Accounting',
    'license': 'OPL-1',
    'depends': [
        'purchase',
        'account',
    ],
    'data': [
        'views/purchase_order.xml',
    ],
    'images': [
        'static/description/banner.gif',
        'static/description/main_screenshot.gif',
        'static/description/corebpo_logo.png',
        'static/description/corebpo_logo_screenshot.png',
        'static/description/purchase_order_menu.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
