# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class message_inherit(models.Model):
    _inherit = "mail.message"

    @api.model
    def create(self, values):
        res = super(message_inherit,self).create(values)
        if values.get('model') == 'crm.lead' :
            if values.get('message_type') == 'comment' :
                crm_res = self.env['crm.lead'].browse(values.get('res_id'))
                if crm_res :
                	partner_res = self.env['res.partner'].search([('email','=',crm_res.email_from)])
        return res


class partner_inherit(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, values):
        res = super(partner_inherit,self).create(values)
        active_model = self.env.context.get('active_model')
        if active_model == 'crm.lead':
            lead = self.env[active_model].browse(self.env.context.get('active_id')).exists()
            if lead:
                lead.partner_id = res.id

        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: