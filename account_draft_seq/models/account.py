from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import formatLang, format_date, get_lang
class AccountMove(models.Model):
    _inherit='account.move'


    # name = fields.Char(string='Number', readonly=True,required=True, copy=False,
    #                    default=lambda self: self.env['ir.sequence'].next_by_code('cust.inv'))


    # sequence = fields.Char(string='Number', readonly=True,required='False', copy=False)


    @api.model_create_multi
    def create(self,vals_list):
        # print("fuuuuuuuuuuuu")
        # print(self.type)

        moves = super(AccountMove, self).create(vals_list)

        if moves.type =='out_invoice':
                        # print("hiiiiiiiiiii")
                        moves["name"] = self.env['ir.sequence'].next_by_code('cust.inv')
                        # print(moves.name)
        elif moves.type == 'in_invoice':
                        moves["name"] = self.env['ir.sequence'].next_by_code('vend.bill')
        elif moves.type == 'out_refund':
                        moves["name"] = self.env['ir.sequence'].next_by_code('cust.credit')
        elif moves.type == 'in_refund':
                        moves["name"] = self.env['ir.sequence'].next_by_code('vend.credit')
        #elif moves.type == 'out_receipt':
                        #moves["name"] = self.env['ir.sequence'].next_by_code('cust.receipt')
        #elif moves.type == 'in_receipt':
                        #moves["name"] = self.env['ir.sequence'].next_by_code('vend.receipt')
        return moves




    


    def unlink(self):
        for rec in self:
            if rec.state not in ('draft', 'cancel'):
                raise UserError(_("You cannot delete an entry which has been posted once."))
        return models.Model.unlink(self)
