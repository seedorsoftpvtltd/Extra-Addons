# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name' : "Custom Clearance in Fright Operations Depend",
    'version' : "13.0.0.1",
    'category' : "Fright",
    'summary': 'Custom Clearance in Fright Operations',
    'description' : """ """,
    'author' : "Fousia Banu A.R",

    'depends'  : [ 'scs_freight','jobbooking_custom_view','custom_clearance'],
    'data'     : [
                 'Views/custom_clearance.xml',
            ],
    'installable' : True,
    'application' :  False,

}