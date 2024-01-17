from odoo import api, models, fields, _

class ReportWizard(models.TransientModel):
    _name = 'report.wizard'

    partner_id = fields.Many2one('res.partner', string="Customer")
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    overall_report = fields.Boolean('View All Records')

    def view_stock_movement(self):
        if self.partner_id:
            domain = [('owner_id', '=', self.partner_id.id), ('create_date', '>=', self.start_date),
                          ('create_date', '<=', self.end_date), ("on_hand","=",True), ]
            return {
                'type': 'ir.actions.act_window',
                'name': _('Stock Balance Report'),
                'res_model': 'stock.quant',
                'view_mode': 'tree',
                'limit': 99999999,
                'search_view_id': self.env.ref('stock.view_stock_quant_tree').id,
                'domain': domain,
            }
        else:
            domain = [('create_date', '>=', self.start_date),
                      ('create_date', '<=', self.end_date), ("on_hand", "=", True), ]
            return {
                  'type': 'ir.actions.act_window',
                  'name': _('Stock Balance Report'),
                  'res_model': 'stock.quant',
                  'view_mode': 'tree',
                  'limit': 99999999,
                  'search_view_id': self.env.ref('stock.view_stock_quant_tree').id,
                  'domain': domain,
              }

    def view_stock_movementt(self):

        # domain = [('picking_code','in',['incoming','outgoing']), ('x_job_type','=','Warehouse')]
        domain = [("on_hand","=",True)]
        return {
            'type': 'ir.actions.act_window',
            'name': _('Stock Balance Report'),
            'res_model': 'stock.quant',
            'view_mode': 'tree',
            'limit': 99999999,
            'search_view_id': self.env.ref('stock.view_stock_quant_tree').id,
        # 'views': ['list'],
            'domain': domain,
        }
