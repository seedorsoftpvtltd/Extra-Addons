# -*- encoding: UTF-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2015-Today Laxicon Solution.
#    (<http://laxicon.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    tds_active = fields.Boolean(compute='get_tds_active')
    tds_value = fields.Float(string='TDS amount', compute="_amount_all")
    tds_per = fields.Float(string='TDS %', track_visibility='always', compute="compute_tds_per")
    force_tds = fields.Boolean(string="Apply Any way", states={'draft': [('readonly', False)]})

    valid_tds = fields.Boolean(string="TDS Applicable ?")
    tds_id = fields.Many2one('account.tds.tds', string="TDS section", states={'draft': [('readonly', False)]})
    tds_type = fields.Selection([('huf', 'Ind/Huf'), ('other', 'Other')], string="TDS type", states={'draft': [('readonly', False)]})
    nature = fields.Char(related='tds_id.nature', string="Payment Nature")
    threshold_amt = fields.Float(related='tds_id.threshold_amt', string="Threshold Amount")
    tax_w_wo = fields.Selection(related='tds_id.tax_w_wo',  string="Amount Type")
    tra_type = fields.Selection(related='tds_id.tra_type', string="Transaction Type")
    ind_huf_tds_per = fields.Float(related='tds_id.ind_huf_tds_per', string="TDS %")
    other_tds_per = fields.Float(related='tds_id.other_tds_per', string="Other TDS %")
    tds_account_id = fields.Many2one(related="tds_id.account_id", string='TDS Account')
    pan = fields.Char(string='PAN Number', states={'draft': [('readonly', False)]})

    @api.depends('order_line.price_total')
    def _amount_all(self):
        super(PurchaseOrder, self)._amount_all()
        for order in self:
            amount_untaxed = amount_tax = 0.0
            order.tds_value = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })
            if order.tds_active and order.tds_per > 0:
                tds_value = (order.amount_untaxed * order.tds_per) / 100
                order.update({
                            'amount_untaxed': order.currency_id.round(amount_untaxed),
                            'amount_tax': order.currency_id.round(amount_tax),
                            'tds_value': tds_value,
                            'amount_total': amount_untaxed + amount_tax - tds_value,
                        })

    def get_tds_active(self):
        for i in self:
            i.tds_active = self.env.user.company_id.tds_active

    @api.onchange('partner_id')
    def onchnage_partner_id_tds(self):
        self.clear_tds_data()
        if self.partner_id and self.partner_id.valid_tds and self.partner_id.tds_id:
            self.valid_tds = self.partner_id.valid_tds
            self.tds_id = self.partner_id.tds_id.id
            self.tds_type = self.partner_id.tds_type
            self.nature = self.partner_id.tds_id.nature
            self.threshold_amt = self.partner_id.tds_id.threshold_amt
            self.tax_w_wo = self.partner_id.tds_id.tax_w_wo
            self.tra_type = self.partner_id.tds_id.tra_type
            self.ind_huf_tds_per = self.partner_id.tds_id.ind_huf_tds_per
            self.other_tds_per = self.partner_id.tds_id.other_tds_per
            self.tds_account_id = self.tds_id.account_id.id
            self.pan = self.partner_id.pan
            if self.partner_id.pan:
                self.tds_type = self.partner_id.check_pan_detail()

    def clear_tds_data(self):
        self.tds_id = False
        self.valid_tds = False
        self.tds_type = ''
        self.nature = ""
        self.threshold_amt = 0.0
        self.tax_w_wo = ''
        self.tra_type = 0.0
        self.ind_huf_tds_per = 0.0
        self.other_tds_per = 0.0
        self.tds_account_id = False
        self.pan = ''

    @api.depends('partner_id', 'tds_id', 'tds_active')
    def compute_tds_per(self):
        for res in self:
            res.tds_per = 0.0
            if res.partner_id and res.tds_active and res.partner_id.valid_tds and res.tds_id:
                domain = [('state', 'not in', ['cancel'])]
                amt = 0.0
                tax = 0.0
                f_amt = 0.0
                if res.tds_id.tra_type == 'single':
                    amt = sum(line.price_subtotal for line in res.order_line)
                    # tax = sum(line.amount for line in res.tax_line_ids)
                elif res.tds_id.tra_type == 'year':
                    domain.append(('invoice_date', '>=', res.tds_id.f_start_date))
                    domain.append(('invoice_date', '<=', res.tds_id.f_end_date))
                    inv_ids = self.search(domain)
                    for inv in inv_ids:
                        amt += sum(line.price_subtotal for line in inv.order_line)
                        # tax += sum(line.amount for line in inv.tax_line_ids)
                if res.tds_id.tax_w_wo == 'w_tax':
                    f_amt = amt + tax
                elif res.tds_id.tax_w_wo == 'wo_tax':
                    f_amt = amt
                if res.partner_id.pan:
                    res.tds_type = res.partner_id.check_pan_detail()
                if f_amt > res.tds_id.threshold_amt:
                    if res.tds_type == 'huf':
                        res.tds_per = res.ind_huf_tds_per or 0.0
                    elif res.tds_type == 'other':
                        res.tds_per = res.other_tds_per or 0.0
                elif res.force_tds:
                    if res.tds_type == 'huf':
                        res.tds_per = res.ind_huf_tds_per or 0.0
                    elif res.tds_type == 'other':
                        res.tds_per = res.other_tds_per or 0.0
