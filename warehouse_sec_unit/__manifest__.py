# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "All In One Secondary Unit Of Measure | Warehouse Secondary Unit ",
    "author" : "Herlin Breese J",
    "website": "https://www.seedorsoft.com",

    "category": "Extra Tools",
    "summary": "Warehouse secondary uom app",
    "description": """Warehouse secondary uom app""",
    "version":"13.0.2",
    "depends" : [

                    "warehouse",
                    "sh_secondary_unit"

                ],
    "application" : True,
    "data" : [
            "security/secondary_unit_group.xml",

            "views/sh_warehouse_order_view.xml",

            ],
    "auto_install":False,
    "installable" : True,
    "images": ['static/description/background.png', ],

}
