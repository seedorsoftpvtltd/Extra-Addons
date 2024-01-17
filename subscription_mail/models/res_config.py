from odoo import api, fields, models, _
from odoo.exceptions import Warning

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    remainder_days= fields.Integer(string="Remainder Days For Monthly Subscription" )
    remainder_year_days = fields.Integer(string="Remainder Days For Yearly Subscription")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        config_parameter = self.env['ir.config_parameter'].sudo()
        remainder_days= (config_parameter.get_param('subscription_mail.remainder_days'))
        remainder_year_days = (config_parameter.get_param('subscription_mail.remainder_year_days'))
        res.update(remainder_days=int(remainder_days))
        res.update(remainder_year_days=int(remainder_year_days))
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        config_parameter = self.env['ir.config_parameter'].sudo()
        config_parameter.set_param('subscription_mail.remainder_days', self.remainder_days)
        config_parameter.set_param('subscription_mail.remainder_year_days', self.remainder_year_days)