from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'account.move'

    jobno = fields.Char(string='Job No',compute='_jobno')

    def _jobno(self):
        moves = self.env['sale.order'].search([('invoice_ids','=',self.id)])
        print(moves)
        if moves:
            self['jobno'] = moves.jobnumber
        else:
            self['jobno'] = ''
