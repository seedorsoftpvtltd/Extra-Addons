# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Contact(models.Model):
    _inherit = 'res.partner'
    add_user_ids = fields.Many2many("res.users")

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    add_user_ids = fields.Many2many("res.users")

    @api.onchange('partner_id')
    def onchange_partner2_id(self):
        self.add_user_ids = self.partner_id.add_user_ids

class Crm(models.Model):
    _inherit = 'crm.lead'
    add_user_ids = fields.Many2many("res.users")

    def _create_lead_partner_data(self, name, is_company, parent_id=False):
        res = super(Crm,self)._create_lead_partner_data(name, is_company, parent_id)
        data = []
        for add_user_id in self.add_user_ids:
            data.append(add_user_id.id)
        res.update({'add_user_ids': data})
        return res







