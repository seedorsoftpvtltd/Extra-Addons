# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2020 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'            
    
    min_sales_price = fields.Boolean("Minimum Sales Price from chain of pricelist",
                                     config_parameter='sale.sale_pricelist_min_price')
    max_sales_price = fields.Boolean("Maximum Sales Price from chain of pricelist",
                                     config_parameter='sale.sale_pricelist_max_price')
    
    
    @api.onchange('multi_sales_price', 'multi_sales_price_method')
    def _onchange_sale_price(self):
        super(ResConfigSettings,self)._onchange_sale_price()
        if not self.multi_sales_price:
            self.update({
                'min_sales_price': False,
                'max_sales_price': False,
            })
