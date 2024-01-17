from odoo import api, fields, models, _

class Res_Partner_Fiannce_payment(models.Model):
    _inherit = 'res.partner'
    def do_fcy_print(self):
        return self.env.ref('overdue_fcy_print.report_customer_fcy_print').report_action(self)
    def do_outstanding_print(self):
        return self.env.ref('overdue_fcy_print.report_customer_outstanding_print').report_action(self)
