from odoo import api, fields, models, tools, _

class JobNumber(models.Model):
    _inherit = 'sale.order'

    jobnumber = fields.Char(string="Job Number", readonly=False, required=True, copy=False, default='New')


    def action_confirm(self):
        result = super(JobNumber, self).action_confirm()
        self['jobnumber'] = self.env['ir.sequence'].next_by_code(
            'job.service') or 'New'

        return result

