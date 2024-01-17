from odoo import fields, models, api, _


class HrEmployee(models.Model):
    _inherit = "res.company"

    @api.model
    def onboarding_action_asn_create_approve(self):
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
    def onboarding_action_asn_import_approve(self):
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
    def onboarding_action_asn_create_approve1(self):
        # idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Products'),
            'res_model': 'product.template',
            'view_mode': 'kanban',
            'limit': 80,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
        }

    @api.model
    def onboarding_action_asn_create_approve2(self):
        # idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Advance Shipping'),
            'res_model': 'warehouse.order',
            'view_mode': 'form',
            'limit': 99999999,
            'views': [[False, 'form'], [False, 'list'], [False, 'kanban']],
        }


    @api.model
    def onboarding_action_asn_create_approve3(self):
        # idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        domain = [('picking_type_id.code', '=', 'incoming')]
        return {
            'type': 'ir.actions.act_window',
            'name': _('Goods Receive Note'),
            'res_model': 'stock.picking',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'tree'], [False, 'list'], [False, 'form']],
            'domain': domain,
        }

