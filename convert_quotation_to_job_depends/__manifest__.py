{
    'name' : 'Job from Quotation Depend',
    'version' : '1.1',
    'summary': 'Create Job from quotation.',
    'sequence': 15,
    'description': """======================""",
    'category': 'Hr',
    'website': ' ',
    'images' : [],
    'depends' : ['sale','sale_management', 'scs_freight','jobbooking_custom_view','convert_quotation_to_job',"hb_freight_extend"],
    'data': [
       'views/job.xml',


    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'post_init_hook': '_auto_install_l10n',
}