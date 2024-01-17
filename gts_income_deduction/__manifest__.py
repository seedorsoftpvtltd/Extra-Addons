{
    'name': 'Employee TDS Deduction|Tds Calculation And Deduction For Employee',
    'version': '13.0.1.0.0',
    'summary': """Manages Employee TDS Deduction""",
    'description': """This module is used to track Employee Income deduction
    	employee, TDS, tds,deduction, employees, deductions, employee income, tds deduction, employee income deduction, 
	tds, employee tds, employee tax, tax employee, tax income, taxable income, tax deduct, tax deduction, tax deducted,
	employee taxable income,employee tds tax, employee tax tds, tds tax employee, tds tax income, tds taxable income, 
	tds tax deduct, tds tax deduction, tds tax deducted, employee tds taxable income,

	odoo employee, odoo tds, odoo deduction, odoo employees, odoo deductions, odoo employee income, odoo income deduction, 
	odoo employee income deduction, 
	odoo tds, odoo employee tds, odoo employee tax, odoo tax employee, odoo tax income, odoo taxable income, odoo tax deduct, 
	odoo tax deduction, odoo tax deducted, odoo employee taxable income, odoo employee tds tax, odoo employee tax tds, 
	odoo tds tax employee, odoo tds tax income, odoo tds taxable income, 
	odoo tds tax deduct, odoo tds tax deduction, odoo tds tax deducted, odoo employee tds taxable income,

	employee in odoo, tds in odoo, deduction in odoo, employees in odoo, deductions in odoo, employee income in odoo, 
	income deduction in odoo, employee income deduction in odoo, 
	tds in odoo, employee tds in odoo, employee tax in odoo, tax employee in odoo, tax income in odoo, taxable income in odoo, 
	tax deduct in odoo, tax deduction in odoo, tax deducted in odoo,
	employee taxable income in odoo, employee tds tax in odoo, employee tax tds in odoo, tds tax employee in odoo, 
	tds tax income in odoo, tds taxable income in odoo, tds tax deduct in odoo, tds tax deduction in odoo, 
	tds tax deducted in odoo, employee tds taxable income in odoo,


	information, tds info, tds information, salary, salary information, Annual Salary,
	other income, other income including interest, interest, gross income, total deduction,
	taxable amount, tax payable, tax, tax%, tax %, monthly deduction, tax deduction per month,
	deduction description, standard deduction, house rent allowances, transport allowance,
	leave travel allowances, deduction under 80c, deductions under other than 80c, 
	other dedcution, any other deduction, tax slab,   
	Employee, Income, Deduction, Employees, Deductions, Employee Income, Income Deduction, Employee Income Deduction, 
	Tds, Employee Tds, Employee Tax, Tax Employee, Tax Income, Taxable Income, Tax Deduct, Tax Deduction, Tax Deducted,
	Employee Taxable Income,employee Tds Tax, Employee Tax Tds, Tds Tax Employee, Tds Tax Income, Tds Taxable Income, 
	Tds Tax Deduct, Tds Tax Deduction, Tds Tax Deducted, Employee Tds Taxable Income,

	
    """,
    'category': "Generic Modules/Human Resources",
    'author': 'GeoTechnosoft',
    'company': 'GeoTechnosoft',
    'website': "https://www.geotechnosoft.com",
    'depends': ['base', 'hr', 'hr_contract', 'hr_payroll_community'],
    'data': [
        'security/ir.model.access.csv',
        'views/income_deduction.xml',
        'views/tds_information.xml',
        'views/tax_slab.xml',
        'views/deduction_description_view.xml',

    ],
    'demo': [],
    'assets': {
        'web.assets_backend': [
        ],
    },

    'images': ['static/description/banner.png'],
    'price': 20,
    'currency': 'USD',
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
