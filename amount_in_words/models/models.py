from odoo import api, fields, models, _
from num2words import num2words

class Overdue_amount(models.Model):
    _inherit='res.partner'

    amount_in_word=fields.Text(string='Amount In Words',compute='_get_amount_in_words')
    curr_first_thirty_day = fields.Float(string="0-30", compute="cur_compute_days")
    curr_thirty_sixty_days = fields.Float(string="30-60", compute="cur_compute_days")
    curr_sixty_ninty_days = fields.Float(string="60-90", compute="cur_compute_days")
    curr_ninty_onetwenty_days = fields.Float(string="90-120", compute="cur_compute_days")
    curr_onetwenty_onefifty_days = fields.Float(string="120-150", compute="cur_compute_days")
    curr_onefifthy_oneeighty_days = fields.Float(string="150-180", compute="cur_compute_days")
    curr_oneeighty_plus_days = fields.Float(string="180+", compute="cur_compute_days")
    curr_total = fields.Float(string="Total", compute="cur_compute_total")

    def _get_amount_in_words(self):
        for rec in self:
            if rec.balance_invoice_over_ids:
                val=0.0
                for rr1 in rec.balance_invoice_over_ids:
                    if rr1.currency_id == self.env.ref('base.main_company').currency_id:
                        val=val+rr1.result_over
                val=round(val)
                a=num2words(val, lang='en')
                a1=a.title()
                #a1=str(rec.currency_id.amount_to_text(val))
                rec['amount_in_word']=a1
            else:
                rec['amount_in_word']=''

    @api.depends('balance_invoice_ids')
    def cur_compute_days(self):
        today = fields.date.today()
        for partner in self:
            partner.curr_first_thirty_day = 0
            partner.curr_thirty_sixty_days = 0
            partner.curr_sixty_ninty_days = 0
            partner.curr_ninty_onetwenty_days = 0
            partner.curr_onetwenty_onefifty_days = 0
            partner.curr_onefifthy_oneeighty_days = 0
            partner.curr_oneeighty_plus_days = 0
            if partner.balance_invoice_ids:
                for line in partner.balance_invoice_ids:
                 if line.currency_id == self.env.ref('base.main_company').currency_id:
                    diff = today - line.invoice_date_due
                    if diff.days <= 30 and diff.days > 0:
                        partner.curr_first_thirty_day = partner.curr_first_thirty_day + line.result
                    elif diff.days > 30 and diff.days <= 60:
                        partner.curr_thirty_sixty_days = partner.curr_thirty_sixty_days + line.result
                    elif diff.days > 60 and diff.days <= 90:
                        partner.curr_sixty_ninty_days = partner.curr_sixty_ninty_days + line.result
                    elif diff.days > 90 and diff.days <= 120:
                        partner.curr_ninty_onetwenty_days = partner.curr_ninty_onetwenty_days + line.result
                    elif diff.days > 120 and diff.days <= 150:
                        partner.curr_onetwenty_onefifty_days = partner.curr_onetwenty_onefifty_days + line.result
                    elif diff.days > 150 and diff.days <= 180:
                        partner.curr_onefifthy_oneeighty_days = partner.curr_onefifthy_oneeighty_days + line.result
                    else:
                        if diff.days > 180:
                            partner.curr_oneeighty_plus_days = partner.curr_oneeighty_plus_days + line.result
        return

    @api.depends('curr_oneeighty_plus_days','curr_onefifthy_oneeighty_days','curr_onetwenty_onefifty_days','curr_ninty_onetwenty_days', 'curr_sixty_ninty_days', 'curr_thirty_sixty_days', 'curr_first_thirty_day')
    def cur_compute_total(self):
        for partner in self:
            partner.curr_total = 0.0
            partner.curr_total =partner.curr_oneeighty_plus_days +partner.curr_onefifthy_oneeighty_days +partner.curr_onetwenty_onefifty_days +partner.curr_ninty_onetwenty_days + partner.curr_sixty_ninty_days + partner.curr_thirty_sixty_days + partner.curr_first_thirty_day
        return

