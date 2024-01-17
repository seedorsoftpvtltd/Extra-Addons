from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class pickingcharge(models.Model):
    _inherit = "stock.picking"

    charge_lines = fields.One2many('service.charges','delivery_idd')

    @api.model
    def create(self, vals):
        res = super(pickingcharge, self).create(vals)
        for rec in self:
            for line in rec.charge_lines:
                line.delivery_idd = rec.id
        return res

class servicecharge(models.Model):

    _name = "service.charges"
    _description = "Sevices"

    product_id = fields.Many2one("product.product", string="Service")
    delivery_idd = fields.Many2one("stock.picking", string="Delivery ID")
    partner_id = fields.Many2one("res.partner", string="Partner")
    invoice_id = fields.Many2one("account.move", string="Invoice")
    inv_line_id = fields.Many2one("account.move.line", string="Invoice Line")
    # bill_id = fields.Many2one("account.move", string="Bill")
    # bill_line_id = fields.Many2one("account.move.line", string="Bill Line")
    qty = fields.Integer(string="QTY", default=1)
    # uom_id = fields.Many2one("uom.uom", string="Unit of Mesure")
    list_price = fields.Float(string="Sale Price")
    # cost_price = fields.Float(string="Cost")
    sale_total = fields.Float(
        compute="_compute_sale_total", string="Sale Total", store=True
    )
    # cost_total = fields.Float(
    #     compute="_compute_cost_total", string="Cost Total", store=True
    # )
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)



    @api.constrains("qty", "list_price")
    def _check_qty_and_price(self):
        """Constrain to check qty and price."""
        for service in self:
            if service.qty < 0:
                raise UserError(_("You can't enter Negative QTY for services!!"))
            if service.list_price < 0:
                raise UserError(
                    _(
                        "You can't enter Sale Price in Negative \
                    for service!!"
                    )
                )
##            if service.cost_price < 0:
#                raise UserError(
#                    _(
#                        "You can't enter Cost Price in Negative \
#                    for service!!"
#                    )
#                )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        """Onchange to update list and cost price."""
        if self.product_id:
            self.update(
                {
                    "list_price": self.product_id.list_price or 0.0,
#                    "cost_price": self.product_id.standard_price or 0.0,
                }
            )

    @api.depends("qty", "list_price")
    def _compute_sale_total(self):
        """Compute total sale amount."""
        for service in self:
            service.sale_total = service.qty * service.list_price or 0.0

    # @api.depends("qty", "cost_price")
    # def _compute_cost_total(self):
    #     """Compute total cost amount."""
    #     for service in self:
    #         service.cost_total = service.qty * service.cost_price or 0.0
