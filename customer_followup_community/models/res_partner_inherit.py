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
from datetime import date
from odoo import fields, models, api


class CustomerFollowPartner(models.Model):
    _inherit = 'res.partner'

    today = date.today()
    invoice_list = fields.One2many('account.move', 'partner_id',
                                   string="Invoice Details",
                                   readonly=True,
                                   domain=([('invoice_payment_state', '=', 'not_paid'),
                                            ('type', '=', 'out_invoice'),
                                            ('state', '=', 'posted')]))
    customer_followup_done = fields.Many2one('followup.line', string='Action Taken')
    customer_followup_to_do = fields.Many2one('followup.line', string='Next Action')
    next_followup_action_date = fields.Char(string='Next Action Date')

    def get_min_date(self):
        for this in self:
            if this.invoice_list:
                min_list = this.invoice_list.mapped('invoice_date_due')
                return min(min_list)

    def send_inv(self):
        template = self.env.ref('customer_followup_community.mail_template_data_follow_cust_test')
        ctx = {
            'default_model': 'res.partner',
            'default_template_id': template.id,
            'default_partner_ids': [self.id],
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'target': 'new',
            'context': ctx,
        }

    def print_followup_letter(self):
        return self.env.ref('customer_followup_community.action_report_followup_community').report_action(self, data='')


class CustomerFollowupCommunity(models.AbstractModel):
    _name = 'report.customer_followup_community.report_followup_template'

    @api.model
    def _get_report_values(self, docids, data):
        self.model = self.env.context.get('active_model')
        docs = self.env.context.get('active_ids')
        if docs == None:
            docs = docids
        return {
            'data': self.env['res.partner'].search([('id', 'in', docs)])
        }


class CustomerFollowupCommunityCron(models.AbstractModel):
    _name = 'report.customer_followup_community.report_followup_all'

    @api.model
    def _get_report_values(self, docids, data):
        docs = self.env.context.get('active_ids')
        if docs == None:
            docs = docids
        values = self.env['res.partner'].search([('id', 'in', docs)])
        if values:
            return {
                'data': self.env['res.partner'].search([('id', 'in', docs)])}
