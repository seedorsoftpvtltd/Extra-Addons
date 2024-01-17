from odoo import fields, models, api, _


class HrEmployee(models.Model):
    _inherit = "res.company"

    @api.model
    def onboardings_step1_action(self):
        idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Configuration'),
            'res_model': 'hr.leave.type',
            'view_mode': 'tree',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
        }

    @api.model
    def onboardings_Allocation1_action(self):
        idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Allocations'),
            'res_model': 'hr.leave.allocation',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'tree'], [False, 'list'], [False, 'form']],
        }


    @api.model
    def onboarding_step2_action(self):
        idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Allocate'),
            'res_model': 'automatic.leave.allocation',
            'view_mode': 'tree',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
        }


    @api.model
    def onboarding_approve2_action(self):
        idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Approve'),
            'res_model': 'hr.leave',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'tree'], [False, 'list'], [False, 'form']],
        }
