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


from odoo import api, exceptions, fields, models, _


class MailChatterVisibility(models.Model):
    _name = 'mail.chatter.visibility'
    _description = "Visibility of Mail Chatter"

    model_name = fields.Char('Model Name')

    res_id = fields.Char('Res Id')

    show_lognote = fields.Boolean('Show Lognote')

    show_mailmessage = fields.Boolean('Show Mail Message')

    show_activity = fields.Boolean('Show Activity')

    @api.model
    def mail_chatter_record_clean(self):
        mail_cron = self.env['mail.chatter.visibility'].search([])
        chatter_visibility_ids = self.env['mail.chatter.visibility']
        for mail in mail_cron:
            record = self.env[mail.model_name].sudo().search([('id', '=', int(mail.res_id))])
            if not record:
                chatter_visibility_ids |= record

        if chatter_visibility_ids:
            chatter_visibility_ids.unlink()


    def get_chatter_visibility_data(self,model,res_id):

        record_exists = self.sudo().search([
                            ('model_name','=',model),
                            ('res_id','=',str(res_id))
                        ])

        if record_exists:
            return {
                'mail_message' : record_exists.show_mailmessage,
                'lognote' : record_exists.show_lognote,
                'activity' : record_exists.show_activity,
            }
        else:
            return {
                'mail_message' : True,
                'lognote' : True,
                'activity' : True,
            }


    def update_chatter_visibility(self,type,value,res_id,model):
        record_exists = self.sudo().search([
                            ('model_name','=',model),
                            ('res_id','=',str(res_id))
                        ])

        if record_exists:
           record_exists.write({type : value})
        else:
            chatter_visibility_id = self.sudo().create({
                                        'model_name' : model,
                                        'res_id' : str(res_id),
                                        'show_lognote' : True,
                                        'show_mailmessage' : True,
                                        'show_activity' : True
                                    })
            if type == 'show_lognote':
                chatter_visibility_id.show_lognote = value

            elif type == 'show_mailmessage':
                chatter_visibility_id.show_mailmessage = value

            elif type == 'show_activity':
                chatter_visibility_id.show_activity = value

        return True
