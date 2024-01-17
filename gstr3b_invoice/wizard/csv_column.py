# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, models


class CsvColumn(models.TransientModel):
    _inherit = "csv.column"

    def getGstr3B_3_1Column(self):
        return [
            'Nature of Supplies',
            'Total Taxable Value',
            'Integrated Tax',
            'Central Tax',
            'State/UT Tax',
            'Cess'
        ]

    def getGstr3B_3_2Column(self):
        return [
            'Place of Supply',
            'Unregistered Total Taxable Value',
            'Unregistered Integrated Tax Amount',
            'Composition Total Taxable Value',
            'Composition Integrated Tax Amount',
            'UIN Total Taxable Value',
            'UIN Integrated Tax Amount'
        ]

    def getGstr3B_4Column(self):
        return [
            'Details',
            'Integrated Tax',
            'Central Tax',
            'State/UT Tax',
            'Cess'
        ]

    def getGstr3B_5Column(self):
        return [
            'Nature of Supplies',
            'Inter-State Supplies',
            'Intra-State Supplies'
        ]
