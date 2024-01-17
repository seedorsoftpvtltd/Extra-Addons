    # -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#   Copyright (C) 2016-today Geminate Consultancy Services (<http://geminatecs.com>).
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
{
    'name': 'Chatter Message Visibility',
    "version" : "13.0.0.1",
    'category': 'Web',
    'summary': "Geminate comes with a feature to show / hide 'Messages', 'Log Notes' and 'Activities' from chatter on formview.",
    'website': 'www.geminatecs.com',
    'author' : 'Geminate Consultancy Services',
    'license': 'Other proprietary',
    'depends': ['mail','web','base'],
    "description": """
       Geminate comes with a feature to show / hide 'Messages', 'Log Notes' and 'Activities' from chatter
       on formview. you will get a complete separated list of all the messages, log notes and activities
       from chatter on formview.Benefit of this feature is that you can easily get a separate list of the 
       all the messages, log notes and activities from chatter on formview.Additionally it can Load messages,
       log notes and activities from chatter with automatic refresh of formview.
    """,
    'data': [
                'security/ir.model.access.csv',
                'data/cron.xml',
                'views/assets.xml',
                'views/mail_message_subtype.xml',
             ],
    'images': ['static/description/poster.png'],
    'qweb' : [],
    'installable': True,
    'auto_install': False,
    'application': False,
    "price": 54.99,
    "currency": "EUR"
}
