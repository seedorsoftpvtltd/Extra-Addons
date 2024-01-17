from odoo import api, fields, models, _


class WizardReport(models.TransientModel):
    _inherit = 'odoo_mo.monthly_sales'

    def print_excel(self):
        data = {}
        lines = self._get_lines()
        data['lines'] = lines
        val = self.env['ir.actions.report'].search([('report_name','=','odoo_mo_monthlysales.xlsx')])
        val['report_file'] = 'monthly_sales'
        return self.env.ref('odoo_mo_monthlysales.xls_reportid2').report_action([],data=data)