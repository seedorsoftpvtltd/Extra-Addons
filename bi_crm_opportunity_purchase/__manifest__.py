# -*- coding: utf-8 -*-
# Part of abc. See LICENSE file for full copyright and licensing details.
{
    'name' : "Purchase Order From LEAD in Odoo",
    'version' : "13.0.0.0",
    'category' : "Project",
    'summary': 'RFQ from crm LEAD convert lead into rfq crm Opportunity into RFQ create PO from lead create Purchase from Opportunity RFQ from Pipeline Quotation from CRM Quotation from pipeline quotation from Opportunity convert Pipeline into purchase order',
    'description' : '''
            This module allow to create 

    odoo Purchase order RFQ from CRM Opportunity also count created purchase orders.

            This module allow to 
    odoo create Purchase order/ RFQ from CRM Opportunity also count created purchase orders.
    This module allow to create Purchase order/ RFQ from CRM Opportunity also count created purchase orders.
    odoo create PO from lead PO from LEAD RFQ-Purchase Order From CRM Opportunity
    odoo purchase order from LEAD odoo RFQ from CRM Opportunity RFQ from LEAD
    odoo RFQ from crm LEAD Purchase Order From CRM Opportunity
    odoo convert lead into po convert lead into purchase order
    odoo convert lead into rfq crm Opportunity into RFQ
    odoo crm Opportunity into PO crm Opportunity into purchase order
    odoo create RFQ from LEAD reate RFQ from Opportunity


    odoo create Purchase order RFQ from Pipeline also count created purchase orders.
    This module allow to create Purchase orderfrom Pipeline also count created purchase orders.
    odoo create PO from Pipeline PO from Pipeline RFQ-Purchase Order From CRM Pipeline
    odoo purchase order from Pipeline odoo RFQ from CRM Opportunity RFQ from Pipeline
    odoo RFQ from Pipeline Purchase Order From Pipeline
    odoo convert Pipeline into po convert Pipeline into purchase order
    odoo convert Pipeline into rfq Pipeline into RFQ
    odoo crm Pipeline into PO Pipeline into purchase order
    odoo create RFQ from Pipeline create RFQ from Pipeline
    ''',
    'author' : "BrowseInfo",
    'website': 'https://www.browseinfo.in',
    "price": 15,
    "currency": 'EUR',
    'depends' : ['base','crm','purchase','stock'],
    'data': [
                'security/ir.model.access.csv',
                "views/crm_opportunity_purchase_view.xml",

             ],
    'installable': True,
    'auto_install': False,
    'live_test_url': "https://youtu.be/2lVCDe0_QcM",
    "images":['static/description/Banner.png'],
    
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
