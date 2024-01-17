from odoo import api, fields, models, _
from datetime import date, datetime,timedelta
from odoo.exceptions import UserError, ValidationError
from num2words import num2words 
import logging
_logger = logging.getLogger(__name__)
   
class AccountMove(models.Model):
    _inherit = "account.move"
    
    # @api.multi
    

  #  num_word = fields.Char(string="Amount In Words:", compute='_compute_amount_in_word')
   # num_total = fields.Char(string="Total Roundoff", compute='_compute_amount_in_word')
    dispatched = fields.Char('Dispatched By')
    
    # def _compute_amount_in_word(self):
        # for rec in self:
            # word = round(int(rec.amount_total))
            # rec.num_total = word
            # rec.num_word =(num2words(word).capitalize()) + ' '+'rupees only'
            
           # # rec.num_word = str(rec.currency_id.amount_to_text(rec.amount_total)) + ' only'

    
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
 
    transport = fields.Char('Transport')   
 
 
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    hsn_code = fields.Char('HSN Code')
    
class Company(models.Model):
    _inherit = "res.company"
    
    logo_2 = fields.Binary(string="Company Logos", readonly=False)
    logos_2 = fields.Binary(string="Company Logos", readonly=False)     
    
class SaleOrder(models.Model):
    _inherit = "sale.order"
    
       
   # num_word = fields.Char(string="Amount In Words:", compute='_compute_amount_in_word')
    dispatched = fields.Char('Dispatched By')
    
    # def _compute_amount_in_word(self):
        # for rec in self:
            # rec.num_word = str(rec.currency_id.amount_to_text(rec.amount_total)) + ' only'
    
    