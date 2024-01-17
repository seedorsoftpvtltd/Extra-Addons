from odoo.http import request
from odoo import api, fields, models, tools, osv, http, _
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError, AccessError, MissingError, ValidationError


class companyext(models.Model):
    _inherit = "res.company"

    company_code = fields.Char('Company Code', store=True)


class freightext(models.Model):
    _inherit = 'freight.operation'

    seq = fields.Char('Custom Sequence')

    @api.model
    def create(self, vals):
        record = super(freightext, self).create(vals)
        record['seq'] = self.env['ir.sequence'].next_by_code('job.log.seq')
        return record

    @api.constrains('transport', 'direction', 'partner_id', 'seq')
    def cust_seq(self):
        try:
            print(self.transport, self.direction)
            if self.transport != False:
                trans = self.transport[0].upper()
            if self.transport == False:
                trans = ''
            if self.direction != False:
                if self.direction == 'import':
                    dir = '01'
                if self.direction == 'export':
                    dir = '02'
                if self.direction not in ('import', 'export'):
                    dir = ''
            else:
                dir = ''
            crnt_mnth = date.today().strftime('%m')
            mnth = (str(crnt_mnth))
            crnt_year = date.today().year
            yr = (str(crnt_year))[-2] + (str(crnt_year))[-1]
            print(trans, dir, mnth, yr)
            cc = self.env.company.company_code
            if not cc:
                raise UserError(_("Please define company code!!"))
            seq = str(cc) + str(trans) + str(dir) + (yr) + (mnth) + str(self.seq)
            print(seq)
            self['name'] = seq
            print(self.transport, self.direction)
        except:
            crnt_mnth = date.today().strftime('%m')
            mnth = (str(crnt_mnth))
            crnt_year = date.today().year
            yr = (str(crnt_year))[-2] + (str(crnt_year))[-1]
            print(mnth, yr)
            cc = self.env.company.company_code
            if not cc:
                raise UserError(_("Please define company code!!"))
            seq = str(cc) + (yr) + (mnth) + str(self.seq)
            print(seq)
            self['name'] = seq


class SaleOrderext(models.Model):
    _inherit = 'sale.order'

    seq = fields.Char('Custom Sequence')

    @api.model
    def create(self, vals):
        record = super(SaleOrderext, self).create(vals)
        record['seq'] = self.env['ir.sequence'].next_by_code('so.log.seq')
        return record

    @api.constrains('fright_transport', 'fright_direction', 'partner_id', 'seq')
    def cust_seq(self):
        try:
            print(self.fright_transport, self.fright_direction)
            if self.fright_transport != False:
                trans = self.fright_transport[0].upper()
            if self.fright_transport == False:
                trans = ''
            if self.fright_direction != False:
                if self.fright_direction == 'import':
                    dir = '01'
                if self.fright_direction == 'export':
                    dir = '02'
                if self.fright_direction not in ('import', 'export'):
                    dir = ''
            else:
                dir = ''
            crnt_mnth = date.today().strftime('%m')
            mnth = (str(crnt_mnth))
            crnt_year = date.today().year
            yr = (str(crnt_year))[-2] + (str(crnt_year))[-1]
            print(trans, dir, mnth, yr)
            cc = self.env.company.company_code
            if not cc:
                raise UserError(_("Please define company code!!"))
            seq = str(cc) + str(trans) + str(dir) + (yr) + (mnth) + str(self.seq)
            print(seq)
            self['name'] = seq
            print(self.fright_transport, self.fright_direction)
        except:
            crnt_mnth = date.today().strftime('%m')
            mnth = (str(crnt_mnth))
            crnt_year = date.today().year
            yr = (str(crnt_year))[-2] + (str(crnt_year))[-1]
            print(mnth, yr)
            cc = self.env.company.company_code
            if not cc:
                raise UserError(_("Please define company code!!"))
            seq = str(cc) + (yr) + (mnth) + str(self.seq)
            print(seq)
            self['name'] = seq


# class invline(models.Model):
#     _inherit = 'stock.inventory.line'
#
#     # @api.model
#     def fetch_bs(self):
#         bs = self.env['stock.inventory.line'].search([])
#         for rec in bs:
#             rec.fetch_bss()
#
#
#         # try:
#         #     if self.x_serialno:
#         #         self.lot_id.serialno = self.x_serialno
#         #         print('self.lot_id.serialno')
#         #     if self.x_batchno:
#         #         self.lot_id.batchno = self.x_batchno
#         #         print('self.lot_id.batchno')
#         # except:
#         #     print('hlooooo')
#
#     def fetch_bss(self):
#         print('hiiii')
#         try:
#             if self.x_serialno:
#                 self.lot_id.serialno = self.x_serialno
#                 print('self.lot_id.serialno')
#             if self.x_batchno:
#                 self.lot_id.batchno = self.x_batchno
#                 print('self.lot_id.batchno')
#         except:
#             print('hlooooo')
#
#
#
#
