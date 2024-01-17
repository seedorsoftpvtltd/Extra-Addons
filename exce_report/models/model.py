from odoo import models, fields, api, _

class Res_Partner(models.Model):
    _inherit='res.partner'

    report_type=fields.Selection(
        [("fcy", "Fcy Report"), ("overdue", "Overdue Payments"),
         ("bl", "BL Details Report")],
        default="fcy",
        string="Report Type",)

    def action_print_xls(self):
        return self.env.ref('exce_report.report_xls_print').report_action(self)
    def action_print_supplier_xls(self):
        return self.env.ref('exce_report.report_supplier_xls_print').report_action(self)
    # def action_print_overdue_xls(self):
    #     # return self.env.ref('exce_report.report_xls_print').report_action(self)
    #     return {
    #         'name': 'Select Report Type',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'excel_wizard',
    #         'view_mode': 'form',
    #         'target': 'new',
    #     }
    def action_print_overduereport_xls(self):
        return self.env.ref('exce_report.report_overduereport_xls_print').report_action(self)