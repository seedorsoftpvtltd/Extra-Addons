{
    'name' : 'Job from Quotation',
    'version' : '1.1',
    'summary': 'Create Job from quotation.',
    'sequence': 15,
    'description': """======================""",
    'category': 'Hr',
    'website': ' ',
    'images' : [],
    'depends' : ['sale','sale_management', 'scs_freight'],
    'data': [
       'views/job.xml',


    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'post_init_hook': '_auto_install_l10n',
}