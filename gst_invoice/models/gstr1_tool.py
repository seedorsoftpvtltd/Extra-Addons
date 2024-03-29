# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import base64
import json

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Gstr1Tool(models.Model):
    _name = "gstr1.tool"
    _description = "GSTR1 Tool"
    _inherit = ['mail.thread']

    def _get_gst_attachments(self):
        attachments = []
        if self.b2b_attachment:
            attachments.append(self.b2b_attachment.id)
        if self.b2bur_attachment:
            attachments.append(self.b2bur_attachment.id)
        if self.b2cs_attachment:
            attachments.append(self.b2cs_attachment.id)
        if self.b2cl_attachment:
            attachments.append(self.b2cl_attachment.id)
        if self.imps_attachment:
            attachments.append(self.imps_attachment.id)
        if self.impg_attachment:
            attachments.append(self.impg_attachment.id)
        if self.cdnr_attachment:
            attachments.append(self.cdnr_attachment.id)
        if self.export_attachment:
            attachments.append(self.export_attachment.id)
        if self.hsn_attachment:
            attachments.append(self.hsn_attachment.id)
        if self.json_attachment:
            attachments.append(self.json_attachment.id)
        return attachments

    @api.depends('b2b_attachment', 'b2cs_attachment', 'b2bur_attachment',
                 'b2cl_attachment', 'imps_attachment', 'impg_attachment',
                 'export_attachment', 'cdnr_attachment', 'hsn_attachment',
                 'json_attachment')
    def _get_attachment_count(self):
        attachments = self._get_gst_attachments()
        self.update({'attachment_count': len(attachments)})

    @api.depends('invoice_lines')
    def _get_invoice_count(self):
        for gst in self:
            invoices = []
            if gst.invoice_lines:
                invoices = gst.invoice_lines.ids
            gst.update({'invoices_count': len(invoices)})

    def _get_gst_type(self):
        return [('gstr1', 'GSTR1'), ('gstr2', 'GSTR2')]

    _gst_type_selection = lambda self, *args, **kwargs: self._get_gst_type(*args, **kwargs)

    name = fields.Char(string='GST Invoice')
    gst_type = fields.Selection(string='GST Type', selection=_gst_type_selection,
                                help="GST Typr. ex : ('gstr1', 'gstr2' ...)", default='gstr1')
    reverse_charge = fields.Boolean(
        string='Reverse Charge', help="Allow reverse charges for b2b invoices")
    counter_filing_status = fields.Boolean(string='Counter Party Filing Status', default=True,
        help="Select when counter party has filed for b2b and cdnr invoices")
    period_id = fields.Many2one('account.period', tracking=True, string='Period')
    status = fields.Selection(
        [('not_uploaded', 'Not uploaded'),
         ('ready_to_upload', 'Ready to upload'),
         ('uploaded', 'Uploaded to govt'), ('filed', 'Filed')],
        string='Status', default="not_uploaded", tracking=True,
        help="status will be consider during gst import, ")
    cgt = fields.Float(string='Current Gross Turnover', tracking=True, help="Current Gross Turnover")
    gt = fields.Float(string='Gross Turnover', tracking=True, help="Gross Turnover till current date")
    date_from = fields.Date(string='Date From', help="Date starting range for filter")
    date_to = fields.Date(string='Date To', help="Date end range for filter")
    invoice_lines = fields.Many2many('account.move', 'gst_account_invoice', 'gst_id', 'account_inv_id',
        string='Customer Invoices', help="Invoices belong to selected period.")
    b2b_attachment = fields.Many2one('ir.attachment', help="B2B Invoice Attachment")
    b2bur_attachment = fields.Many2one('ir.attachment', help="B2BUR Invoice Attachment")
    b2cs_attachment = fields.Many2one('ir.attachment', help="B2CS Invoice Attachment")
    b2cl_attachment = fields.Many2one('ir.attachment', help="B2CL Invoice Attachment")
    export_attachment = fields.Many2one('ir.attachment', help="Export Invoice Attachment")
    imps_attachment = fields.Many2one('ir.attachment', help="IMPS Invoice Attachment")
    impg_attachment = fields.Many2one('ir.attachment', help="IMPG Invoice Attachment")
    hsn_attachment = fields.Many2one('ir.attachment', help="HSN Data Attachment")
    cdnr_attachment = fields.Many2one('ir.attachment', help="CDNR Data Attachment")
    json_attachment = fields.Many2one('ir.attachment', help="json date attachment")
    attachment_count = fields.Integer(string='# of Attachments', compute='_get_attachment_count',
                                      readonly=True, help="Number of attachments")
    invoices_count = fields.Integer(string='# of Invoices', compute='_get_invoice_count',
                                    readonly=True, help="Number of invoices")
    itc_eligibility = fields.Selection([
        ('Inputs', 'Inputs'),
        ('Capital goods', 'Capital goods'),
        ('Input services', 'Input services'),
        ('Ineligible', 'Ineligible'),
    ], string='ITC Eligibility', default='Ineligible')
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                 required=True, readonly=True,
                                 default=lambda self: self.env.user.company_id)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('gstr1.tool')
        res = super(Gstr1Tool, self).create(vals)
        return res

    def unlink(self):
        for obj in self:
            if obj.status != "not_uploaded":
                raise UserError("GST invoice can't be delete as invoices are already generated.")
        res = super(Gstr1Tool, self).unlink()
        return res

    def write(self, vals):
        res = super(Gstr1Tool, self).write(vals)
        for obj in self:
            if obj.date_from and obj.date_to:
                if obj.period_id.date_start > obj.date_from or obj.period_id.date_start > obj.date_to or obj.period_id.date_stop < obj.date_to or obj.period_id.date_stop < obj.date_from:
                    raise UserError("Date should belong to selected period")
                if obj.date_from > obj.date_to:
                    raise UserError("End date should greater than or equal to starting date")
        return res

    def onchange(self, values, field_name, field_onchange):
        ctx = dict(self._context or {})
        ctx['current_id'] = values.get('id')
        res = super(Gstr1Tool, self.with_context(ctx)).onchange(values, field_name, field_onchange)
        return res

    def reset(self):
        totalInvoices = len(self.invoice_lines)
        if self.b2b_attachment:
            self.b2b_attachment.unlink()
        if self.b2bur_attachment:
            self.b2bur_attachment.unlink()
        if self.b2cl_attachment:
            self.b2cl_attachment.unlink()
        if self.b2cs_attachment:
            self.b2cs_attachment.unlink()
        if self.hsn_attachment:
            self.hsn_attachment.unlink()
        if self.cdnr_attachment:
            self.cdnr_attachment.unlink()
        if self.imps_attachment:
            self.imps_attachment.unlink()
        if self.impg_attachment:
            self.impg_attachment.unlink()
        if self.export_attachment:
            self.export_attachment.unlink()
        if self.json_attachment:
            self.json_attachment.unlink()
        self.status = 'not_uploaded'
        self.updateInvoiceStatus('not_uploaded')
        if self.gst_type == 'gstr1':
            self.fetchInvoices()
        elif self.gst_type == 'gstr2':
            self.fetchSupplierInvoices()
        body = '<b>RESET </b>: {} GST Invoices'.format(totalInvoices)
        self.message_post(body=_(body), subtype='mail.mt_comment')
        return True

    def action_view_invoice(self):
        invoices = self.mapped('invoice_lines')
        action = self.env.ref('gst_invoice.customer_invoice_list_action').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def action_view_attachment(self):
        attachments = self._get_gst_attachments()
        action = self.env.ref('gst_invoice.gst_attachments_action').read()[0]
        if len(attachments) > 1:
            action['domain'] = [('id', 'in', attachments)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.onchange('period_id', 'date_from', 'date_to')
    def _compute_invoice_lines(self):
        domain = {}
        filter = []
        ctx = dict(self._context or {})
        invoiceObjs = []
        if ctx.get('current_id'):
            filter = [('id', '!=', ctx.get('current_id'))]
        invoiceType = ['out_invoice', 'out_refund']
        if self.gst_type == 'gstr2':
            invoiceType = ['in_invoice', 'in_refund']
        invoiceObjs = self.getInvoiceObjs(filter, invoiceType)
        if invoiceObjs:
            self.updateGSTInvoiceLines(invoiceObjs)
            domain['invoice_lines'] = [('id', 'in', invoiceObjs.ids)]
        else:
            domain['invoice_lines'] = [('id', 'in', [])]
        return {'domain': domain}

    def fetchInvoices(self):
        ctx = dict(self._context or {})
        filter = [('id', '!=', self.id)]
        invoiceObjs = self.with_context(ctx).getInvoiceObjs(filter, ['out_invoice', 'out_refund'])
        self.invoice_lines = [(6, 0, invoiceObjs.ids)]
        if invoiceObjs:
            self.updateInvoiceCurrencyRate(invoiceObjs)
            self.updateGSTInvoiceLines(invoiceObjs)
        return True

    def fetchSupplierInvoices(self):
        ctx = dict(self._context or {})
        filter = [('id', '!=', self.id)]
        invoiceObjs = self.with_context(ctx).getInvoiceObjs(filter, ['in_invoice', 'in_refund'])
        self.invoice_lines = [(6, 0, invoiceObjs.ids)]
        if invoiceObjs:
            self.updateInvoiceCurrencyRate(invoiceObjs)
            self.updateGSTInvoiceLines(invoiceObjs)
        return True

    def updateInvoiceCurrencyRate(self, invoiceObjs):
        for invoiceObj in invoiceObjs:
            currency = invoiceObj.currency_id
            amount_total = invoiceObj.amount_total_signed
            if currency.name != 'INR':
                amount_total *= currency.rate
            invoiceObj.inr_total = amount_total
        return True

    def updateGSTInvoiceLines(self, invoiceObjs):
        code = self.env.company.state_id.code
        for invoiceObj in invoiceObjs:
            if invoiceObj.type in ['in_refund', 'out_refund']:
                invoiceObj.invoice_type = 'cdnr'
            elif invoiceObj.type == 'in_invoice':
                if invoiceObj.partner_id.country_id.code == 'IN':
                    if invoiceObj.partner_id.vat:
                        invoiceObj.invoice_type = 'b2b'
                    else:
                        invoiceObj.invoice_type = 'b2bur'
                else:
                    invoiceObj.invoice_type = 'import'
            else:
                if invoiceObj.partner_id.country_id.code == 'IN':
                    if invoiceObj.partner_id.vat:
                        invoiceObj.invoice_type = 'b2b'
                    elif invoiceObj.inr_total >= 250000 and invoiceObj.partner_id.state_id.code != code:
                        invoiceObj.invoice_type = 'b2cl'
                        if not invoiceObj.bonded_wh:
                            invoiceObj.bonded_wh = 'no'
                    else:
                        invoiceObj.invoice_type = 'b2cs'
                else:
                    invoiceObj.invoice_type = 'export'
                    invoiceObj.export = 'WOPAY'
        return True

    def getInvoiceObjs(self, extrafilter=[], invoiceType=[]):
        invoiceObjs = []
        gstObjs = self.search(extrafilter)
        invoiceIds = gstObjs and gstObjs.mapped(
            'invoice_lines') and gstObjs.mapped('invoice_lines').ids or []
        if self.period_id:
            filter = [
                ('invoice_date', '>=', self.period_id.date_start),
                ('invoice_date', '<=', self.period_id.date_stop),
                ('gst_status', '=', 'not_uploaded'),
                ('type', 'in', invoiceType),
                ('company_id', '=', self.company_id.id),
                ('state', 'in', ['posted']),
            ]
            if not self.date_from:
                self.date_from = self.period_id.date_start
                self.date_to = self.period_id.date_stop
            if self.date_from and self.date_to:
                if self.period_id.date_start > self.date_from \
                    or self.period_id.date_start > self.date_to \
                    or self.period_id.date_stop < self.date_to \
                    or self.period_id.date_stop < self.date_from:
                    raise UserError("Date should belong to selected period")
                if self.date_from > self.date_to:
                    raise UserError("End date should greater than or equal to starting date")
                filter.append(('invoice_date', '>=', self.date_from))
                filter.append(('invoice_date', '<=', self.date_to))
            if invoiceIds:
                filter.append(('id', 'not in', invoiceIds))
            invoiceObjs = self.env['account.move'].search(filter)
        return invoiceObjs

    def generateCsv(self):
        invoiceObjs = self.invoice_lines
        if invoiceObjs:
            name = self.name
            typeDict = {}
            invoiceIds = invoiceObjs.ids
            for invoiceObj in invoiceObjs:
                if typeDict.get(invoiceObj.invoice_type):
                    typeDict.get(invoiceObj.invoice_type).append(invoiceObj.id)
                else:
                    typeDict[invoiceObj.invoice_type] = [invoiceObj.id]
            gstinCompany = self.env.company.vat
            fp = self.period_id.code
            if fp:
                fp = fp.replace('/', '')
            jsonData = {
                "gstin": gstinCompany,
                "fp": fp,
                "gt": self.gt,
                "cur_gt": self.cgt,
            }
            ctx = dict(self._context or {})
            ctx['gst_id'] = self.id
            typeList = self.getTypeList()
            gstType = self.gst_type
            for invoice_type, active_ids in typeDict.items():
                if invoice_type in typeList:
                    continue
                respData = self.env['export.csv.wizard'].with_context(
                    ctx).exportCsv(active_ids, invoice_type, name, gstType)
                attachment = respData[0]
                jsonInvoiceData = respData[1]
                if invoice_type == 'b2b':
                    jsonData.update({invoice_type: jsonInvoiceData})
                    self.b2b_attachment = attachment.id
                if invoice_type == 'b2bur':
                    jsonData.update({invoice_type: jsonInvoiceData})
                    self.b2bur_attachment = attachment.id
                if invoice_type == 'b2cs':
                    self.b2cs_attachment = attachment.id
                    jsonData.update({invoice_type: jsonInvoiceData})
                if invoice_type == 'b2cl':
                    jsonData.update({invoice_type: jsonInvoiceData})
                    self.b2cl_attachment = attachment.id
                if invoice_type == 'import':
                    impsAttach = attachment[0]
                    impsJsonInvoiceData = attachment[1]
                    impgAttach = jsonInvoiceData[0]
                    impgJsonInvoiceData = jsonInvoiceData[1]
                    jsonData.update({
                        'imp_s': impsJsonInvoiceData,
                        'imp_g': impgJsonInvoiceData
                    })
                    if impsAttach:
                        self.imps_attachment = impsAttach.id
                    if impgAttach:
                        self.impg_attachment = impgAttach.id
                if invoice_type == 'export':
                    jsonData.update(
                        {'exp': {
                            "exp_typ": "WOPAY",
                            "inv": jsonInvoiceData
                        }})
                    self.export_attachment = attachment.id
                if invoice_type == 'cdnr':
                    jsonData.update({
                        invoice_type: jsonInvoiceData
                    })
                    self.cdnr_attachment = attachment.id

            if not self.hsn_attachment:
                respHsnData = self.env['export.csv.wizard'].with_context(
                    ctx).exportCsv(invoiceIds, 'hsn', name, gstType)
                if respHsnData:
                    hsnAttachment = respHsnData[0]
                    jsonInvoiceData = respHsnData[1]
                    jsonData.update({'hsn': {"data": jsonInvoiceData}})
                    if hsnAttachment:
                        self.hsn_attachment = hsnAttachment.id
                        self.status = 'ready_to_upload'
            if not self.json_attachment:
                if jsonData:
                    jsonData = json.dumps(jsonData, indent=4, sort_keys=False)
                    base64Data = base64.b64encode(jsonData.encode('utf-8'))
                    jsonAttachment = False
                    try:
                        jsonFileName = "{}.json".format(name)
                        jsonAttachment = self.env['ir.attachment'].create({
                            'datas': base64Data,
                            'type': 'binary',
                            'res_model': 'gstr1.tool',
                            'res_id': self.id,
                            'db_datas': jsonFileName,
                            'store_fname': jsonFileName,
                            'name': jsonFileName
                        })
                    except ValueError:
                        return jsonAttachment
                    if jsonAttachment:
                        self.json_attachment = jsonAttachment.id
        message = "Your gst & hsn csv are successfully generated"
        partial = self.env['message.wizard'].create({'text': message})
        return {
            'name': ("Information"),
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'view_id': self.env.ref('gst_invoice.message_wizard_form1').id,
            'res_id': partial.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
        }

    def getTypeList(self):
        typeList = []
        if self.b2b_attachment:
            typeList.append('b2b')
        if self.b2bur_attachment:
            typeList.append('b2bur')
        if self.b2cs_attachment:
            typeList.append('b2cs')
        if self.b2cl_attachment:
            typeList.append('b2cl')
        if self.export_attachment:
            typeList.append('export')
        if self.cdnr_attachment:
            typeList.append('cdnr')
        if self.imps_attachment:
            typeList.append('imps')
        if self.impg_attachment:
            typeList.append('impg')
        return typeList

    def exportB2BCSV(self):
        if not self.b2b_attachment:
            self.generateCsv()
        if not self.b2b_attachment:
            raise UserError("CSV of B2B invoice is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.b2b_attachment.id),
            'target': 'new',
        }

    def exportB2BURCSV(self):
        if not self.b2bur_attachment:
            self.generateCsv()
        if not self.b2bur_attachment:
            raise UserError("CSV of B2BUR invoice is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.b2bur_attachment.id),
            'target': 'new',
        }

    def exportB2CSCSV(self):
        if not self.b2cs_attachment:
            self.generateCsv()
        if not self.b2cs_attachment:
            raise UserError("CSV of B2CS invoice is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.b2cs_attachment.id),
            'target': 'new',
        }

    def exportB2CLCSV(self):
        if not self.b2cl_attachment:
            self.generateCsv()
        if not self.b2cl_attachment:
            raise UserError("CSV of B2CL invoice is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.b2cl_attachment.id),
            'target': 'new',
        }

    def exportIMPSCSV(self):
        if not self.imps_attachment:
            self.generateCsv()
        if not self.imps_attachment:
            raise UserError("CSV of IMPS invoice is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.imps_attachment.id),
            'target': 'new',
        }

    def exportIMPGCSV(self):
        if not self.impg_attachment:
            self.generateCsv()
        if not self.impg_attachment:
            raise UserError("CSV of IMPS invoice is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.impg_attachment.id),
            'target': 'new',
        }

    def exportExportCSV(self):
        if not self.export_attachment:
            self.generateCsv()
        if not self.export_attachment:
            raise UserError("CSV of Export invoice is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.export_attachment.id),
            'target': 'new',
        }

    def exportHSNCSV(self):
        if not self.hsn_attachment:
            self.generateCsv()
        if not self.hsn_attachment:
            raise UserError("HSN of gst invoice is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.hsn_attachment.id),
            'target': 'new',
        }

    def exportCDNRCSV(self):
        if not self.cdnr_attachment:
            self.generateCsv()
        if not self.cdnr_attachment:
            raise UserError("CSV of CDNR invoice is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.cdnr_attachment.id),
            'target': 'new',
        }

    def exportJson(self):
        if not self.json_attachment:
            self.generateCsv()
        if not self.json_attachment:
            raise UserError("JSON of GST invoice is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.json_attachment.id),
            'target': 'new',
        }

    def uploadGST(self):
        partial = self.env['message.wizard'].create(
            {'text': 'GST Invoice is successfully uploaded'})
        self.status = 'uploaded'
        self.updateInvoiceStatus('uploaded')
        return {
            'name': ("Information"),
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'view_id': self.env.ref('gst_invoice.message_wizard_form1').id,
            'res_id': partial.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
        }

    def filedGST(self):
        partial = self.env['message.wizard'].create(
            {'text': 'GST Invoice is successfully Filed'})
        self.status = 'filed'
        self.updateInvoiceStatus('filed')
        return {
            'name': ("Information"),
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'view_id': self.env.ref('gst_invoice.message_wizard_form1').id,
            'res_id': partial.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
        }

    def updateInvoiceStatus(self, status):
        self.invoice_lines.write({'gst_status': status})
        return True
