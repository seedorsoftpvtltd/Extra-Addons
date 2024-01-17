# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "All In One Secondary Unit Of Measure | Warehouse Secondary Unit V2",
    "author" : "Fousia Banu A.R",
    "website": "https://www.seedorsoft.com",

    "category": "Extra Tools",
    "summary": "Warehouse secondary uom app V2 extend",
    "description": """Warehouse secondary uom app""",
    "version":"13.0.2",
    "depends" : [

                    "warehouse",
                    "sh_secondary_unit",
                    'asn_views',
                    'warehouse_sec_unit',
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
