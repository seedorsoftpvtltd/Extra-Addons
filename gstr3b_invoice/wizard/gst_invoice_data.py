# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, models

KEYS = ('txval', 'iamt', 'camt', 'samt', 'csamt')

def _unescape(text):
    try:
        text = unquote_plus(text.encode('utf8'))
        return text
    except Exception as e:
        return text


class GstInvoiceData(models.TransientModel):
    _inherit = "gst.invoice.data"

    def updateGstValues(self, data, respData, onlyKeys=[]):
        for key in data.keys():
            if key in KEYS and key in data and key in respData:
                if not onlyKeys or key in onlyKeys:
                    data[key] = round(data[key] + respData[key], 2)

    def getGSTInvoiceData(self, invoiceObj, invoiceType, data, gstType=''):
        if gstType != 'gstr3b':
            return super(GstInvoiceData,
                         self).getGSTInvoiceData(invoiceObj=invoiceObj,
                                                 invoiceType=invoiceType,
                                                 data=data,
                                                 gstType=gstType)
        rateJsonDict = {}
        ctx = dict(self._context or {})
        ctx['gstType'] = gstType
        for invoiceLineObj in invoiceObj.invoice_line_ids:
            response = self.env['gst.invoice.data'].with_context(
                ctx).getInvoiceLineData([], invoiceLineObj, invoiceObj, invoiceType)
            if response:
                respData = response[1]
                respData['txval'] = response[3]
                if invoiceObj.type == 'out_invoice':
                    sup_details = data['sup_details']
                    inter_sup = data['inter_sup']
                    if invoiceObj.reverse_charge:
                        self.updateGstValues(sup_details['isup_rev'], respData)
                    elif invoiceType == 'export':
                        onlyKeys = ['txval', 'iamt', 'csamt']
                        self.updateGstValues(sup_details['osup_zero'], respData, onlyKeys)
                    elif invoiceType in ['b2b', 'b2cs', 'b2cl']:
                        is_nil_exempted = True
                        if invoiceLineObj.tax_ids:
                            tax = invoiceLineObj.tax_ids[0]
                            if tax.amount or (tax.amount_type == 'group' and tax.children_tax_ids and tax.children_tax_ids[0].amount):
                                is_nil_exempted = False
                        if not is_nil_exempted:
                            self.updateGstValues(sup_details['osup_det'], respData)
                        else:
                            onlyKeys = ['txval']
                            self.updateGstValues(sup_details['osup_nil_exmp'], respData, onlyKeys)
                        details = inter_sup['uin_details']
                        if invoiceType in ['b2cs', 'b2cl']:
                            onlyKeys = ['txval']
                            self.updateGstValues(sup_details['osup_nongst'], respData, onlyKeys)
                            details = inter_sup['unreg_details']
                        if self.env.company.state_id != invoiceObj.partner_id.state_id:
                            pos = _unescape(invoiceObj.partner_id.state_id.l10n_in_tin)
                            for element in details:
                                if element['pos'] == pos:
                                    self.updateGstValues(element, respData)
                                    break
                            else:
                                details.append({
                                    'pos': pos,
                                    'txval': respData.get('txval', 0.0),
                                    'iamt': respData.get('iamt', 0.0)
                                })
                            if invoiceLineObj.product_id.is_composition:
                                for element in inter_sup['comp_details']:
                                    if element['pos'] == pos:
                                        self.updateGstValues(element, respData)
                                        break
                                else:
                                    inter_sup['comp_details'].append({
                                        'pos': pos,
                                        'txval': respData.get('txval', 0.0),
                                        'iamt': respData.get('iamt', 0.0)
                                    })
                elif invoiceObj.type == 'in_invoice':
                    itc_elg = data['itc_elg']
                    inward_sup = data['inward_sup']
                    isup_details = inward_sup['isup_details']
                    if invoiceObj.reverse_charge:
                        self.updateGstValues(itc_elg['itc_rev'][0], respData)
                    else:
                        if invoiceType == 'import':
                            if invoiceLineObj.product_id and invoiceLineObj.product_id.type == 'consu':
                                productType = 'IMPG'
                            else:
                                productType = 'IMPS'
                        else:
                            productType = 'OTH'
                        for element in itc_elg['itc_avl']:
                            if element['ty'] == productType:
                                self.updateGstValues(element, respData)
                                break
                        if invoiceType != 'import':
                            if not invoiceObj.partner_id.vat:
                                if self.env.company.state_id == invoiceObj.partner_id.state_id:
                                    ele_state = 'intra'
                                else:
                                    ele_state = 'inter'
                                for ele in isup_details:
                                    if ele['ty'] == 'NONGST':
                                        ele[ele_state] = round(ele[ele_state] + respData['txval'], 2)
                                        break
                            else:
                                is_nil_exempted = True
                                if invoiceLineObj.tax_ids:
                                    tax = invoiceLineObj.tax_ids[0]
                                    if tax.amount or (tax.amount_type == 'group' and tax.children_tax_ids and tax.children_tax_ids[0].amount):
                                        is_nil_exempted = False
                                if is_nil_exempted:
                                    if self.env.company.state_id == invoiceObj.partner_id.state_id:
                                        ele_state = 'intra'
                                    else:
                                        ele_state = 'inter'
                                    for ele in isup_details:
                                        if ele['ty'] == 'GST':
                                            ele[ele_state] = round(ele[ele_state] + respData['txval'], 2)
                                            break
                    for key in itc_elg['itc_net'][0].keys():
                        if key in KEYS:
                            itcAvl_sum = sum([ele[key] for ele in itc_elg['itc_avl']])
                            itcRev_sum = sum([ele[key] for ele in itc_elg['itc_rev']])
                            itc_elg['itc_net'][0][key] = itcAvl_sum - itcRev_sum
        return data
