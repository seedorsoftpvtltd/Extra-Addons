# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Task(models.Model):
    _inherit = "project.task"

    job_insp_ids = fields.One2many(
        'job.order.inspection',
        'task_id',
    )

    def show_inspection(self):
        job_insp = self.mapped('job_insp_ids')
        action = self.env.ref('job_inspection.action_job_order_inspection').read()[0]
        action['domain'] = [('id', 'in', job_insp.ids)]
        action['context'] = {'default_task_id':self.id,'default_project_id':self.project_id.id,'default_analytic_id':self.project_id.analytic_account_id.id,'default_user_id':self.user_id.id}
        return action

    # @api.multi
    # def show_inspection(self):
    #     self.ensure_one()
    #     res = self.env.ref('job_inspection.action_job_order_inspection')
    #     res = res.read()[0]
    #     res['domain'] = str([('task_id','=', self.id)])
    #     return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
