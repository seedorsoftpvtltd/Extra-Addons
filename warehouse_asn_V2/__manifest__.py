
{
    "name" : "Warehouse Views V2",
    "author" : "Fousia Banu A.R",
    "website": "https://www.seedorsoft.com",

    "category": "Extra Tools",
    "summary": "This module replaces views in warehouse views to custom views module",
    "description": """This module replaces views in warehouse views to custom views module""",
    "version":"13.0.2",
    "depends" : [
                    'account',
                    "warehouse",
                     'warehouse_stock',
                    'asn_views',
                     'warehouse_stock_fields_asn_V2'


                ],
    "application" : True,
    "data" : [
            "views/views.xml",
            ],
    "auto_install":False,
    "installable" : True,
    "images": ['static/description/background.png', ],

}
