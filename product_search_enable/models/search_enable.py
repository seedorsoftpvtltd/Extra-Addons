from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    income_account = fields.Many2one(
        'account.account',
        string='Income Account',
        help='This field is used to store the income account.',
        compute='_compute_income_account',
        inverse='_inverse_income_account',
        store=True)
    expense_account = fields.Many2one(
        'account.account',
        string='Expense Account',
        help='This field is used to store the Expense account.',
        compute='_compute_expense_account',
        inverse='_inverse_expense_account',
        store=True)

    @api.depends('property_account_income_id')
    def _compute_income_account(self):
        for record in self:
            #if not record.company_id:
                record.income_account = record.property_account_income_id

    def _inverse_income_account(self):
        for record in self:
            #if not record.company_id:
                record.property_account_income_id = record.income_account

    @api.depends('property_account_expense_id')
    def _compute_expense_account(self):
        for record in self:
            #if not record.company_id:
                record.expense_account = record.property_account_expense_id

    def _inverse_expense_account(self):
        for record in self:
            #if not record.company_id:
                record.property_account_expense_id = record.expense_account


# class product_template(models.Model):
#     _inherit='product.template'
#
#     income_account = fields.Many2one('account.account', string="Income Account")
#
#     @api.model
#     def _migrate_income_account(self):
#         """Copy the value of the property_account_income_id field for each company to the new income_account field."""
#         print("ggggggggggggggg")
#         for company in self.env['res.company'].search([]):
#             print("ggggggggggggggguuuuuuuuuuuuuuuuuuuuuuuuuu")
#             self.env.cr.execute("""
#                     UPDATE product_template
#                      SET income_account  = (
#                       SELECT CAST(value_reference AS integer)
#                       FROM ir_property
#                       WHERE name = 'property_account_income_id'
#                       AND res_id = CONCAT('product.template,', product_template.id)
#                       AND company_id = %s
#                                          )
#                       WHERE company_id = %s
#
#                 """, (company.id, company.id))
#
#             # call the write() method to update the income_account field in the database
#             self.env['product.template'].search([('company_id', '=', company.id)]).write(
#                 {'income_account': self.income_account})
#
#     def init(self):
#         """Run the migration script when the module is installed."""
#         self._migrate_income_account()

# class ProductProduct(models.Model):
#     _inherit = "product.product"
#
#     property_account_income_id = fields.Many2one('account.account', company_dependent=True,store=True,readonly=False,
#         string="Income Account",
#         domain="['&', ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
#         help="Keep this field empty to use the default value from the product category.",
#         related='product_tmpl_id.property_account_income_id')
#     property_account_expense_id = fields.Many2one('account.account', company_dependent=True, store=True,readonly=False,
#         string="Expense Account",
#         domain="['&', ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
#         help="Keep this field empty to use the default value from the product category. "
#             "If anglo-saxon accounting with automated valuation method is configured, "
#             "the expense account on the product category will be used.",
#         related='product_tmpl_id.property_account_expense_id')


