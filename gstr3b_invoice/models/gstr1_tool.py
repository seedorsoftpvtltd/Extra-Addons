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
    _inherit = "gstr1.tool"

    def _get_gst_type(self):
        res = super(Gstr1Tool, self)._get_gst_type()
        res.append(('gstr3b', 'GSTR3B'))
        return res

    @api.onchange('period_id', 'date_from', 'date_to')
    def _compute_invoice_lines(self):
        if self.gst_type != 'gstr3b':
            return super(Gstr1Tool, self)._compute_invoice_lines()
        domain = {}
        filter = []
        ctx = dict(self._context or {})
        invoiceObjs = []
        if ctx.get('current_id'):
            filter.append(('id', '!=', ctx.get('current_id')))
        invoiceType = ['in_invoice', 'out_invoice']
        invoiceObjs = self.getInvoiceObjs(filter, invoiceType)
        if invoiceObjs:
            self.updateGSTInvoiceLines(invoiceObjs)
            domain['invoice_lines'] = [('id', 'in', invoiceObjs.ids)]
        else:
            domain['invoice_lines'] = [('id', 'in', [])]
        return {'domain': domain}

    def fetchAllInvoices(self):
        ctx = dict(self._context or {})
        filter = [('id', '!=', self.id)]
        invoiceObjs = self.with_context(ctx).getInvoiceObjs(filter, ['in_invoice', 'out_invoice'])
        self.invoice_lines = [(6, 0, invoiceObjs.ids)]
        if invoiceObjs:
            self.updateInvoiceCurrencyRate(invoiceObjs)
            self.updateGSTInvoiceLines(invoiceObjs)
        return True

    def getInvoiceObjs(self, extrafilter=[], invoiceType=[]):
        if self.gst_type != 'gstr3b':
            extrafilter.append(('gst_type', '!=', 'gstr3b'))
            return super(Gstr1Tool, self).getInvoiceObjs(extrafilter=extrafilter,
                                                         invoiceType=invoiceType)
        invoiceObjs = []
        extrafilter.append(('gst_type', '=', 'gstr3b'))
        gstObjs = self.search(extrafilter)
        invoiceIds = gstObjs and gstObjs.mapped(
            'invoice_lines') and gstObjs.mapped('invoice_lines').ids or []
        if self.period_id:
            filter = [
                ('invoice_date', '>=', self.period_id.date_start),
                ('invoice_date', '<=', self.period_id.date_stop),
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

    def reset(self):
        res = super(Gstr1Tool, self).reset()
        if self.gst_type == 'gstr3b':
            self.fetchAllInvoices()
        return res

    def generateJsonGstr3B(self):
        gstType = self.gst_type
        if gstType != 'gstr3b':
            return
        gstinCompany = self.env.company.vat
        ret_period = self.period_id.code
        if ret_period:
            ret_period = ret_period.replace('/', '')
        ctx = dict(self._context or {})
        ctx['gst_id'] = self.id
        name = self.name
        active_ids = self.invoice_lines.ids if self.invoice_lines else []
        respData = self.env['export.csv.wizard'].with_context(
                    ctx).exportCsv(active_ids, '', name, gstType)
        attachments = respData[0]
        jsonData = respData[1]
        jsonData.update({
            "gstin": gstinCompany,
            "ret_period": ret_period,
        })
        for attachment in attachments:
            if attachment.get('GSTR3B_3_1') and not self.b2b_attachment:
                self.b2b_attachment = attachment.get('GSTR3B_3_1').id
            elif attachment.get('GSTR3B_3_2') and not self.b2cs_attachment:
                self.b2cs_attachment = attachment.get('GSTR3B_3_2').id
            elif attachment.get('GSTR3B_4') and not self.b2bur_attachment:
                self.b2bur_attachment = attachment.get('GSTR3B_4').id
            elif attachment.get('GSTR3B_5') and not self.b2cl_attachment:
                self.b2cl_attachment = attachment.get('GSTR3B_5').id
        if not self.json_attachment:
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
                self.status = 'ready_to_upload'
                self.json_attachment = jsonAttachment.id
        message = "Your GSTR3B Data are successfully generated"
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

    def exportB2BCSV(self):
        if self.gst_type != 'gstr3b':
            return super(Gstr1Tool, self).exportB2BCSV()
        if not self.b2b_attachment:
            self.generateJsonGstr3B()
        if not self.b2b_attachment:
            raise UserError("CSV of GSTR3B 3.1 is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.b2b_attachment.id),
            'target': 'new',
        }

    def exportB2BURCSV(self):
        if self.gst_type != 'gstr3b':
            return super(Gstr1Tool, self).exportB2BURCSV()
        if not self.b2bur_attachment:
            self.generateJsonGstr3B()
        if not self.b2bur_attachment:
            raise UserError("CSV of GSTR3B 3.2 is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.b2bur_attachment.id),
            'target': 'new',
        }

    def exportB2CSCSV(self):
        if self.gst_type != 'gstr3b':
            return super(Gstr1Tool, self).exportB2CSCSV()
        if not self.b2cs_attachment:
            self.generateJsonGstr3B()
        if not self.b2cs_attachment:
            raise UserError("CSV of GSTR3B 4 is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.b2cs_attachment.id),
            'target': 'new',
        }

    def exportB2CLCSV(self):
        if self.gst_type != 'gstr3b':
            return super(Gstr1Tool, self).exportB2CLCSV()
        if not self.b2cl_attachment:
            self.generateJsonGstr3B()
        if not self.b2cl_attachment:
            raise UserError("CSV of GSTR3B 5 is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.b2cl_attachment.id),
            'target': 'new',
        }

    def exportJson(self):
        if self.gst_type != 'gstr3b':
            return super(Gstr1Tool, self).exportJson()
        if not self.json_attachment:
            self.generateJsonGstr3B()
        if not self.json_attachment:
            raise UserError("JSON of GSTR3B is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.json_attachment.id),
            'target': 'new',
        }

    def updateInvoiceStatus(self, status):
        if self.gst_type != 'gstr3b':
            return super(Gstr1Tool, self).updateInvoiceStatus(status=status)
        return True
