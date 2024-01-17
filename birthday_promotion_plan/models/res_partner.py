from datetime import datetime, timedelta
from odoo import SUPERUSER_ID
from odoo import api, fields, models, _


class res_partner(models.Model):
    _inherit = "res.partner"

    @api.depends("birthdate")
    def _compute_birthdate_month(self):
        for rec in self:
            if rec.birthdate:
                date = datetime.strptime(str(rec.birthdate), "%Y-%m-%d")
                rec.birthdate_month = date.month

    birthdate = fields.Date(string="Date Of Birth")
    birthday_promotion_range = fields.Integer("Birthday Promotion Range", default=10)
    birthdate_month = fields.Integer(
        "Birthday Month", compute="_compute_birthdate_month", store=True
    )

    @api.model
    def _cron_birthday_reminder(self):
        su_id = self.env["res.partner"].browse(SUPERUSER_ID)
        today = datetime.now().date()
        for partner in self.search(
            [
                ('customer_rank', '>', 0),
                ("birthdate", "!=", False),
                ("birthday_promotion_range", "!=", False),
            ]
        ):
            whose_birthdate_is = today + timedelta(
                days=partner.birthday_promotion_range
            )
            if str(partner.birthdate) == str(whose_birthdate_is):
                template_id = self.env.ref(
                    "birthday_promotion_plan.email_template_edi_birthday_reminder"
                )
                if template_id:
                    msg_id = self.env["mail.mail"].create({
                        'email_from':su_id.email,
                        'email_to':partner.email,
                        'model':'res.partner',
                        'subject':'Birthday Promotion Vouchers',
                        'body_html': template_id.body_html
                    })
                    if msg_id:
                        self.env["mail.mail"].send([msg_id])
        return True
