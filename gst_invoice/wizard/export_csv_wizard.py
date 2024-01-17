# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import base64
import csv
import io
from urllib.parse import unquote_plus

from odoo import api, models

def _unescape(text):
    try:
        text = unquote_plus(text.encode('utf8'))
        return text
    except Exception as e:
        return text


class ExportCsvWizard(models.TransientModel):
    _name = "export.csv.wizard"
    _description = "Export CSV wizard"

    @api.model
    def exportCsv(self, active_ids, invoice_type, gstToolName, gstType):
        if invoice_type == 'import':
            impsData = self.getInvoiceData(active_ids, 'imps', gstType)
            mainData = impsData[0]
            impsAttachment = self.prepareCsv(mainData, 'imps', gstToolName, gstType)
            impsJsonData = impsData[1]
            impgData = self.getInvoiceData(active_ids, 'impg', gstType)
            mainData = impgData[0]
            impgAttachment = self.prepareCsv(mainData, 'impg', gstToolName, gstType)
            impgJsonData = impgData[1]
            return [[impsAttachment, impsJsonData], [impgAttachment, impgJsonData]]
        respData = self.getInvoiceData(active_ids, invoice_type, gstType)
        mainData = respData[0]
        jsonData = respData[1]
        attachment = self.prepareCsv(mainData, invoice_type, gstToolName, gstType)
        return [attachment, jsonData]

    def prepareCsv(self, mainData, invoice_type, gstToolName, gstType):
        attachment = False
        if mainData:
            fp = io.StringIO()
            writer = csv.writer(fp, quoting=csv.QUOTE_NONE, escapechar='\\')
            if invoice_type == 'b2b':
                columns = self.env['csv.column'].getB2BColumn(gstType)
                writer.writerow(columns)
            elif invoice_type == 'b2bur':
                columns = self.env['csv.column'].getB2BURColumn()
                writer.writerow(columns)
            elif invoice_type == 'b2cl':
                columns = self.env['csv.column'].getB2CLColumn()
                writer.writerow(columns)
            elif invoice_type == 'b2cs':
                columns = self.env['csv.column'].getB2CSColumn()
                writer.writerow(columns)
            elif invoice_type == 'imps':
                columns = self.env['csv.column'].getImpsColumn()
                writer.writerow(columns)
            elif invoice_type == 'impg':
                columns = self.env['csv.column'].getImpgColumn()
                writer.writerow(columns)
            elif invoice_type == 'export':
                columns = self.env['csv.column'].getExportColumn()
                writer.writerow(columns)
            elif invoice_type == 'hsn':
                columns = self.env['csv.column'].getHSNColumn()
                writer.writerow(columns)
            elif invoice_type == 'cdnr':
                columns = self.env['csv.column'].getCDNRColumn(gstType)
                writer.writerow(columns)
            for lineData in mainData:
                writer.writerow([_unescape(name) for name in lineData])
            fp.seek(0)
            data = fp.read()
            fp.close()
            attachment = self.generateAttachment(data, invoice_type, gstToolName)
        return attachment

    def generateAttachment(self, data, invoice_type, gstToolName):
        attachment = False
        base64Data = base64.b64encode(data.encode('utf-8'))
        store_fname = '{}_{}.csv'.format(invoice_type, gstToolName)
        try:
            resId = 0
            if self._context.get('gst_id'):
                resId = self._context.get('gst_id')
            attachment = self.env['ir.attachment'].create({
                'datas': base64Data,
                'type': 'binary',
                'res_model': 'gstr1.tool',
                'res_id': resId,
                'db_datas': store_fname,
                'store_fname': store_fname,
                'name': store_fname
                }
            )
        except ValueError:
            return attachment
        return attachment

    def getInvoiceData(self, active_ids, invoiceType, gstType):
        mainData = []
        jsonData = []
        count = 0
        ctx = dict(self._context or {})
        b2csDataDict = {}
        b2csJsonDataDict = {}
        b2clJsonDataDict = {}
        b2burDataDict = {}
        b2bDataDict = {}
        cdnrDataDict = {}
        hsnDict = {}
        hsnDataDict = {}
        reverseChargeMain = 'N'
        counterFilingStatus = 'Y'
        gstcompany_id = False
        if ctx.get('gst_id'):
            resId = ctx.get('gst_id')
            resObj = self.env['gstr1.tool'].browse(resId)
            gstcompany_id = resObj.company_id
            if resObj.reverse_charge:
                reverseChargeMain = 'Y'
            if not resObj.counter_filing_status:
                counterFilingStatus = 'N'
        if not gstcompany_id:
            gstcompany_id = self.env.company
        invoiceObjs = self.env['account.move'].browse(active_ids)
        for invoiceObj in invoiceObjs:
            invData = {}
            reverseCharge = 'Y' if invoiceObj.reverse_charge else 'N' if reverseChargeMain == 'N' else reverseChargeMain
            invType = invoiceObj.l10n_in_export_type or 'regular'
            jsonInvType = 'R'
            if invType == 'sez_with_igst':
                jsonInvType = 'SEWP'
            elif invType == 'sez_without_igst':
                jsonInvType = 'SEWOP'
            elif invType == 'deemed':
                jsonInvType = 'DE'
            elif invType == 'sale_from_bonded_wh':
                jsonInvType = 'CBW'
            currency = invoiceObj.currency_id
            invoiceNumber = invoiceObj.name or ''
            if gstType == 'gstr2':
                invoiceNumber = invoiceObj.ref or ''
                if invoiceType == 'cdnr':
                    invoiceNumber = invoiceObj.name or ''
            if len(invoiceNumber) > 16:
                invoiceNumber = invoiceNumber[-16:]
            invoiceDate = invoiceObj.invoice_date
            invoiceJsonDate = invoiceDate.strftime('%d-%m-%Y')
            invoiceDate = invoiceDate.strftime('%d-%b-%Y')
            originalInvObj = invoiceObj.reversed_entry_id
            if originalInvObj:
                originalInvNumber = originalInvObj.name or ''
                if gstType == 'gstr2':
                    originalInvNumber = originalInvObj.ref or ''
                if len(originalInvNumber) > 16:
                    originalInvNumber = originalInvNumber[-16:]
                originalInvDate = originalInvObj.date
                originalInvJsonDate = originalInvDate.strftime('%d-%b-%Y')
                originalInvDate = originalInvDate.strftime('%d-%m-%Y')
            invoiceTotal = invoiceObj.amount_total
            if currency.name != 'INR':
                invoiceTotal = invoiceTotal * currency.rate
            invoiceObj.inr_total = invoiceTotal
            invoiceTotal = round(invoiceTotal, 2)
            state = invoiceObj.partner_id.state_id
            code = _unescape(state.l10n_in_tin) or 0
            sname = _unescape(state.name)
            stateName = "{}-{}".format(code, sname)
            data = []
            if invoiceType == 'b2b':
                customerName = invoiceObj.partner_id.name
                invData = {
                    "inum": invoiceNumber,
                    "idt": invoiceDate,
                    "val": invoiceTotal,
                    "pos": code,
                    "rchrg": reverseCharge,
                    "inv_typ": jsonInvType
                }
                if gstType == 'gstr1':
                    invData['etin'] = ""
                    invData['diff_percent'] = 0.0
                gstrData = [invoiceObj.l10n_in_partner_vat, invoiceNumber, invoiceDate, invoiceTotal, stateName, reverseCharge, 'Regular']
                if gstType == 'gstr1':
                    gstrData = [invoiceObj.l10n_in_partner_vat, customerName, invoiceNumber, invoiceDate, invoiceTotal, stateName, reverseCharge, 0.0, invType, '']
                data.extend(gstrData)
                respData = self.env['gst.invoice.data'].getGSTInvoiceData(invoiceObj, invoiceType, data, gstType)
                data = respData[0]
                invData['itms'] = respData[1]
                invData['idt'] = invoiceJsonDate
                if b2bDataDict.get(invoiceObj.l10n_in_partner_vat):
                    b2bDataDict[invoiceObj.l10n_in_partner_vat].append(invData)
                else:
                    b2bDataDict[invoiceObj.l10n_in_partner_vat] = [invData]
            elif invoiceType == 'b2bur':
                sply_ty = 'INTER'
                sply_type = 'Inter State'
                if invoiceObj.partner_id.state_id.code != gstcompany_id.state_id.code:
                    sply_ty = 'INTRA'
                    sply_type = 'Intra State'
                invData = {
                    "inum": invoiceNumber,
                    "idt": invoiceDate,
                    "val": invoiceTotal,
                    "pos": code,
                    "sply_ty": sply_ty
                }
                supplierName = invoiceObj.partner_id.name
                data.extend([supplierName, invoiceNumber, invoiceDate, invoiceTotal, stateName, sply_type])
                respData = self.env['gst.invoice.data'].getGSTInvoiceData(invoiceObj, invoiceType, data, gstType)
                data = respData[0]
                invData['itms'] = respData[1]
                invData['idt'] = invoiceJsonDate
                if b2burDataDict.get(supplierName):
                    b2burDataDict[supplierName].append(invData)
                else:
                    b2burDataDict[supplierName] = [invData]

            elif invoiceType == 'b2cl':
                invData = {
                    "inum": invoiceNumber,
                    "idt": invoiceDate,
                    "val": invoiceTotal,
                    "etin": "",
                }
                invData['diff_percent'] = 0.0
                data.extend([invoiceNumber, invoiceDate, invoiceTotal, stateName, 0.0])
                respData = self.env['gst.invoice.data'].getGSTInvoiceData(invoiceObj, invoiceType, data, gstType)
                data = respData[0]
                invData['itms'] = respData[1]
                invData['idt'] = invoiceJsonDate
                if b2clJsonDataDict.get(code):
                    b2clJsonDataDict[code].append(invData)
                else:
                    b2clJsonDataDict[code] = [invData]
            elif invoiceType == 'b2cs':
                invData = {
                    "pos": code
                }
                b2bData = ['OE', stateName]
                respData = self.env['gst.invoice.data'].getGSTInvoiceData(invoiceObj, invoiceType, b2bData, gstType)
                b2bData = respData[0]
                rateDataDict = respData[2]
                rateJsonDict = respData[3]
                if b2csDataDict.get(stateName):
                    for key in rateDataDict.keys():
                        if b2csDataDict.get(stateName).get(key):
                            for key1 in rateDataDict.get(key).keys():
                                if b2csDataDict.get(stateName).get(key).get(key1):
                                    b2csDataDict.get(stateName).get(key)[key1] = b2csDataDict.get(stateName).get(key)[key1] + rateDataDict.get(key)[key1]
                                else:
                                    b2csDataDict.get(stateName).get(key)[key1] = rateDataDict.get(key)[key1]
                        else:
                            b2csDataDict.get(stateName)[key] = rateDataDict[key]
                else:
                    b2csDataDict[stateName] = rateDataDict
                if b2csJsonDataDict.get(code):
                    for key in rateJsonDict.keys():
                        if b2csJsonDataDict.get(code).get(key):
                            for key1 in rateJsonDict.get(key).keys():
                                if b2csJsonDataDict.get(code).get(key).get(key1):
                                    if key1 in ['rt', 'sply_ty', 'typ']:
                                        continue
                                    b2csJsonDataDict.get(code).get(key)[key1] = b2csJsonDataDict.get(code).get(key)[key1] + rateJsonDict.get(key)[key1]
                                    b2csJsonDataDict.get(code).get(key)[key1] = round(b2csJsonDataDict.get(code).get(key)[key1], 2)
                                else:
                                    b2csJsonDataDict.get(code).get(key)[key1] = rateJsonDict.get(key)[key1]
                        else:
                            b2csJsonDataDict.get(code)[key] = rateJsonDict[key]
                else:
                    b2csJsonDataDict[code] = rateJsonDict
                if respData[1]:
                    invData.update(respData[1][0])
            elif invoiceType == 'imps':
                state = self.env.company.state_id
                code = _unescape(state.l10n_in_tin) or 0
                sname = _unescape(state.name)
                stateName = "{}-{}".format(code, sname)
                invData = {
                    "inum": invoiceNumber,
                    "idt": invoiceDate,
                    "ival": invoiceTotal,
                    "pos": code
                }
                supplierName = invoiceObj.partner_id.name
                data.extend([invoiceNumber, invoiceDate, invoiceTotal, stateName])
                respData = self.env['gst.invoice.data'].getGSTInvoiceData(invoiceObj, invoiceType, data, gstType)
                data = respData[0]
                invData['itms'] = respData[1]
                invData['idt'] = invoiceJsonDate
                jsonData.append(invData)
            elif invoiceType == 'impg':
                companyGST = self.env.company.vat
                portcode = ''
                if invoiceObj.l10n_in_shipping_port_code_id:
                    portcode = invoiceObj.l10n_in_shipping_port_code_id.name
                invData = {
                    "boe_num": invoiceNumber,
                    "boe_dt": invoiceJsonDate,
                    "boe_val": invoiceTotal,
                    "port_code": portcode,
                    "stin": companyGST,
                    'is_sez':'Y'
                }
                supplierName = invoiceObj.partner_id.name
                data.extend([portcode, invoiceNumber, invoiceDate, invoiceTotal, 'Imports', companyGST])
                respData = self.env['gst.invoice.data'].getGSTInvoiceData(invoiceObj, invoiceType, data, gstType)
                data = respData[0]
                invData['itms'] = respData[1]
                jsonData.append(invData)
            elif invoiceType == 'export':
                portcode = ''
                if invoiceObj.l10n_in_shipping_port_code_id:
                    portcode = invoiceObj.l10n_in_shipping_port_code_id.name
                invData = {
                    "inum": invoiceNumber,
                    "idt": invoiceDate,
                    "val": invoiceTotal,
                    "sbpcode": portcode,
                    "sbnum": "",
                    "sbdt": "",
                }
                invData['diff_percent'] = 0.0
                data.extend([invoiceObj.export, invoiceNumber, invoiceDate, invoiceTotal, portcode, '', '', 0.0])
                respData = self.env['gst.invoice.data'].getGSTInvoiceData(invoiceObj, invoiceType, data, gstType)
                data = respData[0]
                invData['itms'] = respData[1]
                invData['idt'] = invoiceJsonDate
                jsonData.append(invData)
            elif invoiceType == 'hsn':
                respData = self.env['gst.hsn.data'].getHSNData(invoiceObj, count, hsnDict, hsnDataDict)
                data = respData[0]
                jsonData.extend(respData[1])
                hsnDict = respData[2]
                hsnDataDict = respData[3]
                invoiceObj.gst_status = 'ready_to_upload'
            elif invoiceType == 'cdnr':
                customerName = invoiceObj.partner_id.name
                pre_gst = 'N'
                if invoiceObj.pre_gst:
                    pre_gst = 'Y'
                invoiceObjRef = invoiceObj.ref or ''
                reasonList = invoiceObjRef.split(',')
                reasonNote = reasonList[1].strip() if len(reasonList) > 1 else invoiceObjRef
                sply_ty = 'INTER'
                sply_type = 'Inter State'
                if invoiceObj.partner_id.state_id.code != gstcompany_id.state_id.code:
                    sply_ty = 'INTRA'
                    sply_type = 'Intra State'
                invData = {
                    "inum": originalInvNumber,
                    "idt": originalInvDate,
                    "val": invoiceTotal,
                    "nt_num": invoiceNumber,
                    "nt_dt": invoiceJsonDate,
                    "ntty": "C",
                    "p_gst": pre_gst,
                }
                if gstType == 'gstr2':
                    invData['ntty'] = "D"
                gstrData = [invoiceObj.l10n_in_partner_vat, invoiceNumber, invoiceDate, originalInvNumber,
                            originalInvJsonDate, pre_gst, 'D', reasonNote, sply_type, invoiceTotal]
                if gstType == 'gstr1':
                    gstrData = [invoiceObj.l10n_in_partner_vat, customerName, originalInvNumber, originalInvJsonDate,
                                invoiceNumber, invoiceDate, pre_gst, 'C', stateName, invoiceTotal, 0.0]
                data.extend(gstrData)
                respData = self.env['gst.invoice.data'].getGSTInvoiceData(
                    invoiceObj, invoiceType, data, gstType)
                data = respData[0]
                invData['itms'] = respData[1]
                if cdnrDataDict.get(invoiceObj.l10n_in_partner_vat):
                    cdnrDataDict[invoiceObj.l10n_in_partner_vat].append(invData)
                else:
                    cdnrDataDict[invoiceObj.l10n_in_partner_vat] = [invData]
            if data:
                mainData.extend(data)
        if b2csJsonDataDict:
            for pos,val in b2csJsonDataDict.items():
                for line in val.values():
                    line['pos'] = pos
                    line['diff_percent'] = 0.0
                    jsonData.append(line)
        if b2csDataDict:
            b2csData = []
            for state, data in b2csDataDict.items():
                for rate, val in data.items():
                    b2csData.append(['OE', state, 0.0, rate, round(val['taxval'], 2), round(val['cess'], 2), ''])
            mainData = b2csData

        if b2bDataDict:
            for ctin, inv in b2bDataDict.items():
                jsonData.append({
                    'cfs': counterFilingStatus,
                    'ctin':ctin,
                    'inv':inv
                })
        if b2burDataDict:
            for ctin, inv in b2burDataDict.items():
                jsonData.append({
                    'inv':inv
                })
        if b2clJsonDataDict:
            for pos, inv in b2clJsonDataDict.items():
                jsonData.append({
                    'pos':pos,
                    'inv':inv
                })
        if cdnrDataDict:
            for ctin, nt in cdnrDataDict.items():
                jsonData.append({
                    'cfs': counterFilingStatus,
                    'ctin': ctin,
                    'nt': nt
                })
        if hsnDict:
            vals = hsnDict.values()
            hsnMainData = []
            for val in vals:
                hsnMainData.extend(val.values())
            mainData = hsnMainData
        if hsnDataDict:
            vals = hsnDataDict.values()
            hsnMainData = []
            for val in vals:
                hsnMainData.extend(val.values())
            jsonData = hsnMainData
        return [mainData, jsonData]
