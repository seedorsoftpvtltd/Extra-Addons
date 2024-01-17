from odoo import api, fields, models, tools, _


class CustomDashboardinh(models.Model):
    _inherit = 'custom.dashboard'

    def action_import_warehouse_order(self):
        return {
            'name': _('Import warehouse Order'),
            'view_type': 'form',
            "view_mode": 'form',
            'res_model': 'import.warehouse.order',
            'type': 'ir.actions.act_window',
            'target': 'new',

        }
