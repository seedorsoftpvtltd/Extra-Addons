from odoo import api, fields, models, _

class Job_access(models.Model):
    _inherit='freight.operation'

    user_id=fields.Many2one('res.users',related='operator_id.employee_id')

class Sale(models.Model):
    _inherit='sale.order'


class ResUsersInh(models.Model):
    _inherit='res.users'

    employee_id = fields.Many2one('hr.employee', readonly=False, store=True)