{
    "name": "Odoo debrand",
    "version": "13.0.9.4",
    "category": "Marketing",
    'summary': 'Integrate & Manage MailChimp Operations from Seedor',

    "depends": ["mailchimp"],

    'data': [
        'views/mailchimp_accounts_view.xml',
        'views/mailchimp_lists_view.xml',
    ],

    "author": "sujith",
    'auto_install': False,
    "installable": True,
    'application': True,
}
