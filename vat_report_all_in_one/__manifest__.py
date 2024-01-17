{
    'name': 'All in one VAT reports',
    'version': '13.0.5',
    'category': 'Accounting',
    'summary': 'Extend the function of Odoo VAT return and addition of new VAT report',
    
    'author': 'TeamUp4Solutions, TaxDotCom',
    'website': 'http://taxdotcom.org/',
    'maintainer': 'Muhammad Younis, Sohail Ahmad',
    
    'depends': ['account'],
    'data': [
        'views/tax_payment_adjustment.xml',
        'reports/vat_report_wizard.xml',
        'views/account.xml',
        'views/account_tax.xml',
        'views/account_move.xml',
    ],
    'installable': True,
    'auto_install': False,
    'price': 80.00,
    'currency': 'EUR',
    'images': ['static/description/image.jpeg'],
    'license': 'OPL-1',
}
