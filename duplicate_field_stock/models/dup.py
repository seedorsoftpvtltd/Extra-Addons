from odoo import models, fields, api, _

class DuplicateField(models.Model):
    _inherit = "stock.move.line"

    x_volume = fields.Float(string="Volume Not In Use", related='move_id.x_volume')
    x_volu = fields.Float(string="Volume Not In Use", related="move_id.x_volume1")
    volume = fields.Float(string="Volume Not In Use", related='move_id.volume')
    loc = fields.Many2one('stock.location', 'Location Code Not Use', compute='_locloc')
    result_package_id = fields.Many2one(
        'stock.quant.package', 'Result Package',
        ondelete='restrict', required=False, check_company=True,
        domain="['|', '|', ('location_id', '=', False), ('location_id', '=', location_dest_id), ('id', '=', package_id)]",
        help="If set, the operations are packed into this package")
    gross_weight = fields.Float(string="Gross", related='move_id.gross_weight')


