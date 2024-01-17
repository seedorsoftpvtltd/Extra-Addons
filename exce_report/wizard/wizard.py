from odoo import models, fields, api


class MyWizard(models.TransientModel):
    _name = 'excel_wizard'
    report_type = fields.Selection([
        ('fcy', 'FCY Report'),
        ('outstanding', 'Outstanding Report'),
        ('overdue', 'Overdue Report'),
    ], string='Report Type', required=True)
    # Define fields for the wizard


    # Define the action to be taken when the wizard is confirmed

    def get_report_data(self):
        data = {
            'report_type': self.report_type,

        }
        return data
    def print_fcy_xls(self):


        typess = self.get_report_data()
        print(typess)
        return self.env.ref('exce_report.report_overdue_xls_print').report_action(self,typess)