# from odoo import models, fields, api
#
#
# class AccountMoveReversal(models.TransientModel):
#     _inherit = 'account.move.reversal'
#
#     def reverse_moves(self):
#         for rec in self:
#             res = self.env['account.move'].search([('id', '=', rec.move_id.id)])
#             if res:
#                 res.button_draft()

from odoo import models, api,_

class AccountMove(models.Model):
    _inherit = 'account.move'

    # def reverse_moves(self):
    #     print('sasd')
    #     for rec in self:
    #         res = self.env['account.move'].search([('id', '=', rec.move_id.id)])
    #         if res:
    #             res.button_draft()

    def _reverse_moves(self, default_values_list=None, cancel=False):
        res = super(AccountMove, self)._reverse_moves(default_values_list=default_values_list, cancel=cancel)

        res.button_draft()
        return res

#     def reverse_moves(self, date=None, journal_id=None):
#         print('asdasd')
        # for move in self:
        #     if move.state != 'draft':
        #         move.button_draft()
        #     move_lines_to_reconcile = move.mapped('line_ids').filtered(lambda line: not line.reconciled)
        #     move_lines_to_reconcile.sudo()._remove_move_reconcile()
        #     reverse_move = move.copy(default={
        #         'ref': move.ref and _('Reversal of: %s') % (move.ref,),
        #         'move_type': 'entry',
        #         'state': 'draft',
        #     })
        #     for line in reverse_move.line_ids:
        #         line.debit, line.credit = line.credit, line.debit
        #         line.name = _('Reversal of: ') + (line.name or '')
        #     reverse_move.post()
        # return True
