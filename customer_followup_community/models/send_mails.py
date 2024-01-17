# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Technologies(odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################
from datetime import date, timedelta
from odoo import fields, models, api


class CustomerFollowWizard(models.TransientModel):
    _name = 'followup.mails'

    email_count_value = fields.Char()

    def get_delay(self):
        delay = """select id,delay from followup_line where followup_id =
        (select id from account_followup where company_id = %s)
         order by delay limit 1"""
        self._cr.execute(delay, [self.env.user.company_id.id])
        record = self.env.cr.dictfetchall()
        return record

    def followp_wizard(self):
        return {
            'name': 'Send Overdue Emails',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'followup.mails',
            'target': 'new',
        }

    def send_followup_mail(self):
        count = 0
        lines = self.env['followup.line'].search([(
            'followup_id.company_id', '=', self.env.user.company_id.id)])
        if lines:
            for i in self.env['res.partner'].search([('invoice_list', '!=', False)]):
                if i.invoice_list:
                    if not i.customer_followup_to_do and i.customer_followup_done:
                        continue
                    else:
                        if not i.customer_followup_to_do:
                            record = self.get_delay()
                            i.customer_followup_to_do = self.env['followup.line'].browse(record[0]['id'])
                            if i.customer_followup_to_do.days_hours == 'days':
                                date_min = i.get_min_date() + timedelta(days=i.customer_followup_to_do.delay)
                            else:
                                date_min = i.get_min_date() + timedelta(hours=i.customer_followup_to_do.delay)
                            i.next_followup_action_date = str(date_min).split()[0]
                        date_min = i.next_followup_action_date
                        action_date = date.today()
                        if str(action_date) >= str(date_min):
                            # followup date
                            list = lines.mapped('delay')
                            i.customer_followup_done = i.customer_followup_to_do
                            # next action date
                            if len(list) > list.index(i.customer_followup_done.delay) + 1:
                                next_delay = list[list.index(i.customer_followup_done.delay) + 1]
                                next_id = self.env['followup.line'].search([('delay', '=', next_delay)]).id
                                i.customer_followup_to_do = self.env['followup.line'].browse(next_id)
                                if i.customer_followup_to_do.days_hours == 'days':
                                    date_min = i.get_min_date() + timedelta(
                                        days=i.customer_followup_to_do.delay)
                                else:
                                    date_min = i.get_min_date() + timedelta(
                                        hours=i.customer_followup_to_do.delay)
                                i.next_followup_action_date = str(date_min).split()[0]
                            #     .......
                            else:
                                # action completed
                                i.customer_followup_to_do = False
                                i.next_followup_action_date = False
                            if i.customer_followup_done.after_before == 'before':
                                template = self.env.ref(
                                    'customer_followup_community.before_due_date_mail_template_followup')
                            else:
                                template = self.env.ref(
                                    'customer_followup_community.after_due_date_mail_template_followup')
                            self.env['mail.template'].browse(template.id).sudo(self.env.user.id).send_mail(i.id)
                            count += 1
                else:
                    i.next_followup_action_date = False
                    i.customer_followup_to_do = False
                    i.customer_followup_done = False
        self.email_count_value = count
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'followup.mails',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def send_followup_mail_cron(self):

        count = 0
        lines = self.env['followup.line'].search([])
        if lines:
            for i in self.env['res.partner'].search([('invoice_list', '!=', False)]):
                if i.invoice_list:
                    if not i.customer_followup_to_do and i.customer_followup_done:
                        continue
                    else:
                        if not i.customer_followup_to_do:
                            record = self.get_delay()
                            i.customer_followup_to_do = self.env['followup.line'].browse(record[0]['id'])
                            if i.customer_followup_to_do.days_hours == 'days':
                                date_min = i.get_min_date() + timedelta(days=i.customer_followup_to_do.delay)
                            else:
                                date_min = i.get_min_date() + timedelta(hours=i.customer_followup_to_do.delay)
                            i.next_followup_action_date = str(date_min).split()[0]
                        date_min = i.next_followup_action_date
                        action_date = date.today()
                        if str(action_date) >= str(date_min):
                            # followup date
                            list = lines.mapped('delay')
                            i.customer_followup_done = i.customer_followup_to_do
                            # next action date
                            if len(list) > list.index(i.customer_followup_done.delay) + 1:
                                next_delay = list[list.index(i.customer_followup_done.delay) + 1]
                                next_id = self.env['followup.line'].search([('delay', '=', next_delay)]).id
                                i.customer_followup_to_do = self.env['followup.line'].browse(next_id)
                                if i.customer_followup_to_do.days_hours == 'days':
                                    date_min = i.get_min_date() + timedelta(
                                        days=i.customer_followup_to_do.delay)
                                else:
                                    date_min = i.get_min_date() + timedelta(
                                        hours=i.customer_followup_to_do.delay)
                                i.next_followup_action_date = str(date_min).split()[0]
                            #     .......
                            else:
                                # action completed
                                i.customer_followup_to_do = False
                                i.next_followup_action_date = False
                            if i.customer_followup_done.after_before == 'before':
                                template = self.env.ref(
                                    'customer_followup_community.before_due_date_mail_template_followup')
                            else:
                                template = self.env.ref(
                                    'customer_followup_community.after_due_date_mail_template_followup')
                            self.env['mail.template'].browse(template.id).sudo(self.env.user.id).send_mail(i.id)
                            count += 1
                else:
                    i.next_followup_action_date = False
                    i.customer_followup_to_do = False
                    i.customer_followup_done = False
        self.email_count_value = count
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'followup.mails',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def print_all_letter(self):
        return self.env.ref('customer_followup_community.action_report').report_action(self, data='')


class CustomerFollowupPrintAll(models.AbstractModel):
    _name = 'report.customer_followup_community.report'

    @api.model
    def _get_report_values(self, docids, data):
        today = date.today()
        ids = []
        for line in self.env['res.partner'].search([]):
            check_partner = line.invoice_list.filtered((lambda t: t.partner_id.id == line.id))
            if check_partner:
                ids.append(line.id)
        partner_ids = self.env['res.partner'].browse(ids)

        return {
            'today': today,
            'partner': partner_ids
        }
