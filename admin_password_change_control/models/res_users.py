# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from lxml import etree


class ResUsers(models.Model):
    _inherit = 'res.users'

    pswd_change_secure_pin = fields.Char(
        string = "Password PIN",
        copy = False,
        password=True,
    )
    group_custom_secure_admin = fields.Boolean(
        string='Hide Secure PIN for User',
        compute="_compute_custom_secure_admin",
        help="Allows to change Password for admin user"
    )
    group_readonly_custom_secure_admin = fields.Boolean(
        string='Readonly for user Secure Admin PIN',
        compute="_compute_readonly_custom_secure_admin",
        help="Allows to change Password for admin user"
    )


    def _compute_custom_secure_admin(self):#To Hide Secure Pin on Other users (Who are not admin user)
        for rec in self:
            rec.group_custom_secure_admin = True if rec.has_group("base.group_erp_manager") else False
    
    def _compute_readonly_custom_secure_admin(self):#To readonly Secure Pin for other user's
        for rec in self:
            rec.group_readonly_custom_secure_admin = True if rec.has_group("base.group_erp_manager") and self.env.uid == rec.id else False

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(ResUsers, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(result['arch'])
            for node in doc.xpath("//field[@name='pswd_change_secure_pin']"):
                node.set('password', 'True')
            result['arch'] = etree.tostring(doc, encoding='unicode')
        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
