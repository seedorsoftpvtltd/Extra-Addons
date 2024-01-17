{
    'name' : 'Googlesheet Onboarding',
    'version' : '1.1',
    'summary': '',
    'sequence': 15,
    'description': """======================""",
    'category': 'Hr',
    'website': ' ',
    'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'depends' : ['google_sheet_data_import'],
    'data': [
       'views/google_sheet.xml',
       'views/google_sheet_import_onboarding_template.xml',
       'views/googlesheet_onboarding_default_temp.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'post_init_hook': '_auto_install_l10n',
}
