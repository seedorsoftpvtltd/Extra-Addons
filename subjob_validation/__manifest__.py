{
    'name': 'SubJob Validation',
    'version': '13.0.1.0.0',
    'summary': 'SubJob Validation',
    'description': """
        DO Validation.
        """,
    'category': 'Accounting',
    'author': "Fousia Banu A R",
    'company': 'Seedorsoft Private Limited',
    'maintainer': 'Seedorsoft Private Limited',
    'website': "https://www.seedorsoft.com",
    'depends': [
        'stock','scs_freight','convert_freight_operation_to_warehouse'
    ],

   'data':
    [
    ],
    'demo': ['data/hr_overtime_demo.xml'],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}