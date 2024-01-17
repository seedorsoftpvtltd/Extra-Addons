# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    line_id = fields.Many2one('account.analytic.account', 'Analytic Line')
    sale_order_line = fields.Many2one('account.analytic.account', 'Sale Order Line')


class SaleOrder(models.Model):
    _inherit = "sale.order"

    recuring_period = fields.Char(string='Recuring Period')

    def _prepare_analytic_account_data(self):
        name = self.name + '-' + self.partner_id.name
        return {
            'name': name,
            'code': self.client_order_ref,
            'company_id': self.company_id.id,
            'partner_id': self.partner_id.id,
            'recuring_period':self.recuring_period,
            'start_contract_date': fields.Date.today(),
            'end_contract_date':self.validity_date or '2022-05-01',
        }

    def _create_analytic_account(self, prefix=None):
        res = {}
        analytic_account = self.env['account.analytic.account'].create(self._prepare_analytic_account_data())
        product_contract_id = self.order_line.product_id.search([('id','in',self.order_line.product_id.ids),('contract_warranty','=', True)])
        get_contact_line = self.order_line.search([('product_id.id','in', product_contract_id.ids),('id','in', self.order_line.ids)])
        product_without_contract_id = self.order_line.product_id.search([('id','in',self.order_line.product_id.ids),('contract_warranty','=', False)])
        get_order_line = self.order_line.search([('product_id.id','in', product_without_contract_id.ids),('id','in', self.order_line.ids)])
        analytic_account.update({
            'contact_line': [(6, 0, get_contact_line.ids)],
            'order_line_ids': [(6, 0, get_order_line.ids)],
        })
        analytic_account.state = 'new'
        self.write({'analytic_account_id': analytic_account.id})
        res[self.id] = analytic_account
        return res

    def _update_exist_analytic_account(self, analytic):
        res = {}
        line_list = []
        order_list = []
        for line in analytic.contact_line:
            line_list.append(line.product_id.id)
        for o_line in self.order_line:
            order_list.append(o_line.product_id.id)
        c_product = [pr for pr in order_list if not pr in line_list]
        get_contract_diff_prdct = self.order_line.search([('product_id.id','in',c_product),('product_id.contract_warranty','=', True),('id','in', self.order_line.ids)])
        get_order_diff_prdct = self.order_line.search([('product_id.id','in',c_product),('product_id.contract_warranty','=', False),('id','in', self.order_line.ids)])
        
        if get_contract_diff_prdct :
            for data in get_contract_diff_prdct:
                analytic.update({
                    'contact_line': [(4, data.id)],        
                })  
        if get_order_diff_prdct :
            for data in get_order_diff_prdct:
                analytic.update({
                    'order_line_ids': [(4, data.id)],        
                })
        analytic.state = 'running' 
        res[self.id] = analytic
        return res

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        exist_analytic = self.env['account.analytic.account'].sudo().search([('partner_id.id','=',self.partner_id.id)])
        for rec in exist_analytic:
            self.write({'analytic_account_id': rec.id})
            if exist_analytic:
                self._update_exist_analytic_account(self.analytic_account_id)
            if not self.analytic_account_id:
                self._create_analytic_account()
        return res
