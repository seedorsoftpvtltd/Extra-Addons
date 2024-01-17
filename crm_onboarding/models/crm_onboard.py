from odoo import fields, models, api, _


class HrEmployee(models.Model):
    _inherit = "res.company"

    @api.model
    def onboardings_step_crm_action(self):
        # idd = self.env.ref('crm.view_crm_lead_kanban').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Leads'),
            'res_model': 'crm.lead',
            'view_mode': 'form',
            'limit': 99999999,
            'views': [[False, 'form'], [False, 'list'], [False, 'kanban']],
        }



    @api.model
    def onboardings_step_crm_import_action(self):
        # idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Import'),
            'res_model': 'document.attach',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'tree'], [False, 'form']],
        }

    @api.model
    def onboarding_approve2_action_crm(self):
        # idd = self.env.ref('sale.view_sale_order_kanban').id
        company = self.env.company
        domain = [('type','=','opportunity')]
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Opportunities'),
            'res_model': 'crm.lead',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'tree'], [False, 'form']],
            'domain': domain
        }





