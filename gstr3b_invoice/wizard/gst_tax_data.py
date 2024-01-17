# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, models


class GstTaxData(models.TransientModel):
    _inherit = "gst.tax.data"

    def getGstTaxData(self, invoiceObj, invoiceLineObj, rateObjs, taxedAmount, invoiceType):
        if self._context.get('gstType', '') != 'gstr3b':
            return super(GstTaxData,
                         self).getGstTaxData(invoiceObj=invoiceObj,
                                             invoiceLineObj=invoiceLineObj,
                                             rateObjs=rateObjs,
                                             taxedAmount=taxedAmount,
                                             invoiceType=invoiceType)
        gstDict = {
            "txval": 0.0,
            "iamt": 0.0,
            "camt": 0.0,
            "samt": 0.0,
            "csamt": 0.0,
        }
        if rateObjs:
            if invoiceObj.partner_id.country_id.code == 'IN':
                rateObj = rateObjs[0]
                if rateObj.amount_type == "group":
                    gstDict['samt'] = round(taxedAmount / 2, 2)
                    gstDict['camt'] = round(taxedAmount / 2, 2)
                else:
                    gstDict['iamt'] = round(taxedAmount, 2)
            elif invoiceType in ['export', 'import']:
                gstDict['iamt'] = round(taxedAmount, 2)
        return gstDict
