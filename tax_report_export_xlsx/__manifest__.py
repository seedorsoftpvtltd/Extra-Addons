{
    'name': 'Tax Report Export XLSX',
    'author': 'Arun Seedor',
    'summary': 'product enchancement for tax report in base_accounting_kit print excel',
    'depends': ['account', 'base_accounting_kit', 'report_xlsx'],
    'data': ['wizard/account_report_common_view.xml',
             'wizard/tax_report_xlsx_view.xml'],
    'installable': True,
    'auto_install': False,
}