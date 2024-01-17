# -*- coding: utf-8 -*-
from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    password = fields.Char('Password')
    automatic_user_create = fields.Boolean('Create User Automatically?',
                                           default=True,
                                           copy=False,
                                           help="automatic user \
                                           creation along with employee")
    pwd_email = fields.Selection(
        [('send_pwd', 'Send Passowrd'),
         ('send_link', 'Invitation Link')],
        default='send_pwd',
        help='send password:will send password via email \
        Invitatin Link:Send invitation link to user for \
        reset password'
        )


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    password = fields.Char('Password',
                           related='company_id.password', readonly=False)
    user_auto_creation = fields.Boolean(
        'User Auto Creation',
        related='company_id.automatic_user_create',
        readonly=False, copy=False,
        help="automatic user \
        creation along with employee"
    )

    pwd_email = fields.Selection(related='company_id.pwd_email',
                                 readonly=False
                                 )
