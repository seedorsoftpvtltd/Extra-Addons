from odoo import fields, models, api, _

class GoogleSheet(models.Model):
    _inherit = "hr.resignation"

    @api.model
    def onboarding_step1_action(self):
        # idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Offboarding'),
            'res_model': 'hr.resignation',
            'view_mode': 'tree',
            'limit': 99999999,
            'views': [[False, 'list'], [False, 'form']],
        }

    @api.model
    def onboarding_plan2_action(self):
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step2_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Plans'),
            'res_model': 'hr.plan',
            'view_mode': 'tree',
            'views': [[False, 'list'], [False, 'form']],
        }

