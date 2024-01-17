from odoo import fields, models


class CargoStatusReport(models.TransientModel):
    _name = "cargo.status.wizard"

    def get_default_date(self):

        job=self.env['sub.job'].search([], order="job_date", limit=1)
        date=job.job_date.strftime("%Y-%m-%d")

        return date

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    partner_id=fields.Many2many('res.partner',string='Client Name')




    def print_excel(self):
        """ Button function for Xlsx """
        client=[]
        for rec in self.partner_id:
            client.append(rec.id)

        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'client_name':client,
            
        }



        return self.env.ref(
            'cargo_status_report.excel_report_xlsx').report_action(self, data)
