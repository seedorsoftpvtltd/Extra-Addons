from odoo import models, fields, api, _

class GoodsIssueOrder(models.Model):
    _inherit = "goods.issue.order"

    @api.model
    def onboard_create_gio(self):
        view_id = self.env.ref('gio.views_order_form').id
        context = self._context.copy()
        return {
            'name': 'New Goods',
            'view_type': 'form',
            'view_mode': 'tree',
            'views': [(view_id, 'form')],
            'res_model': 'goods.issue.order',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'current',
            'context': context,
        }