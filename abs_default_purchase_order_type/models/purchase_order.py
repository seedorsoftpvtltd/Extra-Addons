# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-Today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api, fields, models, _

class ResPartnerInPurchaseOrder(models.Model):
    _inherit = "res.partner"
  
    purchase_order_type = fields.Many2one('purchase.type',string="Purchase Order Type")

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    #This function is automatically fill vendors purchase order types field on purchase order.  
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        result1 = super(PurchaseOrder,self).onchange_partner_id()
        if self.partner_id:
            partner_purchase_order_type = self.partner_id.purchase_order_type
            self.partner_ref = partner_purchase_order_type.partner_ref
            self.payment_term_id = partner_purchase_order_type.payment_term_id
            self.incoterm_id = partner_purchase_order_type.incoterm_id
        return result1

