{
    'name' : ' Default Charge Type Create',
    'version' : '13.0.0',
    'summary': 'Create an agreement and service if partner_id does not have an agreement.',
    'category': '',
    'depends' : ['agreement', 'warehouse','hb_wms_invoice_v1','hb_warehouse_deliveryv2','hb_agreement_extend'],
    'data': [
        'views/warehouse_view.xml',
        'views/stock_move_view.xml',
        'views/agreement_charges_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
