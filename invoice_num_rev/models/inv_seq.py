
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from datetime import datetime, timedelta
from datetime import *
from dateutil.relativedelta import *
import time
from odoo.exceptions import UserError

class AccSeq(models.Model):
    _inherit = 'account.move'

    fin_seq = fields.Char("Seq Final")

    def action_post_seq(self):
        acc = self.env['account.move'].search([('type', '=', 'in_invoice'),('invoice_date','!=',None)])
        for recs in acc:
            if recs.fin_seq != 'done':
               test = recs.name
               seq_name = test.replace(test[0:4],"BILV")
               recs.write({'name': seq_name,'fin_seq':"done"})

