
{
    'name': 'Product Code Length',
    'version': '1.1',
    'summary': 'Product Code Length',
    'sequence': 15,
    'description': """In product model product code length set as 100  ,
 """,

    'depends': [
        'product',

    ],
    'data': [
        'security/ir.model.access.csv',

        'views/product_fields_form_view.xml',

    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,

    'license': 'LGPL-3',
}
