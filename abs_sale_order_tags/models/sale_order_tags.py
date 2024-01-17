# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020-today Ascetic Business Solution <www.asceticbs.com>
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

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ##create a invoice with tags of sale order into a account.invoice many2many field 'Tags'
    @api.model
    def _prepare_invoice(self):
        result = super(SaleOrder,self)._prepare_invoice()
        tag_list = []
        for record in self.tag_ids: 
            tags = self.env['crm.lead.tag'].search([('name','=',record.name)])
            tag_list.append(tags.id)
            result['invoice_tag_ids'] = [(6, 0,tag_list)]
        return result
