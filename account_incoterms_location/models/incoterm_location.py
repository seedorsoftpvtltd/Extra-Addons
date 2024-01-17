# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountIncoterms(models.Model):
    _inherit = 'account.incoterms'

    location_required = fields.Boolean('location required', copy=False, default=False)
  
   
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    location_incoterm = fields.Char('Default Incoterm Location', related='company_id.location_incoterm', readonly=False)
   
        
class ResCompany(models.Model):
    _inherit = 'res.company'

    location_incoterm = fields.Char('Default Incoterm Location')
    
    @api.constrains('incoterm_id', 'location_incoterm')
    def _check_incoterm_location(self):
        if self.incoterm_id.location_required and not self.location_incoterm:
            raise UserError(_('please enter an incoterm location'))
        return True


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _get_default_incoterm_id(self):
        return self.env.user.company_id.incoterm_id
    
    incoterm_id = fields.Many2one(default=_get_default_incoterm_id)
    location_incoterm = fields.Char('Incoterm Location', copy=False, track_visibility='always', states={'done': [('readonly', True)]})
    
    @api.constrains('incoterm_id', 'location_incoterm')
    def _check_incoterm_location(self):
        if self.incoterm_id.location_required and not self.location_incoterm:
            raise UserError(_('please enter an incoterm location'))
        return True
        
    def action_view_invoice(self):
        result = super().action_view_invoice()
        if self.incoterm_id:
            result['context']['default_invoice_incoterm_id'] = self.incoterm_id.id
        if self.location_incoterm:
            result['context']['default_location_incoterm'] = self.location_incoterm
        return result
        
        
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_default_incoterm_id(self):
        return self.env.user.company_id.incoterm_id
    
    incoterm = fields.Many2one(default=_get_default_incoterm_id)
    location_incoterm = fields.Char('Incoterm Location', copy=False, track_visibility='always')
    
    @api.constrains('incoterm', 'location_incoterm')
    def _check_incoterm_location(self):
        if self.incoterm.location_required and not self.location_incoterm:
            raise UserError(_('please enter an incoterm location'))
        return True
        
    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        if self.location_incoterm:
            invoice_vals['location_incoterm'] = self.location_incoterm
        return invoice_vals
    

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_default_incoterm_location(self):
        return self.env.user.company_id.location_incoterm

    location_incoterm = fields.Char('Incoterm Location', copy=False, track_visibility='always', default=_get_default_incoterm_location, readonly=True, states={'draft': [('readonly', False)]})
    
    @api.constrains('invoice_incoterm_id', 'location_incoterm')
    def _check_incoterm_location(self):
        if self.invoice_incoterm_id.location_required and not self.location_incoterm:
            raise UserError(_('please enter an incoterm location'))
        return True
