from odoo import models, fields, api, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _get_default_journal(self):
        res = super(AccountMove, self)._get_default_journal()
        default_journal = self.env['account.journal']
        # if type(self.type) == 'str':

        ir_fields = self.env['ir.model.fields'].search([('name', '=', 'journal_id'),
                                                        ('model', '=', 'account.move'),
                                                        ('relation', '=', 'account.journal')])
        print(self.type)
        if self.type:
            b = 'type=' + self.type
            ir_default = self.env['ir.default'].search([('field_id', '=', ir_fields.id),
                                                        ('condition', '=', b)])
            print(ir_default)
            if ir_default:
                if len(ir_default) > 1:
                    for value in ir_default:
                        if value.user_id.id == self.env.user.id:
                            ret_id = default_journal.browse(int(value.json_value))
                        else:
                            ret_id = default_journal.browse(int(value.json_value))
                    return ret_id

                else:

                    if ir_default.user_id.id == self.env.user.id:
                        return default_journal.browse(int(ir_default.json_value))
                    else:
                        return default_journal.browse(int(ir_default.json_value))
            else:
                return res
        else:
            return res
