# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import Warning, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import datetime


class Users(models.Model):
    _inherit = 'res.users'

    inactive_date = fields.Datetime('Inactive Date')

    def cron_inactive_user_accounts(self):
        config_data = self.env['res.config.settings'].sudo().get_values()
        inactive_days = config_data.get('inactive_days')
        if inactive_days > 0:
            end_date = datetime.date.today() - datetime.timedelta(days=inactive_days)
            end_date = datetime.datetime.strftime(end_date, '%Y-%m-%d 00:00:00')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d 00:00:00')
            admin_ids = [self.env.ref('base.user_admin').id, self.env.ref('base.user_root').id]
            user_ids = self.search([('id', 'not in', admin_ids)]).filtered(lambda r: (not r.login_date or r.login_date < end_date) and r.id not in admin_ids)
            if user_ids:  # Inactivate Users
                user_ids.write({'inactive_date': datetime.datetime.today()})
                user_ids.toggle_active()
        return True
