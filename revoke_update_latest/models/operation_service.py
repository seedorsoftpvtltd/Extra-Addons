from odoo import _, api, fields, models


class OperationServiceRevoke(models.Model):
    _inherit = "operation.service"
    # related = 'operation_id.isinvoice'
    revoke_invoice = fields.Boolean(string="Revoke Invoice",store=True,copy=False)
    revoke_bill = fields.Boolean(string="Revoke Bill", store=True, copy=False)


class FreightOP(models.Model):
    _inherit="freight.operation"
    service_bill_ids = fields.One2many(
        "operation.service", "operation_id", string="Services"
    )