from odoo.http import request
from odoo import api, fields, models, tools, osv, http, _
import odoo.osv.osv
from odoo.exceptions import ValidationError, UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    pay_inv = fields.Boolean(string='Active')


class PaymentWizard(models.TransientModel):
    _inherit = "sh.payment.wizard"

    def add_payment_wizardd(self):
        print('kkkkkkkkkkkkk')
        # vals = {
        #     (
        #         'pay_inv': False,
        #     )
        # }
        # self.env['account.move'].search([]).write(vals)

        if self.sh_move_line_ids.filtered(lambda x: x.sh_boolean == True):

            payment_lines = self.sh_move_line_ids.filtered(
                lambda x: x.sh_boolean)
            print(payment_lines)

            if payment_lines:
                
                for payment_line in payment_lines:
                    if payment_line.move_line_id:

                        lines = payment_line.move_line_id
                        ding = self.sh_account_move_ids.search([('pay_inv','=',True)])
                        lines += ding.line_ids.filtered(
                                 lambda line: line.account_id == lines[0].account_id and not line.reconciled )

                        # lines += self.sh_account_move_ids.line_ids.filtered(
                        #     lambda line: line.account_id == lines[0].account_id and not line.reconciled )

                        print(lines,'lines')
                        print('--------------------')
                        # print(ding.pay_inv)
                        ding.pay_inv = False
                        # print(ding.pay_inv)

                        print('--------------------')


                        lines.reconcile()


