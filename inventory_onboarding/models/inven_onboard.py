from odoo import fields, models, api, _


class HrEmployee(models.Model):
    _inherit = "res.company"

    @api.model
    def onboardings_step_inventory_action(self):
        # idd = self.env.ref('stock.view_location_tree2').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Locations'),
            'res_model': 'stock.location',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
        }

    @api.model
    def onboardings_Allocation1_inventory_action(self):
        # idd = self.env.ref('product_harmonized_system.hs_code_view_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('H.S Code'),
            'res_model': 'hs.code',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
        }


    @api.model
    def onboarding_step2_action_inventory(self):
        # idd = self.env.ref('uom.product_uom_tree_view').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Unit of Measure'),
            'res_model': 'uom.uom',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
        }


    @api.model
    def onboarding_approve2_action_inventory(self):
        # idd = self.env.ref('product.product_template_kanban_view').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Goods'),
            'res_model': 'product.template',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
            'domain': [('type', '=', 'product')],
        }

    @api.model
    def onboarding_approve5_action_inventory(self):
        # idd = self.env.ref('document_attach.document_attach_kanban').id
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
    def onboarding_approve3_action_inventory(self):
        # idd = self.env.ref('product.product_product_tree_view').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Services'),
            'res_model': 'product.template',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
            'domain': [('type', '=', 'service')],
        }

    @api.model
    def onboarding_approve4_action_inventory(self):
        # idd = self.env.ref('document_attach.document_attach_kanban').id
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
