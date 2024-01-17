from odoo import _, api, fields, models


class HbFleetInspectionTemplate(models.Model):
    _name = "fleet.vehicle.template"
    _description = "Fleet VehicleTemplate"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    model = fields.Many2one('fleet.vehicle.model',string="Model")
    template_line_ids = fields.One2many("fleet.vehicle.template.line", "template_idd", string="Template Lines",
                                        copy=True, auto_join=True, )


class HbFleetTemplateLine(models.Model):
    _name = "fleet.vehicle.template.line"
    _description = "Fleet Vehicle Template Line"

    template_id = fields.Many2one("fleet.vehicle.log.services", string="Template Reference")
    template_idd = fields.Many2one('fleet.vehicle.template', string='Template')
    service_prod = fields.Many2one("product.product", string="Item Selection")
    # uom = fields.Many2one('product.uom', string='UOM', related='service_prod.')
    qty = fields.Float('Quantity')



    # u = fields.Char(string="U")
    # qr = fields.Char(string="qr")
    # cs = fields.Char(string="cs")
    # rate = fields.Char(string="rate")
    cost = fields.Float(string="cost", related='service_prod.list_price')
    result = fields.Selection(
        [("todo", "Todo"), ("success", "Success"), ("failure", "Failure")],
        "Result",
        default="todo",
        readonly=True,
        required=True,
        copy=False,
    )
    statee = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancel", "Cancelled")],
        related="template_id.statee",
        string="Template Status",
        readonly=True,
        copy=False,
        store=True,
        default="draft",
    )

    def action_item_success(self):
        return self.write({"result": "success"})

    def action_item_failure(self):
        return self.write({"result": "failure"})


class HbFleetVehicleservices(models.Model):
    _inherit = "fleet.vehicle.log.services"

    template_id = fields.Many2one("fleet.vehicle.template", string="Template")
    template_line_ids = fields.One2many("fleet.vehicle.template.line","template_id", string="Template Lines", copy=True, auto_join=True )
    statee = fields.Selection([("draft", "Draft"), ("confirmed", "Confirmed"), ("cancel", "Cancelled")], string="Status",
                             copy=False, index=True, readonly=True, track_visibility="onchange", default="draft")

    result = fields.Selection(
        [("todo", "Todo"), ("success", "Success"), ("failure", "Failure")],
        " Result",
        default="todo",
        compute="_compute_result",
        readonly=True,
        copy=False,
        store=True,
    )

    @api.depends("template_line_ids", "statee")
    def _compute_result(self):
        for rec in self:
            if rec.template_line_ids:
                if any(l.result == "todo" for l in rec.template_line_ids):
                    rec.result = "todo"
                elif any(l.result == "failure" for l in rec.template_line_ids):
                    rec.result = "failure"
                else:
                    rec.result = "success"
            else:
                rec.result = "todo"

    def _compute_line_data_for_template_change(self, line):
        return {
            "service_prod": line.service_prod.id,
            "qty": line.qty,
            # "u":line.u,
            # "qr":line.qr,
            # "cs":line.cs,
            # "rate":line.rate,
            "cost":line.cost,
            "statee": "draft",
        }

    @api.onchange("template_id")
    def _onchange_template_id(self):
        if self.template_id:
            self.name = self.template_id.name
#            self.note = self.template_id.note

            lines = [(5, 0, 0)]
            for line in self.template_id.template_line_ids:
                data = self._compute_line_data_for_template_change(line)
                lines.append((0, 0, data))

            self.template_line_ids = lines
