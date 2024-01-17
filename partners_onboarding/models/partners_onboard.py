from odoo import fields, models, api, _


class HrEmployee(models.Model):
    _inherit = "res.company"

    @api.model
    def onboardings_step11_action(self):
        idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        domain = [('is_company', '=', False)]
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Individual'),
            'res_model': 'res.partner',
            'view_mode': 'form',
            'limit': 99999999,
            'views': [[False, 'form'], [False, 'list'], [False, 'kanban']],
            'domain': domain,
        }

    @api.model
    def onboardings_import_action(self):
        idd = self.env.ref('hr.view_department_tree').id
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
    def onboardings_Allocation11_action(self):
        idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        domain = [('is_company', '=', True)]
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Companies'),
            'res_model': 'res.partner',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'tree']],
            'domain': domain,
        }


    @api.model
    def onboarding_step12_action(self):
        idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        domain = [('agent', '=', True)]
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Agents'),
            'res_model': 'res.partner',
            'view_mode': 'tree',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
            'domain': domain,

        }

    @api.model
    def onboarding_approve11_action(self):
        idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        domain = [('customer_rank','>', 0)]
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        print('hlo')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Customers'),
            'res_model': 'res.partner',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'tree'], [False, 'form']],
            'domain': domain,
        }

    @api.model
    def onboarding_approve12_action(self):
        idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        domain = [('supplier_rank','>', 0)]
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Vendors'),
            'res_model': 'res.partner',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'tree'], [False, 'form']],
            'domain': domain,
        }




