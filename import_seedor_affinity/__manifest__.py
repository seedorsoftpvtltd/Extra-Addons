# -*- coding: utf-8 -*-
{
    'name': "Import Sales Orders, Chart Account data, Invoice, Stock Inventory, Products, Product attributes, Payments, Bank Statement, All Entry, Order Picking, Customers, Stocks, Account charts, Sales Pricelist, Supplier,Journal, journal entry using EXCEL or CSV",
    'category': 'Import Record',
    'version': '13.1.5',
    'description' : "Import data in Seedor, import Sale Orders.Chart Account data, Import Product, Invoice, Stock Inventory Import,Payment, Bank Statement, All Entry, Order Picking, Product, Customer, Stock, Account charts, Sales Pricelist, Supplier, Journal data import, journal entry all data import in Seedor using EXCEL or CSV",
    'summary': "Data Import bridge for import Chart Account data import Purchase import Product import Invoice import Stock Inventory import Payment import Bank Statement import All Entry import Order Picking import Products import Customer import Stock import Account charts import Sales Pricelist import Supplier import Journal data import journal entry import Supplier import sale Orders import Bulk Pricelist import product pricelist Import Sale Pricelist import vendor pricelist import inventory Seedor import Data All in one import all import data in Seedor using EXCEL or CSV",
    'depends': ['base', 'sale_management','account','stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/field_data.xml',
      
        # 'views/product_product_view.xml',        
        'wizard/import_customer_wizard_view.xml',
        'wizard/import_order_wizard_view.xml',
        'wizard/import_invoice_line_wizard_view.xml',
        'wizard/import_invoice_wizard_view.xml',
        'wizard/import_payment_wizard_view.xml',
        'wizard/import_product_wizard_view.xml',
        'wizard/import_sale_order_wizard_view.xml',
        'wizard/import_sale_order_line_wizard_view.xml',
        'wizard/import_purchase_order_wizard_view.xml',
        'wizard/import_purchase_order_line_wizard_view.xml',
        'wizard/import_bom_wizard_view.xml',
        'wizard/import_vendor_pricelist_view.xml',
        'wizard/view_import_chart.xml',
        'wizard/import_product_pricelist.xml',
        'wizard/import_bank_statement.xml',
        'wizard/import_sale_pricelist_view.xml',
        'wizard/import_inventory_view.xml',
        'wizard/import_inventory_adjustment_view.xml',
        'wizard/import_journal_view.xml',
        'wizard/import_journal_entry_view.xml',
        'views/customer_menu.xml',
        #'views/product_menu.xml',
        'views/account_view.xml',
        'views/custom_dashboard_view.xml',
        'views/sale_order_view.xml',
        
    ],
    'demo': [
    ],
    'price': 94.5,
    'currency': 'USD',
    'support': 'business@axistechnolabs.com',
    'author': 'Axis Technolabs',
    'website': 'https://www.axistechnolabs.com',
    'installable': True,
    'license': 'OPL-1',
    'images': ['static/description/images/Banner-Img.png'],
}
