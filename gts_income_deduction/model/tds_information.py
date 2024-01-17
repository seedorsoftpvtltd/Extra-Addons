from odoo import models, fields, api


class Contract(models.Model):
    _inherit = 'hr.contract'

    annual_salary = fields.Float(string='Annual Salary')
    other_income = fields.Float(string='Other Income Including Interest')
    gross_income = fields.Float(string='Gross Income')
    total_deductions = fields.Float(string='Total Deductions')
    taxable_amount = fields.Float(string='Taxable Amount')
    tax_payable = fields.Float(string='Tax Payable')
    monthly = fields.Boolean('Monthly Deduction ?')
    tax_payable_per_month = fields.Float('TDS Deduction per month')
    deduction_ids = fields.One2many('income.deduction', 'contract_id')

    extra_charges_ids = fields.One2many('extra.charges', 'contract_id', string='Extra Charges')
    tax_slab_id = fields.Many2one('tax.configuration', string='Tax')

    @api.model
    def default_get(self, fields_list):
        res = super(Contract, self).default_get(fields_list)
        deduction_obj = self.env['deduction.description'].search([])
        default_val = []
        for obj in deduction_obj:
            val = (0, 0, {'deduction_id': obj.id, 'amount': 0})
            default_val.append(val)
        res.update({'deduction_ids': default_val})
        return res

    # @api.multi
    # def write(self,values):
    #     # your logic goes here
    #     override_write = super(your_model, self).write(values)
    #     return override_write


    # def write(self, values):
    #     deduction_obj = self.env['deduction.description'].search([])
    #     print('res==============>>>>>>>>>', deduction_obj)
    #     default_val = []
    #     # override_write = self.env['deduction.description'].browse(id).write({'deduction_id': 'obj.id'})
    #     for obj in deduction_obj:
    #         val = (0, 0, {'deduction_id': obj.id, 'amount': 0})
    #         default_val.append(val)
    #     # res = super(Contract, self).write(values)
    #     res = self.env['deduction.description'].browse(id).write({'deduction_id': 'obj.id'})
    #     print('res==============>>>>>>>>>', res)
    #     # res.update({'deduction_ids': default_val})
    #     return res

# #--------------------------------
#     def write(self, vals):
#         result = super(Contract, self).write(vals)
#         if 'deduction_ids' not in vals or 'deduction_ids' in vals:
#             for obj in self:
#                 obj.deduction_ids.write(obj.default_get())
#         return result


    @api.onchange('annual_salary', 'other_income')
    def onchange_gross_income_amount(self):
        if self.annual_salary or self.other_income:
            self.gross_income = 0.00
            self.gross_income = self.annual_salary + self.other_income
        else:
            self.gross_income = 0.00

    @api.onchange('deduction_ids')
    def onchange_deduction_amount(self):
        if self.deduction_ids:
            total_deduct_cost = 0.00
            for line in self.deduction_ids:
                total_deduct_cost += line.amount
            self.total_deductions = total_deduct_cost
        else:
            self.total_deductions = 0.00

    @api.onchange('gross_income', 'total_deductions')
    def onchange_taxable_income_amount(self):
        if self.gross_income or self.total_deductions:
            self.taxable_amount = 0.0
            self.taxable_amount = self.gross_income - self.total_deductions
        else:
            self.taxable_amount = 0.00


    @api.onchange('taxable_amount', 'extra_charges_ids')
    def onchange_to_tax_payable(self):
        if self.taxable_amount:
            self.tax_payable = 0.0
            if self.extra_charges_ids:
                total_cost = 0.00
                for line in self.extra_charges_ids:
                    total_cost += line.amount
                    print('total_cost', total_cost)
                self.tax_payable = total_cost + (self.taxable_amount * ((self.tax_slab_id.tax)/100))

            else:
                self.tax_payable = self.taxable_amount * ((self.tax_slab_id.tax)/100)
        else:
            self.tax_payable = 0.00

    @api.onchange('taxable_amount')
    def onchange_taxable_amount(self):
        if self.taxable_amount:
            tax_slabs = self.env['tax.configuration'].search([])
            if tax_slabs:
                for tax_slab in tax_slabs:
                    if self.taxable_amount >= tax_slab.range_from and self.taxable_amount <= tax_slab.range_to:
                        self.tax_slab_id = tax_slab.id

    @api.onchange('monthly', 'tax_payable')
    def onchange_tax_payable_per_month(self):
        if self.monthly == True:
            self.tax_payable_per_month = 0.0
            self.tax_payable_per_month = self.tax_payable/12
        else:
            self.tax_payable_per_month = 0.0
