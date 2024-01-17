from odoo import api, fields, models, _


class res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'

    remove_sesions = fields.Integer("Scheduled remove old sessions", default=7)
    send_mail = fields.Boolean('Send Mail When New Session Start', default=True)

    @api.model
    def get_values(self):
        res = super(res_config_settings, self).get_values()

        res['remove_sesions'] = int(self.env['ir.config_parameter'].sudo().get_param('advanced_session_management.remove_sesions', default=7))
        res['send_mail'] = self.env['ir.config_parameter'].sudo().get_param('advanced_session_management.send_mail', default='False') == 'True'

        return res

    @api.model
    def set_values(self):
        
        if self.remove_sesions <= 0:
            remove_sesions = 7 
        else:
            remove_sesions = self.remove_sesions
        self.env['ir.config_parameter'].sudo().set_param('advanced_session_management.remove_sesions', remove_sesions)
        self.env['ir.config_parameter'].sudo().set_param('advanced_session_management.send_mail', str(self.send_mail))

        return super(res_config_settings, self).set_values()


class ir_config_parameter(models.Model):
    _inherit = 'ir.config_parameter'

    def delete_record_ao(self):
        self.search([('key','=','disable_log')],limit=1).unlink()

