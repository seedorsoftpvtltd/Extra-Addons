from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.http import request

class activity_log(models.Model):
    _name = 'activity.log'
    _description = 'Activity Log'
    _order = 'id desc'

    name = fields.Char('Record Name')
    login_log_id = fields.Many2one('login.log', 'Session')
    # user_id = fields.Many2one('res.users', 'User', related='login_log_id.user_id', store=True)
    # user_id = fields.Many2one('res.users', 'User', compute='_get_user_id', store=True)
    user_id = fields.Many2one('res.users', 'User')
    model_id = fields.Many2one('ir.model', 'Model')
    # edit_value_id = fields.Many2one('edit.value', 'Edit Value')
    edit_value_ids = fields.One2many('edit.value', 'activity_log_id', 'Edit Value')
    res_id = fields.Integer('Record ID')
    action = fields.Selection([('create','Create'),('edit','Modify'),('delete','Delete')], string='Action')
    value = fields.Html('Changes')
    has_change_view = fields.Boolean('Has Change View', compute='_get_has_change_view')

    # @api.depends('login_log_id','login_log_id.user_id')
    # def _get_user_id(self):
    #     for record in self:
    #         record.user_id = record.login_log_id.user_id.id

    @api.depends('edit_value_ids')
    def _get_has_change_view(self):
        for record in self:
            record.has_change_view = bool(record.edit_value_ids)

    def unlink(self):
        for record in self:
            try:
                model = request.params['model']
            except:
                model = ''
            if record.login_log_id.user_id.id == self.env.user.id and model != 'base.module.uninstall':
                raise UserError(_("You cant delete your own sessions and activitiy."))
        return super(activity_log, self).unlink()

    def action_open_edit_view(self):
        action = {
            'name': _('Changes'),
            'view_mode': 'form',
            'res_model': 'edit.value',
            'type': 'ir.actions.act_window',
            'res_id': self.edit_value_id.id,
            'target': 'new'
        }
        return action

    def action_open_record(self):
        action = {
            'name': self.model_id.name,
            'view_mode': 'form',
            'res_model': self.model_id.model,
            'type': 'ir.actions.act_window',
            'res_id': self.res_id,
            'target': 'current'
        }
        return action