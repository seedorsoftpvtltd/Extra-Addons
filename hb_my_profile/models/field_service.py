import datetime
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta


class FieldServiceCnt(models.Model):
    _inherit = "res.users"

    # fsm_id = fields.Integer()
    fsm_myservices = fields.Integer(string="My Orders", compute='_fsm_myservices')
    fsm_mylast_servdate = fields.Date(string="Last Service Date - My", compute='_fsm_mylast_servdate')
    fsm_pendingservices = fields.Integer(string="Pending Services - My", compute='_fsm_pendingservices')

    def _fsm_myservices(self):
        for rec in self:
            partner = rec.partner_id.id
            fsm_myorders = self.env['fsm.order'].search(
                [('person_id.partner_id.id', '=', partner), ('stage_id.is_closed', '=', True)])
            tot = len(fsm_myorders)
            rec['fsm_myservices'] = tot
            # print(partner)
            # print(fsm_myorders)
            print(rec.fsm_myservices, 'fsm_myservices')

    def _fsm_mylast_servdate(self):
        for rec in self:
            partner = rec.partner_id
            last_id = self.env['fsm.order'].search([], order='id desc')[0]
            # print(last_id)
            # rec['fsm_mylast_servdate'] = last_id.create_date
            # print(rec.fsm_mylast_servdate, 'fsm_mylast_servdate')
            if last_id.person_id.partner_id == partner:
                print(last_id, 'last')
                rec['fsm_mylast_servdate'] = last_id.create_date
                print(rec.fsm_mylast_servdate, 'fsm_mylast_servdate')
            else:
                rec['fsm_mylast_servdate'] = ''
                print(rec.fsm_mylast_servdate, 'fsm_mylast_servdate')

    def _fsm_pendingservices(self):
        for rec in self:
            partner = rec.partner_id.id
            fsm_pendingorders = self.env['fsm.order'].search(
                [('person_id.partner_id.id', '=', partner), ('stage_id.is_closed', '=', False)])
            tot = len(fsm_pendingorders)
            rec['fsm_pendingservices'] = tot
            print(rec.fsm_pendingservices, 'fsm_pendingservices')

    fsm_services = fields.Integer(string="My Orders", compute='_fsm_services')
    fsm_last_servdate = fields.Date(string="Last Service Date - My", compute='_fsm_last_servdate')
    fsm_last_pick = fields.Char(string="Pending Services - My", compute='_fsm_last_pick')

    def _fsm_services(self):
        for rec in self:
            fsm_myorders = self.env['fsm.order'].search([('person_id', '=', False), ('stage_id.is_closed', '=', False)])
            tot = len(fsm_myorders)
            rec['fsm_services'] = tot
            print(rec.fsm_services, 'fsm_services')

    def _fsm_last_servdate(self):
        for rec in self:
            last_id = self.env['fsm.order'].search([('person_id', '=', False)], order='id desc')[0]
            print(last_id, 'last')
            rec['fsm_last_servdate'] = last_id.create_date
            print(rec.fsm_last_servdate, 'fsm_last_servdate')

    def _fsm_last_pick(self):
        for rec in self:
            fsm_last_pickkk = \
            self.env['fsm.order'].search([('stage_id.is_closed', '=', False), ('person_id', '!=', False)],
                                         order='person_id desc')[0]
            date = fsm_last_pickkk.pick_date
            now = datetime.datetime.now()
            print(fsm_last_pickkk, date, 'dateeeeeeeeeeeeeeeeee')
            print(now, 'nowwwwwwwwwwwwww')
            if date:
                # lstpick = (now - date).days
                lstpick = relativedelta(now, date)
                durat = '{} year {} month {} days {} hours'.format(lstpick.years, lstpick.months, lstpick.days,
                                                                   lstpick.hours)

                rec['fsm_last_pick'] = durat
                print(rec.fsm_last_pick, 'fsm_last_pick')
            else:
                rec['fsm_last_pick'] = ''
                print(rec.fsm_last_pick, 'fsm_last_pick')

    crm_opp_count = fields.Integer("pipeline Count", compute='_compute_crm_opp_count')
    crm_sale_count = fields.Integer("Sales Count", compute='_compute_crm_sale_count')
    crm_inv_count = fields.Integer("Invoice Count", compute='_compute_crm_inv_count')
    crm_quot_count = fields.Integer("Quotation Count", compute='_compute_crm_quot_count')
    crm_lead_count = fields.Integer("Lead Count", compute='_compute_crm_lead_count')
    crm_partner_count = fields.Integer("Partner Count", compute='_compute_crm_partner_count')

    def _compute_crm_partner_count(self):
        for rec in self:
            partner = self.env['res.partner'].search([])
            tot = len(partner)
            if tot:
                rec['crm_partner_count'] = tot
            else:
                rec['crm_partner_count'] = ''
                print(rec.crm_partner_count, 'crm_partner_count')

    def _compute_crm_quot_count(self):
        for rec in self:
            crm_quot = self.env['sale.order'].search([('user_id.id', '=', rec.id), ('state', '!=', 'sale')])
            tot = len(crm_quot)
            if tot:
                rec['crm_quot_count'] = tot
            else:
                rec['crm_quot_count'] = ''
                print(rec.crm_quot_count, 'crm_quot_count')

    def _compute_crm_lead_count(self):
        for rec in self:
            crm_lead = self.env['crm.lead'].search([('user_id.id', '=', rec.id), ('type', '=', 'lead')])
            tot = len(crm_lead)
            if tot:
                rec['crm_lead_count'] = tot
            else:
                rec['crm_lead_count'] = ''
                print(rec.crm_lead_count, 'crm_lead_count')

    def _compute_crm_opp_count(self):
        for rec in self:
            crm_opp = self.env['crm.lead'].search([('user_id.id', '=', rec.id), ('type', '=', 'opportunity')])
            tot = len(crm_opp)
            if tot:
                rec['crm_opp_count'] = tot
            else:
                rec['crm_opp_count'] = ''
                print(rec.crm_opp_count, 'crm_opp_count')

    def _compute_crm_sale_count(self):
        for rec in self:
            crm_sale = self.env['sale.order'].search([('user_id.id', '=', rec.id), ('state', '=', 'sale')])
            tot = len(crm_sale)
            if tot:
                rec['crm_sale_count'] = tot
            else:
                rec['crm_sale_count'] = ''
                print(rec.crm_sale_count, 'crm_sale_count')

    def _compute_crm_inv_count(self):
        for rec in self:
            crm_inv = self.env['account.move'].search([('user_id.id', '=', rec.id), ('state', '=', 'sale')])
            tot = len(crm_inv)
            if tot:
                rec['crm_inv_count'] = tot
            else:
                rec['crm_inv_count'] = ''
                print(rec.crm_inv_count, 'crm_inv_count')

    # stk_mydeliveries = fields.Integer(string="My Orders", compute='_stk_mydeliveries')
    # stk_mylast_delvdate = fields.Date(string="Last Service Date - My", compute='_stk_mylast_delvdate')
    # stk_pendingdeliveries = fields.Integer(string="Pending Services - My", compute='_stk_pendingdeliveries')
    #
    # def _stk_mydeliveries(self):
    #     for rec in self:
    #         partner = rec.partner_id.id
    #         stk_myorders = self.env['stock.picking'].search([('partner_id.id', '=', partner)])
    #         tot = len(stk_myorders)
    #         rec['stk_mydeliveries'] = tot
    #         print(rec.stk_mydeliveries, 'stk_mydeliveries')
    #
    # def _fsm_mylast_delvdate(self):
    #     for rec in self:
    #         partner = rec.partner_id
    #         last_id = self.env['stock.picking'].search([], order='id desc')[0]
    #         if last_id.partner_id == partner:
    #             print(last_id, 'last')
    #             rec['stk_mylast_delvdate'] = last_id.create_date
    #             print(rec.stk_mylast_delvdate, 'stk_mylast_delvdate')
    #         else:
    #             rec['stk_mylast_delvdate'] = ''
    #             print(rec.stk_mylast_delvdate, 'stk_mylast_delvdate')
    #
    # def _stk_pendingdeliveries(self):
    #     for rec in self:
    #         partner = rec.partner_id.id
    #         stk_pendingdeliveries = self.env['stock.picking'].search(
    #             [('partner_id.id', '=', partner), ('state', '=', ('draft', 'waiting', 'confirmed'))])
    #         tot = len(stk_pendingdeliveries)
    #         rec['stk_pendingdeliveries'] = tot
    #         print(rec.stk_pendingdeliveries, 'stk_pendingdeliveries')
    #
    # stk_deliveries = fields.Integer(string="My Orders", compute='_stk_services')
    # stk_last_deldate = fields.Date(string="Last Service Date - My", compute='_stk_last_servdate')
    # stk_last_pick = fields.Char(string="Pending Services - My", compute='_stk_last_pick')
    #
    # def _stk_services(self):
    #     for rec in self:
    #         fsm_myorders = self.env['stock.picking'].search([('person_id', '=', False)])
    #         tot = len(fsm_myorders)
    #         rec['stk_deliveries'] = tot
    #         print(rec.stk_deliveries, 'stk_deliveries')
    #
    # def _stk_last_servdate(self):
    #     for rec in self:
    #         last_id = self.env['fsm.order'].search([('person_id', '=', False)], order='id desc')[0]
    #         print(last_id, 'last')
    #         rec['stk_last_deldate'] = last_id.create_date
    #         print(rec.stk_last_deldate, 'stk_last_deldate')
    #
    # def _stk_last_pick(self):
    #     for rec in self:
    #         stk_last_pickkk = \
    #             self.env['fsm.order'].search([('stage_id.is_closed', '=', False)], order='person_id desc')[0]
    #         date = stk_last_pickkk.pick_date
    #         print(date)
    #         rec['stk_last_pick'] = stk_last_pickkk.id
    #         print(rec.stk_last_pick, 'fsm_last_pick')


class FieldServiceINH(models.Model):
    _inherit = "fsm.order"

    pick_date = fields.Datetime('Pick Date', compute='_compute_pick_date', store="True")
    picked = fields.Boolean('Picked')

    @api.onchange('person_id')
    def _compute_pick_date(self):
        for rec in self:
            if rec.person_id and rec.picked == False:
                now = datetime.datetime.now()
                rec['pick_date'] = now
                rec['picked'] = True
                print(rec.pick_date)
            else:
                rec['pick_date'] = ''

