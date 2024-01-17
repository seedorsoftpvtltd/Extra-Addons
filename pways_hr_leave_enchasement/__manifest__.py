# -*- coding: utf-8 -*-
{
    'name': "Hr Enchasement",
    'summary': "Hr Enchasement",
    'description': """Hr Enchasement""",
    'category': 'HR',
    'version': '13.0.0',
    'author' : 'Preciseways',
    'website': "http://www.preciseways.com",
    'depends': ['hr', 'hr_contract', 'account'],
    'data': [
            'security/ir.model.access.csv',
            'data/data.xml',
            'views/hr_contract.xml',             
            'views/hr_enchasement.xml',             
             ],

    'installable': True,
    'application': True,
    'price': 15.0,
    'currency': 'EUR',
    'images':['static/description/banner.png'],
    'license': 'OPL-1',
}
