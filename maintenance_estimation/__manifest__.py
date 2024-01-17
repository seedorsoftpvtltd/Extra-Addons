{
    'name' : 'Maintenance Estimation',
    'version' : '1.1',
    'summary': '',
    'sequence': 15,
    'description': """======================""",
    'category': 'Hr',
    'website': ' ',
    'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'depends' : ['maintenance','maintenance_checklist', 'job_cost_estimate_customer','material_purchase_requisitions'],
    'data': [
       'views/estimation.xml',
       'views/requisition.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'post_init_hook': '_auto_install_l10n',
}