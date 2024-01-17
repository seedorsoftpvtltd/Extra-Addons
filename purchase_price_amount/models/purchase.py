# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from datetime import datetime, timedelta
from datetime import *
from dateutil.relativedelta import *
import time
from odoo.exceptions import UserError

class PurchasePrice(models.Model):
    _inherit = 'purchase.order'

#    def action_view_invoice_new(self):
#        ret = self.action_view_invoice()
#        move_line = self.env['account.move.line']
#        for recs in self.order_line:
#            move_line.search([('purchase_line_id','='recs.id)]).update({'price_unit':655665})
#        return ret

    def action_view_invoice_new(self):
        ret = self.action_view_invoice()
        move_line = self.env['account.move.line']
        for recs in self.order_line:
            move_line.search([('product_id','=',recs.product_id.id)]).update({'price_unit':recs.price_unit})
            print(" vamk vamk vamk logs %s  next move line %s"%(recs.id,move_line.search([('product_id','=',recs.product_id.id)]).product_id.name))
        return ret

