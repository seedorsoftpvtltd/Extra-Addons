from odoo import models, fields, api, _
import re
from odoo.exceptions import AccessError, UserError, ValidationError
import logging
from lxml import etree
_logger = logging.getLogger(__name__)

class MultiContainer(models.Model):
    _name = "multiple.container"


    # multi_container_no = fields.Char(string="Container No")
    company_id = fields.Many2one('res.company', string='Company', readonly=True)

    container = fields.Many2one('freight.container', string="Container Type")

    order_id = fields.Many2one('warehouse.order', string='Order Reference', index=True,
                               ondelete='cascade')
    picking_id = fields.Many2one('stock.picking', string='Picking Reference',index=True,
                               ondelete='cascade')

    container_serial_no = fields.Char(string='Container No')

    agent_seal = fields.Char(string='Agent Seal')

    developer_seal = fields.Char(string="Developer Seal")

    custom_seal = fields.Char(string='Custom Seal')

    truck_no = fields.Char(string='Truck No')


    @api.constrains('container_serial_no')
    def constraint_serial_numner(self):
        _logger.info("Multiple Container Constraints")
        tag = self.env['container.pattern'].search([('country_id.id','=',self.order_id.company_id.country_id.id or self.picking_id.company_id.country_id.id)])
        for rec in self:
            if rec.order_id.x_transport == 'ocean':
                if tag.country_id:
                    if not re.match(tag.pattern, str(rec.container_serial_no)):
                        raise ValidationError(f"Container Serial Number should be in a correct format. Example {tag.example}")
                else:
                    raise UserError(f"{self.order_id.company_id.country_id.name} container pattern is not created.")
        return True