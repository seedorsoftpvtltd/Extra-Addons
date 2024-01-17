# -*- coding: utf-8 -*-
{
    'name': "vamk work sheet Report",

    'summary': """
        Print vamk work sheet""",

    'description': """
        vamk work sheet

     configurations:
     1)cleaning and fitting - CF
     2)Juice making - JM
     3)Measuring - MSR
     4)Cleaning Circulation - CC
     5)Initial Heating - IH
     6)sugar addition and heating - SAH
     7)Cooling filteration and water addition - CFWA
     8)Brix settings -BS
     9)Homogenesing - HMG
     10)Pasteurising - PSG
     11)Filling -FIG
     12)Bottle Checking - BC
     13)Label Pasting - LP
     14)Data Coding - DC
     15) Packing - PCKG 

    """,

    'author': "Poovarasan",
    'website': "http://banibro.com/",
    'company': 'banibro',
    'category': 'MRP',
    'version': '13.0.1',
    'depends': ['mrp','hr','mrp_request_field','mrp_production_request'],
    'license': 'AGPL-3',

    'data': [
        'security/ir.model.access.csv',
        'views/vamk_views.xml',
        'views/vamk_templates.xml',
        'views/vamk_report_views.xml',
    ],
    "application": True,
    "installable": True,
}
