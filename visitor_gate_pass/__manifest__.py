# -*- coding: utf-8 -*-
{
    'name': "Gate Pass for Visitors",
    'version': '2.3',
    'price': 9.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'category': 'Human Resources/Employees',
    'summary': """Visitor / Guest Gate Pass""",
    'description': """
Company Visitors Gate Passes.
company visitor
visitor process 
visitor pass
visitor report
company visit
employee visitors
odoo visitor
visit company
pass print
gate pass
company gate pass
visitor pass company
delivery gate pass

    """,
    'author': "Probuse Consulting Service Pvt. Ltd.",
    'website': 'www.probuse.com',
    'images': ['static/description/gate_pass.jpg'],
    'live_test_url': 'http://probuseappdemo.com/probuse_apps/visitor_gate_pass/451',#'https://youtu.be/lJXs9-QWJkE',
    'depends': ['hr'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/gate_visitor_sequence.xml',
        'views/visitor_gate_pass_view.xml',
        'report/gate_visitor_report.xml',
    ],
    'installable': True,
    'application': False,
}
