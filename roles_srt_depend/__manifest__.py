#############################################################################
{
    'name': "Access for Warehouse/Freight Depend",
    'version': '13.0.1.0.0',
    'summary': """This module provides Access/Restrict record from creation,confirmation,view in warehouse/freight modules.""",
    'description': """This module provides Access/Restrict record from creation,confirmation,view in warehouse/freight modules.""",
    'category': 'Freight',
    'author': 'Fousia banu A R',
    'company': '',
    'maintainer': '',
    'website': "https://www.cybrosys.com",
    'depends': ['scs_freight', 'warehouse', 'sale', 'stock', 'product', 'convert_quotation_to_job', 'gio',
                'job_cost_estimate_customer', 'agreement', 'account','roles_srt',
                'jobbooking_custom_view', 'jobbooking_service_salecost_read_depend', 'gio_custom_view'],
    'data': [
        'views/freight_roles.xml',
        'views/warehouse_roles.xml',
    ],
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
