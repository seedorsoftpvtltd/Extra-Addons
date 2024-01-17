# -*- coding: utf-8 -*-
###################################################################################
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

{
    'name': "Attendance Mail for hr,manager",
    'version': "13.0.1.0.0",
    'author': 'Poovarasan',
    'company': 'Seedorsoft Private Limited',
    'website': 'https://www.seedorsoft.com',
    'summary': '''Automatically send email for hr,manager''',
    'description': '''Automatically send email for hr,manager.
                      Configuration:
                          1. Kindly fill the fields Manager,HR employee and also enable Emp Remainder field.''',
    'category': "hr",
    'depends': ['web','mail','hr'],
    'license': 'AGPL-3',
    'data': [
            'views/attendance_mail_hr_reminder.xml',            
            'data/attendance_mail_hr_action_data.xml',
            'data/attendance_mail_manager_action_data.xml',
            'views/attend_hr_inh_view.xml'
             ],
    'demo': [],
#    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False
}
