# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, _
from odoo.exceptions import UserError



class ChangePasswordUser(models.TransientModel):
    _inherit = 'change.password.user'

    pswd_change_secure_pin = fields.Char(
        string='Secure Pin',
    )
#    group_custom_secure_admin = fields.Boolean(string='Secure Admin PIN',
#        compute="_compute_custom_secure_admin",
#        help="Allows to change Paswrod for admin user"
#    )


#    def _compute_custom_secure_admin(self):
#        for rec in self:
#            rec.group_custom_secure_admin = True if rec.user_id.has_group("base.group_erp_manager") else False

    def change_password_button(self):
        for line in self:
            if line.user_id.has_group("base.group_erp_manager") and line.user_id.pswd_change_secure_pin and line.user_id.pswd_change_secure_pin != line.pswd_change_secure_pin:
                raise UserError(_("You can not change password of %s as PIN validation found wrong,You can try by closing change password screen again.")%(line.user_id.name))
        return super(ChangePasswordUser, self).change_password_button()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: