# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo import tools

class PayslipAnalysis(models.Model):
    _name = "payslip.analysis"
    _description = "Payslip Analysis"
    _auto = False

    payslip_id = fields.Many2one("hr.payslip", string="Payslip")
    employee_id = fields.Many2one("hr.employee", string="Employee")
    department_id = fields.Many2one("hr.department", string="Department")
    parent_id = fields.Many2one("hr.employee", string="Manager")
    job_id = fields.Many2one("hr.job", string="Job Position")
    date_start = fields.Date(string="Date Start")
    date_end = fields.Date(string="Date End")
    rule_id = fields.Many2one("hr.salary.rule",string="Salary Rule")
    structure_id = fields.Many2one("hr.payroll.structure", string="Salary Structure")
    run_id = fields.Many2one("hr.payslip.run", string="Payslip Run")
    state = fields.Selection([("draft", "Draft"),("done", "Done")], string="Status")
    amount = fields.Float("Amount")

    def _select(self):
        select_str = """
        SELECT
            payslip_line.id AS id,
            payslip.id AS payslip_id,
            employee.id AS employee_id,
            employee.department_id AS department_id,
            employee.job_id AS job_id,
            payslip_line.salary_rule_id AS rule_id,
            payslip.state AS state,
            payslip.date_from AS date_start,
            payslip.date_to AS date_end,
            employee.parent_id AS parent_id,
            payslip.struct_id AS structure_id,
            payslip.payslip_run_id AS run_id,
            SUM(payslip_line.rate) AS rate,
            SUM(payslip_line.amount) AS amount,
            SUM(payslip_line.quantity) AS quantity,
            SUM(payslip_line.total) AS total
        """
        return select_str

    def _from(self):
        from_str = """
        hr_payslip_line AS payslip_line
        JOIN hr_payslip AS payslip ON
            payslip_line.slip_id = payslip.id
        JOIN hr_employee AS employee ON
            payslip.employee_id = employee.id        
        """
        return from_str

    def _group_by(self):
        group_str = """
        GROUP BY
            payslip_line.id,
            payslip.id,
            employee.id,
            employee.department_id,
            employee.job_id,
            payslip_line.salary_rule_id,
            payslip.state,
            payslip.date_from,
            payslip.date_to,
            employee.parent_id,
            payslip.struct_id,
            payslip.payslip_run_id
        """
        return group_str

    def init(self):
        tools.drop_view_if_exists(self._cr, 'payslip_analysis')
        self._cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
        )""" % (
            self._table,
            self._select(),
            self._from(),
            self._group_by()
        ))