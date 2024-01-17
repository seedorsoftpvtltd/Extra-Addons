from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class UpdateInvoiceWizard(models.TransientModel):
    _name = "update.invoice.wizard"
    _description = "Revoke"

    # isinvoice = fields.Boolean(string="Is Invoice", )
    # isbill = fields.Boolean(string="Is Bill", )

    service_ids = fields.One2many(
        "invoice.wizard", "service_line_id", string="Services"
    )
    partner_id = fields.Many2one('res.partner', string='Vendor')
    customer_id = fields.Many2one('res.partner', string='Vendor')
    isinvoice = fields.Boolean(string="Select Invoice")
    product_id = fields.Many2one('product.product',String='Product')
    consignee_id = fields.Many2one("res.partner", string="Consignee")
    operation_id = fields.Many2one("freight.operation", "Freight Operation")
    routes_ids = fields.One2many("operation.route", "operation_id", string="Routes")
    link_id=fields.Many2one('operation.service',string='Link')
    triger = fields.Boolean('trigger', )
    invoice = fields.Boolean('invoice')
    revoke_invoice=fields.Boolean('Revoke')
    # revoke_bill = fields.Boolean('Revoke Bill')
    qty = fields.Float(String='Quantity', readonly=True)
    list_price =fields.Float(String='Sale Price', readonly=True)
    cost_price = fields.Float(String='Cost Price', readonly=True)
    invoice_id = fields.Many2one('account.move', String='Invoice', readonly=True)

    service_bill_ids = fields.One2many(
        "invoice.wizard", "service_line_bill_id", string="Services"
    )
    partner_ids = fields.Many2one('res.partner', string='Vendor')
    product_ids = fields.Many2one('product.product', String='Product')
    revoke_bill = fields.Boolean('Revoke Bill')
    qtys = fields.Float(String='Quantity', readonly=True)
    list_prices = fields.Float(String='Sale Price', readonly=True)
    bill_id = fields.Many2one('account.move', String='Bill', readonly=True)
    @api.model
    def default_get(self, default_fields):
        res = super(UpdateInvoiceWizard, self).default_get(default_fields)
        data = self.env['freight.operation'].browse(self._context.get('active_ids', []))
        update = []
        update1 = []

        for record in data.service_ids:
            if record.isinvoice == True:
              if record.invoice_id.state == 'draft':
                update.append((0, 0, {
                    'vendor_id': record.vendor_id.id,
                    'isinvoice': record.isinvoice,
                    'invoice_id': record.invoice_id.id,
                    'customer_id':record.customer_id.id,
                    'product_id': record.product_id.id,
                    'qty': record.qty,
                    'list_price': record.list_price,
                    'cost_price':record.cost_price,
                }))
        res.update({'service_ids': update})
        for record in data.service_bill_ids:
            if record.isbill == True:
              if record.bill_id.state == 'draft':
                update1.append((0, 0, {
                    'vendor_id': record.vendor_id.id,
                    'product_id': record.product_id.id,
                    'bill_id': record.bill_id.id,
                    'qty': record.qty,
                    'list_price': record.list_price,
                    'cost_price':record.cost_price,
                }))

        res.update({'service_bill_ids': update1})
        return res

    def revoke_inv(self):
        revoke = []
        revoke_bill = []
        ids=[]
        ids1 = []
        updated_service_ids = []
        data = self.env['freight.operation'].browse(self._context.get('active_ids', []))
        for rec in self.service_ids:
                print("wwwwwwwwwwwwwwww")
                print(rec)
                revoke.append(rec.revoke_invoice)
        for rec in self.service_bill_ids:
                revoke_bill.append(rec.revoke_bill)
        print(revoke)
        print(revoke_bill)
        # if True not in service:
        #     # Display validation message or raise an exception
        #     raise ValidationError("Please select any of the above services to generate invoice")
        for line in range(0, len(data.service_ids)):
            if data.service_ids[line].isinvoice == True and data.service_ids[line].invoice_id.state == 'draft':
                ids.append(data.service_ids[line])
                print(ids)
        for recc in range(0, len(ids)):
                print(recc)
                ids[recc].update({'revoke_invoice': revoke[recc]})
        for line in range(0, len(data.service_bill_ids)):
            if data.service_bill_ids[line].isbill == True and data.service_ids[line].bill_id.state == 'draft':

                ids1.append(data.service_bill_ids[line])
                print(ids1)
        for recc1 in range(0, len(ids1)):
                print(recc1)
                ids1[recc1].update({
                                  'revoke_bill': revoke_bill[recc1]})

        # for recc1 in range(0, len(ids)):
        #
        #         ids[recc1].update({'revoke_bill': revoke[recc1]})


class UpdateInvoice(models.TransientModel):
    _name = 'invoice.wizard'

    service_line_id = fields.Many2one('update.invoice.wizard')
    service_line_bill_id = fields.Many2one('update.invoice.wizard')

    vendor_id = fields.Many2one('res.partner', string="Vendor",readonly=True)
    isinvoice = fields.Boolean(string="Is Invoice")
    customer_id=fields.Many2one('res.partner', string="Customer",readonly=True)
    product_id = fields.Many2one('product.product', String='Service',readonly=True)
    qty = fields.Float(String='Quantity', readonly=True)
    list_price =fields.Float(String='Sale Price', readonly=True)
    cost_price = fields.Float(String='Cost Price', readonly=True)
    revoke_invoice = fields.Boolean(string="Revoke Invoice", store=True, copy=False)
    revoke_bill = fields.Boolean(string="Revoke Bill", store=True, copy=False)
    invoice_id=fields.Many2one('account.move', String='Invoice',readonly=True)
    bill_id = fields.Many2one('account.move', String='Bill', readonly=True)