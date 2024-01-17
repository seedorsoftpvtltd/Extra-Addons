from dateutil import parser
from odoo import api, models, fields, http, _
from datetime import datetime, date, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    start_date_sto = fields.Date(string = 'Start Date Sto', store=True)
    end_date_sto = fields.Date(string='End Date Sto', store=True)
    sto_type = fields.Selection(string="Invoicing Type", selection=[('cfs', 'CFS'), ('warehouse', 'Warehouse')],store=True)


class chargetypes(models.Model):
    _name = "charge.types"

    name = fields.Char(string='Name', store=True)
    restricted = fields.Boolean(string='Is Restricted', store=True)

    def write(self, vals):
        res = super(chargetypes, self).write(vals)
        if self.restricted == True:
            raise UserError(_('You are not allowed to edit this record'))
        return res

    def unlink(self):
        if self.restricted == True:
            raise UserError(_('You are not allowed to edit this record'))
        return super(chargetypes, self).unlink()


class servicechargeagree(models.Model):
    _inherit = "agreement.charges"

    charge_unit_type = fields.Many2one('charge.types', string="Charge Type", store=True)
    is_uom = fields.Boolean(string='Is UOM', store=True, default=False)

    @api.onchange('charge_unit_type')
    def _onchange_charge_unit_type(self):
        for rec in self:
            if rec.charge_unit_type.name == 'UOM':
                rec['is_uom'] = True
            else:
                rec['is_uom'] = False


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    charge_unit_type = fields.Many2one('charge.types', string="Charge Type", store=True)

#     def _search_charge_unit_type_domain(self):
#         print(self._context,'------------', self.env.context.get('base_model_name'))
#         try:
#             print('try')
#             if self.env.context.get('params')['model'] == 'stock.picking':
#                 print('if--------------1')
#                 picking_id = self.env.context.get('params')['id']
#                 picking = self.env['stock.picking'].browse(picking_id)
#                 partner = picking.partner_id
#                 agreement = self.env['agreement'].search([('partner_id', '=', partner.id)])
#                 print(agreement, 'agreement')
#                 domain = []
#                 if agreement:
#                     print('if')
#                     agreement_charges = self.env['agreement.charges'].search([('agreement_id', '=', agreement.id)])
#                     for line in agreement_charges:
#                         if line.charge_unit_type and line.charge_unit_type not in domain:
#                             domain.append(line.charge_unit_type.id)
#                     print(domain, 'domain')
#                     return [('id', 'in', domain)]
#                 else:
#                     print('else')
#                     return [('id', 'in', domain)]
#             if self.env.context['base_model_name'] == 'stock.picking':
#                 print('if--------------1')
#                 picking_id = self.env.context.get('params')['id']
#                 picking = self.env['stock.picking'].browse(picking_id)
#                 partner = picking.partner_id
#                 agreement = self.env['agreement'].search([('partner_id', '=', partner.id)])
#                 print(agreement, 'agreement')
#                 domain = []
#                 if agreement:
#                     print('if')
#                     agreement_charges = self.env['agreement.charges'].search([('agreement_id', '=', agreement.id)])
#                     for line in agreement_charges:
#                         if line.charge_unit_type and line.charge_unit_type not in domain:
#                             domain.append(line.charge_unit_type.id)
#                     print(domain, 'domain')
#                     return [('id', 'in', domain)]
#                 else:
#                     print('else')
#                     return [('id', 'in', domain)]
#             if self._context['default_picking_id']:
#                 print('if--------------2')
#                 picking_id = self._context['default_picking_id']
#                 picking = self.env['stock.picking'].browse(picking_id)
#                 partner = picking.partner_id
#                 agreement = self.env['agreement'].search([('partner_id', '=', partner.id)])
#                 print(agreement, 'agreement')
#                 domain = []
#                 if agreement:
#                     print('if')
#                     agreement_charges = self.env['agreement.charges'].search([('agreement_id', '=', agreement.id)])
#                     for line in agreement_charges:
#                         if line.charge_unit_type and line.charge_unit_type not in domain:
#                             domain.append(line.charge_unit_type.id)
#                     print(domain, 'domain')
#                     return [('id', 'in', domain)]
#                 else:
#                     print('else')
#                     return [('id', 'in', domain)]
#
#         # else:
#         #     print('else--------------1')
#         #     domain = self.env['charge.types'].search([])
#         #     return [('id', 'in', [])]
#         except:
#             print('no params')
#



class Settings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_type = fields.Selection([
        ('sep', 'Generate Seperate Invoice'),
        ('con', 'Generate Consolidated Invoice')], string="Select the Invoice Type",
        default='sep',
        config_parameter='hb_wms_invoice_v1.invoice_type')
