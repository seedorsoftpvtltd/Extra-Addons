from odoo import fields, models, api, _


class HrEmployee(models.Model):
    _inherit = "res.company"

    @api.model
    def onboardings_jobrelocation_action(self):
        # idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Customers'),
            'res_model': 'res.partner',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],

        }

    @api.model
    def onboardings_step_jobrelocation_import_action(self):
        # idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Import'),
            'res_model': 'document.attach',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
        }

    @api.model
    def onboardings_jobrelocationstep2_action(self):
        # idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        domain = [('type', '=', 'service')]
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Services'),
            'res_model': 'product.template',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
            'domain': domain,
        }


    @api.model
    def onboarding_jobrelocationstep4_action(self):
        # idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Jobs'),
            'res_model': 'freight.operation',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
        }


    @api.model
    def onboarding_jobrelocationstep3_action(self):
        # idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Jobs'),
            'res_model': 'freight.operation',
            'view_mode': 'form',
            'limit': 99999999,
            'views': [[False, 'form'], [False, 'list'], [False, 'kanban']],
        }


    @api.model
    def onboarding_jobrelocationapprove5_action(self):
        # idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoices'),
            'res_model': 'account.move',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
        }



