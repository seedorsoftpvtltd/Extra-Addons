{
    'name': 'Custom Hr Employee',
    'version': '13.0.0.0.0',
    'category': 'Human Resources/Employees',
    'sequence': 80,
    'license': 'AGPL-3',
    'depends': [
        'hr','base_setup',
    ],
    'data': [
        'views/hr_employee_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
