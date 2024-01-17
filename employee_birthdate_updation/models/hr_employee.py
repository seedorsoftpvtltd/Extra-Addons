from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.onchange('spouse_complete_name', 'spouse_birthdate')
    def onchange_spouse(self):
        relation = self.env.ref('hr_employee_updation.employee_relationship')
        lines_info = []
        spouse_name = self.spouse_complete_name
        date = self.spouse_birthdate
        if spouse_name and date:
            lines_info.append((0, 0, {
                'member_name': spouse_name,
                'relation_id': relation.id,
                'birth_date': date,
            })
                              )
            self.fam_ids = [(5, 0, 0)] + lines_info

    # @api.onchange('spouse_complete_name', 'spouse_birthdate')
    # def onchange_spouse(self):
    #     relation = self.env.ref('hr_employee_updation.employee_relationship')
    #     lines_info = []
    #     spouse_name = self.spouse_complete_name
    #     date = self.spouse_birthdate
    #     try:
    #         if spouse_name and date:
    #             lines_info.append((0, 0, {
    #                 'member_name': spouse_name,
    #                 'relation_id': relation.id,
    #                 'birth_date': date,
    #             }))
    #     except Exception as e:
    #         # Log the exception or print an error message for debugging
    #         print(f"An error occurred: {str(e)}")
    #     else:
    #         print(self.fam_ids, 'self.fam_ids  1')
    #         print(lines_info, 'lines_info   2')
    #         self.fam_ids = [(5,)] + lines_info
