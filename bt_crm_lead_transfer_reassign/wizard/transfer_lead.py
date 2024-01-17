# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class BtTransferLead(models.TransientModel):
    _name = 'bt.transfer.lead'
    _description = 'Transfer Lead'
    

    present_user_id = fields.Many2one('res.users', 'Salesperson')
    lead_details_ids = fields.One2many('bt.lead.details', 'transfer_lead_id')
     
     
    @api.onchange('present_user_id')    
    def on_change_sale_person(self):
        self.lead_details_ids=False        
        if not self.present_user_id:
            return {}
        lead_ids = self.env['crm.lead'].search([('user_id', '=' , self.present_user_id.id)])
        if lead_ids:
            x = [{
                'lead_id': lead.id , 
                'user_id': lead.user_id.id, 
                'lead_name': lead.name
            } for lead in lead_ids]            
            for lead in x:                          
                self.lead_details_ids=[(0,0,lead)]                      
        else:
            raise UserError(_('There is no lead  for   %s ') % (self.present_user_id.name))
                 
                    
    def action_transfer_apply(self):
        for lead in self.lead_details_ids:
            if lead.assign_user_id :                
                lead.lead_id.write({'user_id': lead.assign_user_id.id})
               
        
class BtLeadDetails(models.TransientModel):
    _name = 'bt.lead.details'
    _description = 'Lead Details'
    
    lead_id = fields.Many2one('crm.lead', 'Lead Id')
    user_id = fields.Many2one('res.users', 'Salesperson')
    transfer_lead_id = fields.Many2one('bt.transfer.lead', 'Lead Transfer')
    assign_user_id = fields.Many2one('res.users', 'New Salesperson')
    lead_name = fields.Char('Lead')
    

