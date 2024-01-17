{
    'name': 'Custom Hr Employee',
    'version': '13.0.0.0.0',
    'category': 'Human Resources/Employees',
    'summary': 'Employees  Configuration',
    'sequence': 80,
    'license': 'AGPL-3',
    'website': 'https://www.banibro.com',
    'depends': [
        'hr','base_setup',
    ],
    'data': [
        'views/hr_employee_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
