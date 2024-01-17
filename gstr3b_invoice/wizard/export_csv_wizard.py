# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

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
    _inherit = "export.csv.wizard"

    @api.model
    def exportCsv(self, active_ids, invoice_type, gstToolName, gstType):
        if gstType != 'gstr3b':
            return super(ExportCsvWizard,
                         self).exportCsv(active_ids=active_ids,
                                         invoice_type=invoice_type,
                                         gstToolName=gstToolName,
                                         gstType=gstType)
        respData = self.getInvoiceData(active_ids, invoice_type, gstType)
        jsonData = respData[1]
        types = ['GSTR3B_3_1', 'GSTR3B_3_2', 'GSTR3B_4', 'GSTR3B_5']
        attachments = []
        flag = 0
        for mainData in respData[0]:
            attachment = self.prepareCsv(mainData, types[flag], gstToolName, gstType)
            attachments.append({types[flag]: attachment})
            flag += 1
        return [attachments, jsonData]

    def prepareCsv(self, mainData, invoice_type, gstToolName, gstType):
        if gstType != 'gstr3b':
            return super(ExportCsvWizard,
                         self).prepareCsv(mainData=mainData,
                                          invoice_type=invoice_type,
                                          gstToolName=gstToolName,
                                          gstType=gstType)
        attachment = False
        if mainData:
            fp = io.StringIO()
            writer = csv.writer(fp, quoting=csv.QUOTE_NONE, escapechar='\\')
            if invoice_type == 'GSTR3B_3_1':
                columns = self.env['csv.column'].getGstr3B_3_1Column()
                writer.writerow(columns)
            elif invoice_type == 'GSTR3B_3_2':
                columns = self.env['csv.column'].getGstr3B_3_2Column()
                writer.writerow(columns)
            elif invoice_type == 'GSTR3B_4':
                columns = self.env['csv.column'].getGstr3B_4Column()
                writer.writerow(columns)
            elif invoice_type == 'GSTR3B_5':
                columns = self.env['csv.column'].getGstr3B_5Column()
                writer.writerow(columns)
            for lineData in mainData:
                writer.writerow([_unescape(name) for name in lineData])
            fp.seek(0)
            data = fp.read()
            fp.close()
            attachment = self.generateAttachment(data, invoice_type, gstToolName)
        return attachment

    def getInvoiceData(self, active_ids, invoiceType, gstType):
        if gstType != 'gstr3b':
            return super(ExportCsvWizard,
                         self).getInvoiceData(active_ids=active_ids,
                                              invoiceType=invoiceType,
                                              gstType=gstType)
        jsonData = {}
        mainData = []
        if active_ids:
            invoiceObjs = self.env['account.move'].browse(active_ids)
            jsonData = self.getGstr3BJsonData()
            for invoiceObj in invoiceObjs:
                invoiceType = invoiceObj.invoice_type
                jsonData = self.env["gst.invoice.data"].getGSTInvoiceData(
                    invoiceObj, invoiceType, jsonData, gstType)
            lineData = []
            rows = ['osup_det', 'osup_zero', 'osup_nil_exmp', 'isup_rev', 'osup_nongst']
            cols = ['txval', 'iamt', 'camt', 'samt', 'csamt']
            vals = [
                '(a) Outward Taxable supplies(other than zero/nil/exempted)',
                '(b) Outward Taxable supplies(zero rated)',
                '(c) Other Outward Taxable  supplies(Nil/exempted)',
                '(d) Inward supplies (liable to reverse charge)',
                '(e) Non-GST Outward supplies'
            ]
            for index in range(len(jsonData['sup_details'])):
                line = [vals[index]]
                for col in cols:
                    line.append(jsonData['sup_details'][rows[index]][col])
                lineData.append(line)
            mainData.append(lineData)
            lineData = []
            rows = ['unreg_details', 'comp_details', 'uin_details']
            poss = []
            for row in rows:
                for ele in jsonData['inter_sup'][row]:
                    poss.append(ele['pos'])
            poss = list(set(poss))
            for pos in poss:
                line = [pos]
                for row in rows:
                    for ele in jsonData['inter_sup'][row]:
                        if ele['pos'] == pos:
                            line += [ele['txval'], ele['iamt']]
                            break
                    else:
                        line += [0.0, 0.0]
                lineData.append(line)
            mainData.append(lineData)
            lineData = []
            rows = ['itc_avl', 'itc_rev', 'itc_net', 'itc_inelg']
            cols = ['iamt', 'camt', 'samt', 'csamt']
            vals = [
                '(A)(1) Import of goods',
                '(A)(2) Import of services',
                '(A)(3) Inward supplies liable to reverse charge(other than 1&2 above)',
                '(A)(4) Inward supplies from ISD',
                '(A)(5) All other ITC',
                '(B)(1) As per Rule 42 & 43 of SGST/CGST rules',
                '(B)(2) Others',
                '(C) Net ITC Available (A)-(B)',
                '(D)(1) As per section 17(5) of CGST//SGST Act',
                '(D)(2) Others'
            ]
            flag = 0
            for row in rows:
                for details in jsonData['itc_elg'][row]:
                    line = [vals[flag]]
                    for col in cols:
                        line.append(details[col])
                    flag += 1
                    lineData.append(line)
            mainData.append(lineData)
            lineData = []
            vals = [
                'From a supplier under composition/Exempt/Nil rated supply',
                'Non GST supply'
            ]
            flag = 0
            for details in jsonData['inward_sup']['isup_details']:
                line = [vals[flag], details['inter'], details['intra']]
                flag += 1
                lineData.append(line)
            mainData.append(lineData)
        return [mainData, jsonData]

    def getGstr3BJsonData(self):
        return {
            'gstin': '',
            'ret_period': '',
            'sup_details': {
                'osup_det': {
                    'txval': 0.0,
                    'iamt': 0.0,
                    'camt': 0.0,
                    'samt': 0.0,
                    'csamt': 0.0
                },
                'osup_zero': {
                    'txval': 0.0,
                    'iamt': 0.0,
                    'camt': 0.0,
                    'samt': 0.0,
                    'csamt': 0.0
                },
                'osup_nil_exmp': {
                    'txval': 0.0,
                    'iamt': 0.0,
                    'camt': 0.0,
                    'samt': 0.0,
                    'csamt': 0.0
                },
                'isup_rev': {
                    'txval': 0.0,
                    'iamt': 0.0,
                    'camt': 0.0,
                    'samt': 0.0,
                    'csamt': 0.0
                },
                'osup_nongst': {
                    'txval': 0.0,
                    'iamt': 0.0,
                    'camt': 0.0,
                    'samt': 0.0,
                    'csamt': 0.0
                }
            },
            'inter_sup': {
                'unreg_details': [],
                'comp_details': [],
                'uin_details': []
            },
            'itc_elg': {
                'itc_avl': [{
                    'iamt': 0.0,
                    'camt': 0.0,
                    'samt': 0.0,
                    'csamt': 0.0,
                    'ty': 'IMPG'
                }, {
                    'iamt': 0.0,
                    'camt': 0.0,
                    'samt': 0.0,
                    'csamt': 0.0,
                    'ty': 'IMPS'
                }, {
                    'iamt': 0.0,
                    'camt': 0.0,
                    'samt': 0.0,
                    'csamt': 0.0,
                    'ty': 'ISRC'
                }, {
                    'iamt': 0.0,
                    'camt': 0.0,
                    'samt': 0.0,
                    'csamt': 0.0,
                    'ty': 'ISD'
                }, {
                    'iamt': 0.0,
                    'camt': 0.0,
                    'samt': 0.0,
                    'csamt': 0.0,
                    'ty': 'OTH'
                }],
                'itc_rev': [{
                    'iamt': 0.0,
                    'camt': 0.0,
                    'samt': 0.0,
                    'csamt': 0.0,
                    'ty': 'RUL'
                }, {
                    'iamt': 0.0,
                    'camt': 0.0,
                    'samt': 0.0,
                    'csamt': 0.0,
                    'ty': 'OTH'
                }],
                'itc_net': [{
                    'iamt': 0.0,
                    'camt': 0.0,
                    'samt': 0.0,
                    'csamt': 0.0
                }],
                'itc_inelg': [{
                    'iamt': 0.0,
                    'camt': 0.0,
                    'samt': 0.0,
                    'csamt': 0.0,
                    'ty': 'RUL'
                }, {
                    'iamt': 0.0,
                    'camt': 0.0,
                    'samt': 0.0,
                    'csamt': 0.0,
                    'ty': 'OTH'
                }]
            },
            'inward_sup': {
                'isup_details': [{
                    'inter': 0.0,
                    'intra': 0.0,
                    'ty': 'GST'
                }, {
                    'inter': 0.0,
                    'intra': 0.0,
                    'ty': 'NONGST'
                }]
            },
            'intr_ltfee': {
                'intr_details': {
                    'camt': 0.0,
                    'csamt': 0.0,
                    'iamt': 0.0,
                    'samt': 0.0
                },
                'ltfee_details': {}
            }
        }
