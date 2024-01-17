# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from datetime import date

class SalesTeamTarget(models.Model):
    _name = "sales.team.target"
    _description = "Sales Team SalesTarget"
    _inherit = ['mail.thread']
    _order = "name"
    
    
    @api.depends('salesteam_id', 'start_date', 'end_date','state')
    def _get_sales_order(self):
        for record in self:
            related_ids = []
            if record.salesteam_id and record.start_date and record.end_date and record.state in ['open','closed']:
                order_ids = self.env["sale.order"].search([
                    ('team_id', '=',record.salesteam_id.id),
                    ('company_id', '=', record.company_id.id),
                    ('date_order','>=', record.start_date),
                    ('date_order','<=', record.end_date),('state','in', ('sale','done'))])
                record.sale_order_ids = order_ids
            else:
                record.sale_order_ids = False
        
    @api.depends('salesteam_id', 'start_date', 'end_date','state')
    def _get_invoices(self):
        for record in self:
            related_ids = []
            if record.salesteam_id and record.start_date and record.end_date and record.state in ['open','closed']:
                move_ids = self.env["account.move"].search([
                    ('team_id', '=',record.salesteam_id.id),
                    ('company_id', '=', record.company_id.id),
                    ('invoice_date','>=', record.start_date),
                    ('invoice_date','<=', record.end_date),('state','=', 'posted'),('type', '=', 'out_invoice')])
                record.move_ids = move_ids
            else:
                record.move_ids = False
            
    @api.depends('sale_order_ids','move_ids','target_point')
    def _compute_target_amount(self):
        for record in self:
            if record.target_point == 'sale_confirm':
                amount_achive = amount_diff = amount_achive_per = 0.0
                for order in record.sale_order_ids:
                    amount_achive += order.amount_total
                
                amount_diff = amount_achive - record.target_amount
                if record.target_amount > 0:
                    amount_achive_per = ((amount_achive * 100) / record.target_amount)
                
                record.update({
                    'achivement_amount': amount_achive,
                    'difference_amount': amount_diff,
                    'achivement_per': amount_achive_per,
                })
            
            if record.target_point in ['invoice_paid','invoice_validate']:
                amount_achive = amount_diff = amount_achive_per = 0.0
                for move in record.move_ids:
                    if record.target_point == 'invoice_validate':
                        amount_achive += move.amount_total
                    if record.target_point == 'invoice_paid':
                        if move.amount_residual <= 0:
                            amount_achive += move.amount_total
                        else:
                            amount_achive += (move.amount_total - move.amount_residual)
                
                amount_diff = amount_achive - record.target_amount
                if record.target_amount > 0:
                    amount_achive_per = ((amount_achive * 100) / record.target_amount)
                
                record.update({
                    'achivement_amount': amount_achive,
                    'difference_amount': amount_diff,
                    'achivement_per': amount_achive_per,
                })
    
    @api.onchange('salesteam_id') 
    def _onchange_salesteam_id(self):
        if self.salesteam_id.user_id:
            self.update({'responsible_id': self.salesteam_id.user_id.id})
        else:
            self.update({'responsible_id': False})
    
    
    name = fields.Char(string='Target Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    state = fields.Selection(selection=[
            ('draft', 'Draft'),
            ('open', 'Open'),
            ('closed', 'Closed'),
            ('cancel', 'Cancelled'),
        ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')
    salesteam_id = fields.Many2one('crm.team', string='Sales Team', required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    responsible_id = fields.Many2one('res.users', string='Responsible(Team Leader)', required=True)
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.company, index=True)
    
    target_point = fields.Selection([
        ('sale_confirm', 'Sale Order Confirm'),
        ('invoice_paid', 'Invoice Paid'),
        ('invoice_validate', 'Invoice Validate')
        ], default='sale_confirm', string='Target Point')
    
    target_amount = fields.Float('Target')
    achivement_amount = fields.Float(string='Achivement', readonly=True, compute='_compute_target_amount')
    difference_amount = fields.Float(string='Difference', readonly=True, compute='_compute_target_amount')
    achivement_per = fields.Float(string='Achivement Percentage', readonly=True, compute='_compute_target_amount')
    
    sale_order_ids = fields.One2many('sale.order',compute='_get_sales_order', string='Sale Orders')
    move_ids = fields.One2many('account.move',compute='_get_invoices', string='Invoice')
    
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('sales.team.target') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('sales.team.target') or _('New')
        result = super(SalesTeamTarget, self).create(vals)
        if result.target_amount <= 0:
            raise UserError(_('Target must be grater than 0.'))
        return result
        
    def action_confirm(self):
        mail_template = self.env.ref('st_sales_target_omax.mail_template_salesteam_target_confirm_data')
        mail_template.send_mail(self.id, force_send=True)
        return self.write({'state': 'open'})
        
    def action_close(self):
        today = date.today()
        if self.end_date >= today:
            raise UserError(_('You can close after Target End Date'))
        mail_template = self.env.ref('st_sales_target_omax.mail_template_salesteam_target_closed_data')
        mail_template.send_mail(self.id, force_send=True)
        return self.write({'state': 'closed'})
        
    def action_calcel(self):
        return self.write({'state': 'cancel'})
        
    def action_send_mail(self):
        self.ensure_one()
        template_id = False
        if self.env.ref('st_sales_target_omax.mail_template_salesteam_target_data'):
            template_id = self.env.ref('st_sales_target_omax.mail_template_salesteam_target_data').id
        else:
            template_id = self.env['ir.model.data']._xmlid_to_res_id('st_sales_target_omax.mail_template_salesteam_target_data', raise_if_not_found=False)
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_template(template.lang, 'sales.team.target', self.ids[0])
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'sales.team.target',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
        })
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
