# -*- coding: utf-8 -*-
##############################################################################
#
#    Global Creative Concepts Tech Co Ltd.
#    Copyright (C) 2018-TODAY iWesabe (<http://www.iwesabe.com>).
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Sequence in Project Tasks',
    'version': '1.0',
    'author': 'iWesabe',
    'summary': 'Shows Sequence in Project Tasks',
    'description': """This module shows sequence in project tasks""",
    'category': 'Base',
    'website': 'https://www.iwesabe.com/',
    'license': 'AGPL-3',
    'depends': ['project'],
    'data': [
        'data/ir_sequence_data.xml',
        'views/project_task_views.xml',
    ],
    'qweb': [],
    'images': ['static/description/iWesabe-Sequence-Project-Task.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
