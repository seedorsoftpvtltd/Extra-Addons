from odoo import models, fields, api, _


class Stockpicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def _keeps(self):
        res = super(Stockpicking, self)._keeps()
        for rec in self:
            move_line = self.env['stock.move.line'].search([('picking_id', '=', rec.id)])
            for line in move_line:
                if not line.agreement_id:
                    line.agreement_id = rec.agreement_id.id
        return res


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    charge_lines = fields.Many2one('agreement.charges', string="Charge Line",
                                   domain="[('agreement_id','=',agreement_id)]")
    agreement_id = fields.Many2one('agreement', string="Agreement", readonly=False, store=True)
    charge_unit_type = fields.Many2one('charge.types', string="Charge Type", store=True, related='charge_lines.charge_unit_type')

    # @api.depends('picking_id')
    # def _compute_agreement(self):
    #     for rec in self:
    #         if rec.picking_id.agreement_id:
    #             rec.agreement_id = rec.picking_id.agreement_id.id
    #         else:
    #             rec.agreement_id = None

    @api.model
    def create(self, vals):
        res = super(StockMoveLine, self).create(vals)
        if res.picking_id:
            res.update(
                {'agreement_id': res.picking_id.agreement_id.id})
        return res

    # @api.model
    # def write(self, vals):
    #     res = super(StockMoveLine, self).create(vals)
    #     if res.picking_id:
    #         res.update(
    #             {'agreement_id': res.picking_id.agreement_id.id})
    #     return res

    @api.model
    def default_get(self, vals):
        res = super(StockMoveLine, self).default_get(vals)
        print(self._context)
        if self.env.context.get('picking_type_code'):
            if self.env.context.get('active_model') == 'warehouse.order':
                ware = self.env['warehouse.order'].browse(self.env.context.get('active_id')).name
                if ware:
                    picking = self.env['stock.picking'].search([('origin', '=', ware)])
                    if picking:
                        self.agreement_id = picking.agreement_id.id
            else:
                if self.env.context.get('params'):
                    if self.env.context.get('params')['model']:
                        if self.env.context.get('params')['model'] == 'stock.picking':
                            if self.env.context.get('params')['id']:
                                picking = self.env['stock.picking'].browse(self.env.context.get('params')['id'])
                                if picking:
                                    self.agreement_id = picking.agreement_id.id
        return res
