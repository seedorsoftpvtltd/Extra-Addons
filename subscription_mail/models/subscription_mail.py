from odoo import fields, models, api, _
from datetime import datetime,timedelta



class SaleFou(models.Model):
    _inherit = 'sale.order'

    subs_startsale = fields.Datetime(string="Sub Start Date", related='subscription_ids.start_date')
    subs_endsale = fields.Datetime(string="Sub End Date", related='subscription_ids.end_date')

class SubscriptionRemainder(models.Model):
    _inherit = 'account.move'

    is_subscription = fields.Boolean(string="Is Subscription")
    #sub_ids = fields.Many2one("subscription.subscription", string="Sub Ids")
    #subs_startmove = fields.Datetime(string="Sub Start Date", related='sub_ids.start_date')
    #subs_endmove = fields.Datetime(string="Sub End Date", related='sub_ids.end_date')

    @api.model
    def subscription_mail(self):
        rem_days= int(self.env['ir.config_parameter'].sudo().get_param('subscription_mail.remainder_days'))
        print(rem_days)
        rem_year_days = int(self.env['ir.config_parameter'].sudo().get_param('subscription_mail.remainder_year_days'))
        print(rem_year_days)
        invoices=self.env['account.move'].search([('state', '=', 'draft'),('type','=','out_invoice'),('is_subscription','=',True),('startsubs_date','!=',False),('endsubs_date','!=',False)])
        # print(invoices)
        today_date = datetime.now().date()
        # print(today_date)

        # print(type(today_date))
        # print(invoices)
        for rec in invoices:
            enddate = rec.mapped('endsubs_date')
            edate = list()
            for r in enddate:

                if r != False:
                    edate.append(r)

            enddate = edate[0]
            enddate = enddate.date()
            startdate = rec.mapped('startsubs_date')
            sdate = list()
            for r in startdate:

                if r != False:
                    sdate.append(r)

            startdate = sdate[0]
            startdate = startdate.date()
            # print(startdate)
            # print(enddate)
            if enddate == "":
                print('```````````````````````````````````')
                print('{0}:No End date in Subscription Invoice'.format(today_date))
                print('```````````````````````````````````')
                return True
            # days= rem_days
            remaining_date = enddate - startdate
            ree_date = remaining_date.days
            #print(remaining_date)
            if ree_date < 365:
                days = rem_days
            else:
                days = rem_year_days
            remainder_date = enddate - timedelta(days=days)
            sub_remainder_date = remainder_date
            print(sub_remainder_date)
            if sub_remainder_date == today_date:
                template_id = \
                    self.env['ir.model.data'].get_object_reference('subscription_mail', 'mail_schedule')[1]
                mail_template_obj = self.env['mail.template'].browse(template_id)
                values = mail_template_obj.generate_email(rec.id, fields=None)
                mail_mail_obj = self.env['mail.mail']
                msg_id = mail_mail_obj.sudo().create(values)
                if msg_id:
                    # mail_mail_obj.send([msg_id])
                    msg_id.sudo().send()
                    # msg_id = self.env['mail_schedule'].send_mail(template_id.id, force_send=True)
                    # print("hii")




            else:
                print("No subscription is in its end date")

        else:
            print("No sub")


        return True

    @api.model
    def subscription_notify(self):

        _inherit = "mail.message"

        invoices = self.env['account.move'].search(
            [('state', '=', 'draft'), ('type', '=', 'out_invoice'), ('is_subscription', '=', True),
             ('subs_endmove', '!=', False), ('subs_startmove', '!=', False)])
        for rec in invoices:


            message_data = {

                'type': 'notification',

                'subject': "Subscription Remainder",

                'body': 'email',

                'partner_ids': [(4, rec.user_id.partner_id.id)],
                'message_type': 'notification'

            }
            # mail_message_obj = self.env['mail.message']
            messages = super(SubscriptionRemainder, self).create(message_data)
            print("Message")
            mail_id = self.env['mail.message'].create()
