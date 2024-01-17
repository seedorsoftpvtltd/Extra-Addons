from odoo import fields, models, api, _

class GoogleSheet(models.Model):
    _inherit = "google.spreadsheet.import"

    @api.model
    def onboarding_login_action(self):
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step2_state')
        return {
            'type': 'ir.actions.act_url',
            'url': "https://www.google.com",
            'target': 'new',
            'res_id': self.id,
        }