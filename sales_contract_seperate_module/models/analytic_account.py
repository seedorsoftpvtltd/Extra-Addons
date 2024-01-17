# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime
import calendar as cal

class AccountAnalytic(models.Model):

    _inherit = "account.analytic.account"

    @api.depends('contact_line.price_total')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.contact_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })

    @api.depends('order_line_ids.price_total')
    def _amount_order_all(self):
        for order in self:
            amount_line_untaxed = amount_line_tax = 0.0
            for line in order.order_line_ids:
                amount_line_untaxed += line.price_subtotal
                amount_line_tax += line.price_tax
            order.update({
                'amount_line_untaxed': amount_line_untaxed,
                'amount_line_tax': amount_line_tax,
                'amount_line_total': amount_line_untaxed + amount_line_tax,
            })

    date_of_next_invoice = fields.Date(string="Date Of Next Invoice")
    recuring_period = fields.Char(string='Recuring Period')
    currency_id = fields.Many2one('res.currency', string='Order Currency')
    state=fields.Selection([
        ('new', 'New'),
        ('running', 'Running'),
        ('expires_soon', 'Expires Soon'),
        ('expired', 'Expired'),
        ('locked', 'Locked'),
    ], 'Status', readonly=True, store=True, tracking=True, default='new')
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', tracking=5)
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', tracking=4)
    amount_line_untaxed = fields.Monetary(string='Untaxed Order Amount', store=True, readonly=True, compute='_amount_order_all', tracking=5)
    amount_line_tax = fields.Monetary(string='Order Taxes', store=True, readonly=True, compute='_amount_order_all')
    amount_line_total = fields.Monetary(string='Amount Total', store=True, readonly=True, compute='_amount_order_all', tracking=4)
    order_line_ids = fields.One2many('sale.order.line', 'sale_order_line', string='Order Lines')
    contact_line = fields.One2many('sale.order.line', 'line_id', string='Contact Lines')
    start_contract_date = fields.Date('Start Date of Contract')
    end_contract_date  = fields.Date('End Date of Contract')
    remindar_days = fields.Char('Remindar Days For Expiration Contract', readonly=True)
    invoice_count = fields.Integer(string='Invoice Count', readonly=True)
    invoice_ids = fields.Many2many("account.move", string='Invoices', readonly=True, copy=False)
    description = fields.Html(string="Description")
    
    def create_invoices(self):
        invoice = self.env['account.move'].create({
            'partner_id':self.partner_id.id,
            'type': 'out_invoice',
            'invoice_date': fields.Date.today(),
            'company_id':self.company_id.id,
        })
        for data in self.contact_line:
            invoice.write({
                'invoice_line_ids': [(0, 0, {
                    'product_id': data.product_id.id,
                    'name':data.name,
                    'quantity':data.product_uom_qty,
                    'price_unit':data.price_unit,
                })],        
            })  
        self.write({'invoice_ids': invoice.ids})
        action = {
            'name': 'Draft Invoice',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'target': 'current',
            'flags': {'search_view': True, 'action_buttons': True},
            'domain': [('id', '=', self.invoice_ids.id)],
        }
        return action

    @api.onchange('end_contract_date')
    def onchange_exipry_date(self):
        for record in self:
            if record.end_contract_date != '':
                today = fields.Date.today()
                if record.end_contract_date == today:
                    record.state ='expired'
                else:
                    record.state = 'running'
                    if record.end_contract_date:
#                       assert isinstance(record.end_contract_date, datetime)
                       remindar = record.end_contract_date - today
                       day = str(remindar).split(' ')[0]
                       if int(day) <= 10:
                          record.state = 'expires_soon'
                          record.remindar_days = day + 'Days'
            
    def locked_account(self):
        self.state = 'locked'

    def unlock_account(self):
        self.state = 'running'

    @api.model
    def get_count_list(self):
        total_contract = self.env['account.analytic.account'].sudo().search_count([])
        new_contract = self.env['account.analytic.account'].sudo().search_count([('state','=','new')])
        running_contract = self.env['account.analytic.account'].sudo().search_count([('state','=','running')])
        expiry_soon_contract = self.env['account.analytic.account'].sudo().search_count([('state','=','expires_soon')])
        expired_contract = self.env['account.analytic.account'].sudo().search_count([('state','=','expired')])
        locked_contract = self.env['account.analytic.account'].sudo().search_count([('state','=','locked')])
        total_product = self.env['product.template'].sudo().search_count([('contract_warranty','=', True)])
        total_invoice = self.env['account.move'].sudo().search_count([])
        customer = self.env['account.analytic.account'].sudo().search([])
        total_customer = self.env['res.partner'].sudo().search_count([('id','in',customer.partner_id.ids)])

        return {
            'total_contract':total_contract,
            'new_contract':new_contract,
            'running_contract':running_contract,
            'expiry_soon_contract':expiry_soon_contract,
            'expired_contract':expired_contract,
            'locked_contract':locked_contract,
            'total_product':total_product,
            'total_invoice':total_invoice,
            'total_customer':total_customer
        }

    @api.model
    def get_week_contract(self):
        cr = self._cr

        query = """
        SELECT cl.start_contract_date AS date_time,count(*) as count
        FROM account_analytic_account cl 
        group by cl.start_contract_date
        order by cl.start_contract_date

        """
        cr.execute(query)
        partner_data = cr.dictfetchall()
        partner_day = []
        data_set = {}
        mydate = []
        mycount = []
        list_value = []
        dict={} 
        count = 0
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                         "Friday", "Saturday", "Sunday"]
        for data in partner_data:
            if data['date_time']:
                mydate = data['date_time'].weekday()
                if mydate >= 0:
                    value = days[mydate]
                    list_value.append(value)
                    
                    list_value1 = list(set(list_value))

                    for record in list_value1:
                        count = 0
                        for rec in list_value:
                            if rec ==record:
                                count = count+1
                            dict.update({record:count})
                        keys, values = zip(*dict.items())
                        data_set.update({"data":dict})
        return data_set

    @api.model
    def get_monthly_contract(self):
        cr = self._cr

        query = """
        SELECT cl.start_contract_date AS start_date,count(*) as count
        FROM account_analytic_account cl
        group by cl.start_contract_date
        order by cl.start_contract_date

        """
        cr.execute(query)
        partner_data = cr.dictfetchall()
        partner_day = []
        data_set = {}
        mycount = []
        list_value = []
        
        dict={} 
        count = 0

        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                'August', 'September', 'October', 'November', 'December']
    
        for data in partner_data:
            if data['start_date']:
                mydate = data['start_date'].month
                for month_idx in range(0, 13):
                    if mydate == month_idx:
                        value = cal.month_name[month_idx]
                        list_value.append(value)
                        list_value1 = list(set(list_value))
                        for record in list_value1:
                            count = 0
                            for rec in list_value:
                                if rec ==record:
                                    count = count+1
                                dict.update({record:count})
                        keys, values = zip(*dict.items())
                        data_set.update({"data":dict})
        return data_set

    @api.model
    def _cron_generate_invoice(self):
        get_contract = self.env['account.analytic.account'].sudo().search([('date_of_next_invoice','=', datetime.now())])
        for record in get_contract:
            invoice = self.env['account.move'].create({
                'partner_id':record.partner_id.id,
                'type': 'out_invoice',
                'invoice_date': fields.Date.today(),
                'company_id':record.company_id.id,
            })
            for data in record.contact_line:
                invoice.write({
                    'invoice_line_ids': [(0, 0, {
                        'product_id': data.product_id.id,
                        'name':data.name,
                        'quantity':data.product_uom_qty,
                        'price_unit':data.price_unit,
                    })],        
                }) 
            record.write({'invoice_ids': invoice.ids})
        return True


    def _find_mail_template(self, force_confirmation_template=False):
        template_id = False
        if force_confirmation_template or (self.state != 'locked'):
            template_id = int(self.env['ir.config_parameter'].sudo().get_param('sales_contract_seperate_module.default_template'))
            template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
            if not template_id:
                template_id = self.env['ir.model.data'].xmlid_to_res_id('sales_contract_seperate_module.mail_template_contract', raise_if_not_found=False)
        return template_id

    def action_contract_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_template(template.lang, 'account.analytic.account', self.ids[0])
        ctx = {
            'default_model': 'account.analytic.account',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }


