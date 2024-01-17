# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': "Create Job Estimation From CRM",
    'version': "13.0.0.1",
    'category': "Relocation",
    'summary': 'Create Job Estimation From CRM',
    'description': """ """,
    'author': "",

    'depends': ['crm', 'crm_lead_product', 'crm_to_job_estimate', 'hb_lead_to_job_extend'],
    'data': [
        'views/est.xml'
    ],
    'installable': True,
    'application': False,

}
