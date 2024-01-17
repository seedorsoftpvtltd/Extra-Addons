# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "Additional fields state",
    "author" : "Linu",
    "website": "",
    "support": "",
    "category": "Extra Tools",
    "summary": "Added attribute for fields",
    "description": """Added attribute for fields""",
    "version":"13.0.2",
    "depends" : [
                    'scs_freight',"hb_freight_extend",'jobbooking_custom_view',
                ],
    "application" : True,
    "data" : [

            "views/attributes_additional_views.xml",
            ],
    "auto_install":False,
    "installable" : True,
    "price": 25,
    "currency": "EUR" ,
    "images": ['static/description/background.png', ],
    "live_test_url": "https://www.youtube.com/watch?v=KrX_zvlWRdI&feature=youtu.be",
}
