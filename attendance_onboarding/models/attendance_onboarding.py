from odoo import fields, models, api, _

class Attendance(models.Model):
    _inherit = "hr.attendance"

    @api.model
    def onboarding_step2_action(self):
        # idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Regularization'),
            'res_model': 'attendance.regular',
            'view_mode': 'tree',
            'limit': 99999999,
            'views':[[False, 'list'], [False, 'form']],
        }

    @api.model
    def onboarding_step1_action(self):
        # idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'res_model': 'hr.attendance',
            'type': 'ir.actions.client',
            'tag': 'hr_attendance_my_attendances',
            'target': 'current'
        }

    @api.model
    def onboarding_step3_action(self):
        # idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Import'),
            'res_model': 'hr.document',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views':[[False, 'kanban'], [False, 'form'],[False, 'tree']],
        }

#    @api.model
#    def onboarding_step4_action(self):
        # idd = self.env.ref('hr.view_department_tree').id
#        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
#        return {
#            'type': 'ir.actions.act_window',
 #           'name': _('Google Sync'),
  #          'res_model': 'google.spreadsheet.import',
   #         'view_mode': 'kanban',
    #        'limit': 99999999,
     #       'views':[[False, 'kanban'], [False, 'form'],[False, 'tree']],
      #  }

    @api.model
    def onboarding_step5_action(self):
        # idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Biometric'),
            'res_model': 'zk.machine',
            'view_mode': 'tree',
            'limit': 99999999,
            'views': [[False, 'list'], [False, 'form']],
        }
