{
    'name': 'Tax Report Export XLSX for srt client requirement',
    'author': 'Arun Seedor',
    'summary': 'product enchancement for tax report in base_accounting_kit print excel',
    'depends': ['account', 'base_accounting_kit', 'report_xlsx', 'tax_report_export_xlsx','account_tax_balance',
                'to_account_payment'],
    'data': [

        'wizard/tax_report_wizard_view.xml',
        'wizard/account_report_common_view.xml',
        'wizard/report_srt_view.xml',
        'reports/print_report.xml',
        'views/account_view.xml',],
    'installable': True,
    'auto_install': False,
}
