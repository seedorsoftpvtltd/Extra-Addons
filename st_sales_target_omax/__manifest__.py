# -*- coding: utf-8 -*-
{
    "name":"Sales Target Management for SalesTeam",
    "author": "OMAX Informatics",
    "version": "13.0.1.0",
    "website": "https://www.omaxinformatics.com",
    "category": "Sales/Sales,Accounting/Accounting",
    'summary': """
        Sales Target Based Sales Person,
        Sales Target for Salesman,
        Sale Target,
        Sales Target,
        Sales Target & Achivement,
        Sales Target and Achivement,
        Sales Target Management,
        Sale Target Management,
        Sales Target For Sales Person
        Sales Target For Salesman
        Sale Target For Sales Person
        Sale Target For Salesman,
        Sales Person Target,
        Salesperson Target,
        Salesman Target,
        Sales Target,
        Sale Target,
        Sales Target Management,
        Sale Target Management,
        Sales Target Based Sales Team,
        Sales Target for SalesTeam,
        Sales Target For Sales Team
        Sales Target For Salesteam
        Sale Target For Sales Team
        Sale Target For Salesteam,
        Sales Team Target,
        SalesTeam Target,
        SalesTeam Target,
        Sales Team Sales Target,
        SalesTeam Sales Target,
        Sales Team Sale Target,
        SalesTeam Sale Target,
    """,
    'description': """
        This Odoo apps helps to manage sales target for sales team. User can set the target for sales team for a specific period and also send email to resposible with targeted details. You can set sales target based on specific date internal which helps to generate sales target for monthly, quarterly or for specific date period. We have provided option to achieve target based on sales order confirmation and while invoice is paid.  
    """,
    "depends": ["sale","sale_management","sales_team","account"],
    "data": [
        "security/target_security.xml",
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/mail_template_data.xml",
        "views/sales_target_view.xml",
    ],
    'demo': [],
    'test':[],
    "images": ["static/description/banner.jpg"],
    'license': 'AGPL-3',
    'currency':'USD',
    'price': 45.0,
    'installable' : True,
    "auto_install" : False,
    "application" : True,
}
