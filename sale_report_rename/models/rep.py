from odoo import api, fields, models, _


class WizardReport(models.TransientModel):
    _inherit = 'odoo_mo.monthly_sales'

    def print_excel(self):
        data = {}
        lines = self._get_lines()
        data['lines'] = lines
        print(lines)

        return self.env.ref('sale_report_rename.xls_report_id24').report_action([],data=data)