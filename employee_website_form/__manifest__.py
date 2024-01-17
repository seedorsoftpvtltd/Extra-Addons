# See LICENSE file for full copyright and licensing details.

{
    # Module Information
    'name': 'Employee Portal Form',
    'category': 'Portal',
    'sequence': 1,
    'version': '13.0.1.0.0',
    'license': 'LGPL-3',
    'summary': """Display Employee Details in website.
        Can view and update employee details in my info menu in website.""",
    'description': """
        Display Employee Details in website
         Can view and update employee details in my info menu in website
     """,
    # Website
    'author': 'Fousia Banu A.R',
    'website': 'http://www.seedors.com',

    # Dependencies
    'depends': ['base', 'website','hr_employee_updation'],
    # Data
    'data': [

            'views/employee_website_form_view.xml',
            'views/employee_menu.xml',
            'views/submit.xml',

    ],

    'images': ['static/description/fleet_rental_vehicle_banner.png'],

    # Technical
    'auto_install': False,
    'installable': True,
    'application': True,
}
