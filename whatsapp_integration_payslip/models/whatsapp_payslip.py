from odoo import models, fields, api,_
import base64
from odoo.http import request

class whataspp_payslip(models.Model):

    _inherit = ['hr.payslip']
    attachment_ids = fields.Many2one('ir.attachment', string='Attachments')
    mobile_number = fields.Char(required=True, store=True)




    def whatsapp_payslip(self):
        for rec in self:
            attac = self.env["ir.attachment"].search([('res_model', '=', 'hr.payslip'), ('res_id', 'in', rec.ids)])
            rec['attachment_ids'] = attac


        if self.employee_id:
            self.env['wizard.whatsapp.payslip'].write({'mobile_number': self.employee_id.mobile_phone})
            return{'type': 'ir.actions.act_window',
                    'name': _('Whatsapp Message'),
                    'res_model': 'wizard.whatsapp.payslip',
                    'target': 'new',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'context': {
                    'default_attachment_ids': rec.attachment_ids.id,
                    'default_mobile_number': self.employee_id.mobile_phone,
                       }

                     }