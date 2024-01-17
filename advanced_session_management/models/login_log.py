import odoo
from odoo import models, fields, api, http, _
import re
import os
from datetime import datetime, timedelta
from odoo.http import request
from odoo.exceptions import UserError
import werkzeug

class login_log(models.Model):
    _name = 'login.log'
    _description = 'Login Log'
    _order = 'id desc'

    name = fields.Char('Name')
    user_id = fields.Many2one('res.users', 'User')
    user_agent = fields.Char('User Agent')
    browser = fields.Char('Browser')
    device = fields.Char('Device')
    os = fields.Char('OS')
    ip = fields.Char('IP')
    session_id = fields.Char('Session ID')
    login_date = fields.Datetime('Login Date')
    logout_date = fields.Datetime('Logged out Date')
    state = fields.Selection([('active','Active'),('close','Closed')], string='Status')
    activity_log_ids = fields.One2many('activity.log', 'login_log_id', 'Activity Logs')
    country = fields.Char('Country')
    loc_state = fields.Char('State')
    city = fields.Char('City')
    url = fields.Char('URL', compute='_get_url')

    def _get_url(self):
        self.url = '/web#id='+ str(self.id) +'&model=login.log&view_type=form'

    def location_lookup_ao(self):
        self.ensure_one()
        if self.ip:
            return {
                'type': 'ir.actions.act_url',
                'name': "Location",
                'target': 'new',
                'url': 'https://www.ip2location.com/demo/' + self.ip,
            }

    def logout_button(self):
        not_found = True
        db_name = ''
        for record in self:
            if record.state == 'active':
                for fname in os.listdir(odoo.tools.config.session_dir):
                    path = os.path.join(odoo.tools.config.session_dir, fname)
                    name = re.split('_|\\.', fname)
                    session_store = http.root.session_store
                    get_session = session_store.get(name[1])
                    if get_session.db and get_session.uid == record.user_id.id and get_session.sid == record.session_id:
                        record.sudo().write({'state':'close','logout_date':datetime.now()})
                        os.unlink(path)
                        get_session.logout(keep_db=True)
                        not_found = False
                        if get_session.sid == request.session.sid:
                            db_name = get_session.db
            if not_found:
                record.sudo().write({'state':'close','logout_date':datetime.now()})
        if db_name:
            return {
                    'type': 'ir.actions.act_url',
                    'target': 'self',
                    'url': '/web?db=' + db_name,
                }

    @api.model
    def create(self, vals):
        # vals['name'] = str(self.env['res.users'].browse(vals['user_id']).name) + '/'  + str(vals['login_date'])[:10] + '/' + vals['browser'] + '/' + vals['device'] + '/' + '00' + str(self.env['ir.sequence'].sudo().next_by_code('login.log')) or _('New')
        res = super(login_log, self).create(vals)
        res.name = 'S00' + str(self.env['ir.sequence'].sudo().next_by_code('login.log')) or _('New')
        config_parameter_obj = self.env['ir.config_parameter']
        send_mail = config_parameter_obj.search([('key','=','advanced_session_management.send_mail')],limit=1)
        if send_mail.value == 'True' and res.user_id.has_group('advanced_session_management.group_login_log_user_ah'):
            template = self.env.ref('advanced_session_management.new_session_start_mail_template_ah', raise_if_not_found=False)
            if res and res.id and template:
                template.sudo().send_mail(res.id, force_send=True)
        return res 

    def unlink(self):
        for record in self:
            try:
                model = request.params['model']
            except:
                model = ''
            if record.user_id.id == self.env.user.id and model != 'base.module.uninstall':
                raise UserError(_("For the security purpose, you can't delete your own sessions and activities."))
            record.activity_log_ids.unlink()
            record.logout_button()
            
        return super(login_log, self).unlink()
    
    def remove_old_log(self):
        config_parameter_obj = self.env['ir.config_parameter']
        value = config_parameter_obj.search([('key','=','advanced_session_management.remove_sesions')],limit=1)
        if value and value.value:
            value = int(value.value)
        else:
            value = 7
        for record in self.search([('state','=','close'),('logout_date','>=',datetime.now() + timedelta(value))]):
            record.unlink()
        for record in self.env['activity.log'].search([('create_date','>=',datetime.now() + timedelta(value))]):
            record.unlink()
