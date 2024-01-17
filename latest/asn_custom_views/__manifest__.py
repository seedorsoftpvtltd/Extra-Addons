
{
    'name': 'ASN Views for custom Module',
    'category': 'Accounting',
    'version': '14.0.0.0',
    'description': """

""",
    'author': 'Fousia Banu A.R',
    'summary': 'This module replaces existing views in custom modules : HB Warehouse Fields,HB Warehouse Delivery V2,Convert Freight Operation to Warehouse.',
    'website': 'https://www.browseinfo.in',
    'price': 29,
    'currency': "EUR",
    'depends': ['warehouse','warehouse_stock','asn_views','hb_warehouse_fields',
                'hb_warehouse_deliveryv2','warehouse_import','warehouse_stock_fields_asn_V2'],

    'data': [
        'views/views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    "live_test_url": 'https://youtu.be/DuMt9in_RaE',
    "images": ['static/description/Banner.png'],
}
