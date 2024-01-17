# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016-Today Geminate Consultancy Services (<http://geminatecs.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import api, models,fields,_


class MailActivityInherit(models.Model):

    _inherit = "mail.activity"

    def read(self, fields=None, load='_classic_read'):
        
        res = super(MailActivityInherit,self).read(fields, load)
        if 'chatter_model' in self._context and 'chatter_res_id' in self._context:
            record_exists = self.env['mail.chatter.visibility'].sudo().search([
                                ('model_name','=',self._context.get('chatter_model')),
                                ('res_id','=',self._context.get('chatter_res_id')),
                            ],limit=1)

            if record_exists:
                message_dup_dict = []
                add_activity = record_exists.show_activity
                for mes_id in res:
                    mail_message_id = self.browse(mes_id.get('id'))
                    if mail_message_id and add_activity:
                        message_dup_dict.append(mes_id)
                return message_dup_dict
        return res
