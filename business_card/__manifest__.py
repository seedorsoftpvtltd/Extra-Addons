# Part of Abdallah Mohammed (<abdalla_mohammed@outlook.com>). See LICENSE file for full copyright and licensing details.

{
    'name': 'Business Card for Odoo Online',
    'version': '14.0.1.0',
    'author': 'Abdallah Mohamed',
    'license': 'OPL-1',
    'category': 'CRM',
    'price': 5.0,
    'currency': 'EUR',
    'website': 'https://www.abdalla.work/r/1AQ',
    'description': ''' 
This module add feature in Partner form to save multi business card.
  ''',
    'depends': ['contacts'],
    'data': [
        'models/ir_model.xml',
        'models/ir_model_fields.xml',
        'security/ir_model_access.xml',
        'views/ir_actions_act_window.xml',
        'views/ir_ui_view.xml',
    ],
    'installable': True,

}
