from datetime import datetime
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

#
class FreightOperationserviceExtend(models.Model):
    _inherit = "operation.service"
    # related = 'operation_id.isinvoice'
    isinvoice = fields.Boolean(string="Select Invoice",store=True,copy=False)
    isbill = fields.Boolean(string="Select Bill",)
    customer_id = fields.Many2one(related='operation_id.customer_id',
        string='Customer',
        readonly=True,)
#

    # @api.model
    # def _default_has_down_payment(self):
    #     if self._context.get('active_model') == 'operation.service' and self._context.get('active_id', False):
    #         service = self.env['operation.service'].browse(self._context.get('active_id'))
    #         return service.isinvoice == False
    #     return False
    #
    # @api.depends('other_field')
    # def _compute_isinvoice(self):
    #     for service in self:
    #         if service.other_field == 'some_value':
    #             service.isinvoice = True
    #         else:
    #             service.isinvoice = False
    # @api.onchange('isinvoice')
    # def onchange_bool_field(self):
    #     if self.isinvoice:
    #         # Set the corresponding field value in the associated model or record
    #         self.env['operation.service'].write({'isinvoice': True})
    #     else:
    #         # Set the corresponding field value to False
    #         self.env['operation.service'].write({'isinvoice': False})
    # @api.onchange('isinvoice')
    # def _onchange_isinvoice(self):
    #     if self.isinvoice:
    #         active_ids = self._context.get('active_ids', [])
    #         services = self.env['operation.service'].browse(active_ids)
    #         print(services,'ser')
    #         services.write({'isinvoice': True})

    @api.depends('bill_id')
    def _compute_isbill(self):
        for service in self:
            print(service.bill_id, ' service.isbill1')
            service.isbill = bool(service.bill_id)
            print(bool(service.bill_id), 'bool(service.bill_id)')
            # service.vendor_id.readonly = service.isbill
            # service.uom_id.readonly = service.isbill
            # service.qty.readonly =not service.isbill

# #
#     @api.depends('isinvoice')
#     def _compute_isinvoice(self):
#         for service in self:
#             print(service.isinvoice, ' service.isinvoice')
#             service.isinvoice = service.isinvoice == True
#             print(bool(service.isinvoice), ' bool(service.isinvoice)')
            # if service.invoice_id:
            #     self.vendor_id.readonly = True
            #     self.uom_id.readonly = True
            # else:
            #     self.uom_id.readonly = False

            # print(service.uom_id.readonly, ' service.uom_id.readonly')



