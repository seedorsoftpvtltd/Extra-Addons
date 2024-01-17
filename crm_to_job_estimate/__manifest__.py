# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name' : "Create Job Estimation From CRM",
    'version' : "13.0.0.1",
    'category' : "Fright",
    'summary': 'This apps helps to Create Job Estimation From CRM',
    'description' : """ """,
    'author' : "Fousia Banu A.R",

    'depends'  : [ 'crm','job_cost_estimate_customer'],
    'data'     : [
        'views/estimate.xml'
    ],
    'installable' : True,
    'application' :  False,

}