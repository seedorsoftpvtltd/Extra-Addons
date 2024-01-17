from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta, date
import calendar
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

FETCH_RANGE = 2000

class InsGeneralLedger(models.TransientModel):
    _inherit = "ins.general.ledger"

    def write(self, vals):

        if vals.get('date_range'):
            vals.update({'date_from': False, 'date_to': False})
        if vals.get('date_from') and vals.get('date_to'):
            vals.update({'date_range': False})
            a=vals.get('date_from')
            try:
                date_from = datetime.strptime(a, "%d/%m/%Y")
                formatted_date = date_from.strftime("%Y-%m-%d")
                vals.update({'date_from': formatted_date})
                b = vals.get('date_to')
                date_to = datetime.strptime(b, "%d/%m/%Y")
                formatted_date1 = date_to.strftime("%Y-%m-%d")
                vals.update({'date_to': formatted_date1})
            except:
                pass

        if vals.get('journal_ids'):
            vals.update({'journal_ids': vals.get('journal_ids')})
        if vals.get('journal_ids') == []:
            vals.update({'journal_ids': [(5,)]})

        if vals.get('account_ids'):
            vals.update({'account_ids': vals.get('account_ids')})
        if vals.get('account_ids') == []:
            vals.update({'account_ids': [(5,)]})

        if vals.get('account_tag_ids'):
            vals.update({'account_tag_ids': vals.get('account_tag_ids')})
        if vals.get('account_tag_ids') == []:
            vals.update({'account_tag_ids': [(5,)]})

        if vals.get('analytic_ids'):
            vals.update({'analytic_ids': vals.get('analytic_ids')})
        if vals.get('analytic_ids') == []:
            vals.update({'analytic_ids': [(5,)]})

        if vals.get('analytic_tag_ids'):
            vals.update({'analytic_tag_ids': vals.get('analytic_tag_ids')})
        if vals.get('analytic_tag_ids') == []:
            vals.update({'analytic_tag_ids': [(5,)]})

        if vals.get('partner_ids'):

            vals.update({'partner_ids': vals.get('partner_ids')})
        if vals.get('partner_ids') == []:

            vals.update({'partner_ids': [(5,)]})

        ret = super(InsGeneralLedger, self).write(vals)
        return ret