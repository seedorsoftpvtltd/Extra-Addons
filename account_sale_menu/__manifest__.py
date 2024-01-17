# pylint: disable=missing-docstring,manifest-required-author
{
    'name': 'Sales Menu in Accounting',
    'summary': 'Appear confirmed sale orders under accounting',
    'author': 'CORE B.P.O',
    'maintainer': 'Abdalla Mohamed',
    'website': 'http://www.core-bpo.com',
    'version': '13.0.1.0.0',
    'category': 'Accounting/Accounting',
    'license': 'OPL-1',
    'depends': [
        'sale',
    ],
    'data': [
        'views/sale_order.xml',
    ],
    'images': [
        'static/description/banner.gif',
        'static/description/main_screenshot.gif',
        'static/description/corebpo_logo.png',
        'static/description/corebpo_logo_screenshot.png',
        'static/description/sale_order_menu.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
