from odoo import fields, models


class ResPartner(models.TransientModel):
    _name = "customer.supplier.wizard"


    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    def print_pdf(self):
        """ Button function for PDF """


        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
        print(self)
        return self.env.ref(
            'customer_supplier_wizard.customer_supplier_report').report_action(self, data)

class ResPartner1(models.TransientModel):
        _name = "supplier.wizard"

        start_date = fields.Date(string='Start Date')
        end_date = fields.Date(string='End Date')

        def print_pdf_supplier(self):
            """ Button function for PDF """

            data = {
                'start_date': self.start_date,
                'end_date': self.end_date,
            }
            print(self)
            return self.env.ref(
                'customer_supplier_wizard.supplier_report').report_action(self, data)

