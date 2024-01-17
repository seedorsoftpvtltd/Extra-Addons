from odoo import api, fields, models, _
from num2words import num2words
from odoo.tools.float_utils import float_round

class Overdue_amount(models.Model):
    _inherit='res.partner'

    curr_total1 = fields.Float(string="Total", compute="cur_compute_total")
    curr_first_thirty_day1 = fields.Float(string="0-30", compute="cur_compute_days")
    curr_thirty_sixty_days1 = fields.Float(string="30-60", compute="cur_compute_days")
    curr_sixty_ninty_days1 = fields.Float(string="60-90", compute="cur_compute_days")
    curr_ninty_onetwenty_days1 = fields.Float(string="90-120", compute="cur_compute_days")
    curr_onetwenty_onefifty_days1 = fields.Float(string="120-150", compute="cur_compute_days")
    curr_onefifthy_oneeighty_days1 = fields.Float(string="150-180", compute="cur_compute_days")
    curr_oneeighty_plus_days1 = fields.Float(string="180+", compute="cur_compute_days")
    curr_usd = fields.Float(string="Total", compute="cur_compute_total_usd")
    curr_first_thirty_usd = fields.Float(string="0-30", compute="cur_compute_days")
    curr_thirty_sixty_usd = fields.Float(string="30-60", compute="cur_compute_days")
    curr_sixty_ninty_usd = fields.Float(string="60-90", compute="cur_compute_days")
    curr_ninty_onetwenty_usd = fields.Float(string="90-120", compute="cur_compute_days")
    curr_onetwenty_onefifty_usd = fields.Float(string="120-150", compute="cur_compute_days")
    curr_onefifthy_oneeighty_usd = fields.Float(string="150-180", compute="cur_compute_days")
    curr_oneeighty_plus_usd = fields.Float(string="180+", compute="cur_compute_days")

    @api.depends('balance_invoice_over_ids')
    def cur_compute_days(self):

        today = fields.date.today()
        for partner in self:
            partner.curr_first_thirty_day1 = 0
            partner.curr_thirty_sixty_days1 = 0
            partner.curr_sixty_ninty_days1 = 0
            partner.curr_ninty_onetwenty_days1 = 0
            partner.curr_onetwenty_onefifty_days1 = 0
            partner.curr_onefifthy_oneeighty_days1 = 0
            partner.curr_oneeighty_plus_days1 = 0
            partner.curr_first_thirty_usd = 0
            partner.curr_thirty_sixty_usd = 0
            partner.curr_sixty_ninty_usd = 0
            partner.curr_ninty_onetwenty_usd = 0
            partner.curr_onetwenty_onefifty_usd = 0
            partner.curr_onefifthy_oneeighty_usd = 0
            partner.curr_oneeighty_plus_usd = 0
            if partner.balance_invoice_over_ids:

                for line in partner.balance_invoice_over_ids:
                 if line.currency_id == self.env.ref('base.main_company').currency_id:

                    diff = today - line.invoice_date

                    if diff.days <= 30 and diff.days >= 0:

                        partner.curr_first_thirty_day1 = partner.curr_first_thirty_day1 + line.result_over

                        partner.curr_first_thirty_day1 =float_round(partner.curr_first_thirty_day1,precision_digits=3)


                    elif diff.days > 30 and diff.days <= 60:
                        partner.curr_thirty_sixty_days1 = partner.curr_thirty_sixty_days1 + line.result_over
                        partner.curr_thirty_sixty_days1 = float_round(partner.curr_thirty_sixty_days1, precision_digits=3)
                    elif diff.days > 60 and diff.days <= 90:
                        partner.curr_sixty_ninty_days1 = partner.curr_sixty_ninty_days1 + line.result_over
                        partner.curr_sixty_ninty_days1 = float_round(partner.curr_sixty_ninty_days1,
                                                                      precision_digits=3)
                    elif diff.days > 90 and diff.days <= 120:
                        partner.curr_ninty_onetwenty_days1 = partner.curr_ninty_onetwenty_days1 + line.result_over
                        partner.curr_ninty_onetwenty_days1 = float_round(partner.curr_ninty_onetwenty_days1,
                                                                      precision_digits=3)
                    elif diff.days > 120 and diff.days <= 150:
                        partner.curr_onetwenty_onefifty_days1 = partner.curr_onetwenty_onefifty_days1 + line.result_over
                        partner.curr_onetwenty_onefifty_days1 = float_round(partner.curr_onetwenty_onefifty_days1,
                                                                      precision_digits=3)
                    elif diff.days > 150 and diff.days <= 180:
                        partner.curr_onefifthy_oneeighty_days1 =partner.curr_onefifthy_oneeighty_days1 + line.result_over
                        partner.curr_onefifthy_oneeighty_days1 = float_round(partner.curr_onefifthy_oneeighty_days1,
                                                                      precision_digits=3)
                    else:
                        if diff.days > 180:
                            partner.curr_oneeighty_plus_days1 = partner.curr_oneeighty_plus_days1 + line.result_over
                            partner.curr_oneeighty_plus_days1 = float_round(partner.curr_oneeighty_plus_days1,
                                                                          precision_digits=3)
                 if line.currency_id.name == 'USD':

                    diff = today - line.invoice_date

                    if diff.days <= 30 and diff.days >= 0:

                        partner.curr_first_thirty_usd = partner.curr_first_thirty_usd + line.result_over

                        partner.curr_first_thirty_usd = float_round(partner.curr_first_thirty_usd, precision_digits=3)


                    elif diff.days > 30 and diff.days <= 60:
                        partner.curr_thirty_sixty_usd = partner.curr_thirty_sixty_usd + line.result_over
                        partner.curr_thirty_sixty_usd = float_round(partner.curr_thirty_sixty_usd,
                                                                      precision_digits=3)
                    elif diff.days > 60 and diff.days <= 90:
                        partner.curr_sixty_ninty_usd = partner.curr_sixty_ninty_usd + line.result_over
                        partner.curr_sixty_ninty_usd = float_round(partner.curr_sixty_ninty_usd,
                                                                     precision_digits=3)
                    elif diff.days > 90 and diff.days <= 120:
                        partner.curr_ninty_onetwenty_usd = partner.curr_ninty_onetwenty_usd + line.result_over
                        partner.curr_ninty_onetwenty_usd = float_round(partner.curr_ninty_onetwenty_usd,
                                                                         precision_digits=3)
                    elif diff.days > 120 and diff.days <= 150:
                        partner.curr_onetwenty_onefifty_usd = partner.curr_onetwenty_onefifty_usd + line.result_over
                        partner.curr_onetwenty_onefifty_usd = float_round(partner.curr_onetwenty_onefifty_usd,
                                                                            precision_digits=3)
                    elif diff.days > 150 and diff.days <= 180:
                        partner.curr_onefifthy_oneeighty_usd = partner.curr_onefifthy_oneeighty_usd + line.result_over
                        partner.curr_onefifthy_oneeighty_usd = float_round(partner.curr_onefifthy_oneeighty_usd,
                                                                             precision_digits=3)
                    else:
                        if diff.days > 180:
                            partner.curr_oneeighty_plus_usd = partner.curr_oneeighty_plus_usd + line.result_over
                            partner.curr_oneeighty_plus_usd = float_round(partner.curr_oneeighty_plus_usd,
                                                                            precision_digits=3)
        return

    @api.depends('curr_oneeighty_plus_days1','curr_onefifthy_oneeighty_days1','curr_onetwenty_onefifty_days1','curr_ninty_onetwenty_days1', 'curr_sixty_ninty_days1', 'curr_thirty_sixty_days1', 'curr_first_thirty_day1')
    def cur_compute_total(self):
        for partner in self:
            partner.curr_total1 = 0.0
            partner.curr_total1 =partner.curr_oneeighty_plus_days1 +partner.curr_onefifthy_oneeighty_days1 +partner.curr_onetwenty_onefifty_days1 +partner.curr_ninty_onetwenty_days1 + partner.curr_sixty_ninty_days1 + partner.curr_thirty_sixty_days1 + partner.curr_first_thirty_day1
        return

    @api.depends('curr_first_thirty_usd', 'curr_thirty_sixty_usd','curr_sixty_ninty_usd','curr_ninty_onetwenty_usd','curr_onetwenty_onefifty_usd','curr_onefifthy_oneeighty_usd','curr_oneeighty_plus_usd')
    def cur_compute_total_usd(self):
        for partner in self:
            partner.curr_usd = 0.0
            partner.curr_usd = partner.curr_oneeighty_plus_usd + partner.curr_onefifthy_oneeighty_usd + partner.curr_onetwenty_onefifty_usd + partner.curr_ninty_onetwenty_usd + partner.curr_sixty_ninty_usd + partner.curr_thirty_sixty_usd + partner.curr_first_thirty_usd


