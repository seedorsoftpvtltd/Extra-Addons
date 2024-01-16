# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-Today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
import datetime

#Class Created For Add New Funcationality Of Send Email Of Daily Timesheet Report
class SendTimesheet(models.TransientModel):
    _name = 'send.timesheet'
    _description = 'Send Timesheet'

    next_step = fields.Char("Next Step", help="The Next Step From Current Position")
    email_to_ = fields.Many2many('res.partner', string="Email to", help="The List Of User Whom You Want To Send The Mail")

    def send_status_report(self):

        if self.env.context.get('active_model')=='hr.employee':
            employee = self.env.context.get('active_id')
            employee_id = self.env['hr.employee'].search([('id','=',employee)])
        
        email_subject = "Status Upadte from " + employee_id.name + " on " + str(datetime.date.today())
        email_to = []
        for recipient in self.email_to_:
           email_to.append(recipient.id)
        
        analytic_lines = employee_id.env['account.analytic.line'].search([('user_id', '=', employee_id.user_id.id),('date','=',datetime.date.today())])

        if self.next_step:
            next_step = self.next_step
        else:
            next_step = ""

        if analytic_lines:
            task_unit_amount = 0.00
            task_description = ""
            total_hours = "" 
                
            for line in analytic_lines:

                if ((line.unit_amount * 60) % 60) <= 9:
                    task_hours = str(int(line.unit_amount)) + " : 0" + str(int((line.unit_amount * 60) % 60))
                else:
                    task_hours = str(int(line.unit_amount)) + " : " + str(int((line.unit_amount * 60) % 60))

                task_unit_amount += (line.unit_amount)
                if ((task_unit_amount * 60) % 60) <= 9:
                    total_hours = str(int(task_unit_amount)) + " : " + "0" + str(int((task_unit_amount * 60) % 60))
                else:
                    total_hours = str(int(task_unit_amount)) + " : " + str(int((task_unit_amount * 60) % 60))

                task_description += "<tr>   <td  align=""center""> <font size=""2"">{0}</font></td>    <td  align=""center""> <font size=""2"">{1}</font></td>   <td  align=""center""> <font size=""2"">{2}</font></td>    <td  align=""center""> <font size=""2"">{3}</font></td>    </tr>".format(str(line.date), str(line.name), str(line.project_id.name), task_hours)
            
            status_table = " <font size=""2"">   <p> Hello, </p>    <p> Today’s status update report: </p>    <table style=""width:80%"" border="" 1px solid black""> <tr> <th align=""center""><font size=""2"">Date</font> </th>    <th align=""center""><font size=""2""> Description</font> </th>    <th align=""center""><font size=""2"">Project</font> </th>    <th align=""center""><font size=""2""> Duration </font> </th>    </tr>{0}     <tr> <td colspan=""3"" align=""right""><font size=""2""> Total </font></td>    <td  align=""center""><font size=""2""> {1} </font> </td>   </table> <p>Next Step:  {3}</p>      <p>Regards,</p>    <p> {2} </p>    </font>".format(task_description, total_hours, employee_id.name, next_step) 
            if email_to:
                mail={
                      'subject'       : email_subject,
                      'email_from'    : employee_id.name,
                      'recipient_ids' : [(6, 0, email_to)],
                      'body_html'     : status_table
                     }
                mail_create = employee_id.env['mail.mail'].create(mail)
                if mail_create:
                    mail_create.send()
            else:
                raise ValidationError(_('Please,Add Recipient.'))
 
        else:
            raise ValidationError(_('There is no any timesheets available for today.'))


