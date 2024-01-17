from odoo import api, fields, models, _
from odoo.addons.mail.models.mail_mail import MailMail
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class MailExtend(models.Model):
    _inherit = "mail.mail"

    def unlink(self):
        mail_msg_cascade_ids = [mail.mail_message_id.id for mail in self if not mail.notification]
        res = super(MailMail, self)
        if mail_msg_cascade_ids:
            self.env['mail.message'].browse(mail_msg_cascade_ids)
        return res

#class CroneExtend(models.Model):
#    _inherit = "ir.crone"

    
