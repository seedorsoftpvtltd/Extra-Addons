# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt. Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': "Whatsapp Integration For Payslip",
    'version': '1.0.2',
    'license': 'Other proprietary',
    'price': 29.0,
    'currency': 'EUR',
    'summary':  """Used to send payslip of employees through whatsapp""",
    'description': """
Used to send payslip of employees through whatsapp.
    """,
    'author': "Fousia Banu A R",
    'website': "http://www.seedorsoft.com",
    'support': 'support@seedorsoft.com',
    'images': ['static/description/image.png'],

    'depends': ['hr_payroll_community'],
    'data': [

            'views/whatsapp_payslip.xml',
            'wizard/wizard_whatsapp_payslip.xml',
            'security/ir.model.access.csv',
            ],
    'installable': True,
    'application': False,
}