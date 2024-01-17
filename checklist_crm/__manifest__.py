# -*- coding: utf-8 -*-
##############################################################################
##############################################################################
{
        'name': 'CRM Checklist',
        'version': '0.1',
        'category': 'crm',
        'license': 'OPL-1',
        'price': 49.00,
        'images': ['static/description/check007.PNG'],
        'author': 'oranga',
        'currency': 'EUR',
        'summary': 'CRM Checklist, Checklist Template, Checklist Points',
        'description': """
        CRM Checklist, 
        Checklist Template, 
        CRM Checklist Points
        Sales Checklist
    """,
    'depends': [
        'base',
        'crm',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/report_checklist_view.xml',
        'views/crm_checklist_view.xml',
    ],

    'installable': True,
    'application': True,
}