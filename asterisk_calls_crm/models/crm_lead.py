import logging
from phonenumbers import phonenumberutil
import phonenumbers
from odoo import api, models, tools, fields, release, _
from odoo.exceptions import ValidationError, UserError

logger = logging.getLogger(__name__)


class Lead(models.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'

    asterisk_calls_count = fields.Integer(compute='_get_asterisk_calls_count',
                                          string=_('Calls'))
    phone_normalized = fields.Char(compute='_get_phone_normalized',
                                   index=True, store=True)
    mobile_normalized = fields.Char(compute='_get_phone_normalized',
                                    index=True, store=True)
    if release.version_info[0] >= 12:
        partner_address_phone_normalized = fields.Char(
            compute='_get_phone_normalized', index=True, store=True)

    def write(self, values):
        res = super(Lead, self).write(values)
        # Comment out as we do not cache 
        #if res:
        #    self.pool.clear_caches()
        return res

    def unlink(self):
        res = super(Lead, self).unlink()
        # Comment out as we do not cache 
        #if res:
        #    self.pool.clear_caches()
        return res

    @api.model
    def create(self, vals):
        res = super(Lead, self).create(vals)
        try:
            if self.env.context.get('create_call_lead'):
                call = self.env['asterisk_calls.call'].browse(
                    self.env.context['create_call_lead'])
                call.lead = res.id
        except Exception as e:
            logger.exception(e)
        # Comment out as we do not cache 
        #if res:
        #    self.pool.clear_caches()
        return res

    @api.depends('phone', 'mobile', 'country_id')
    def _get_phone_normalized(self):
        for rec in self:
            if rec.phone:
                rec.phone_normalized = rec.normalize_phone(rec.phone)
            if rec.mobile:
                rec.mobile_normalized = rec.normalize_phone(rec.mobile)
            if release.version_info[0] >= 12 and rec.partner_address_phone:
                rec.partner_address_phone_normalized = rec.normalize_phone(
                    rec.partner_address_phone)

    def _get_country_code(self):
        if self and self.country_id:
            return self.country_id.code
        elif self and self.partner_id and self.partner_id.country_id:
            return self.partner_id._get_country_code()
        else:
            if self.env.user and self.env.user.company_id.country_id:
                # Return Odoo's main company country
                return self.env.user.company_id.country_id.code

    def normalize_phone(self, number):
        self.ensure_one()
        country_code = self._get_country_code()
        try:
            phone_nbr = phonenumbers.parse(number, country_code)
            if phonenumbers.is_possible_number(phone_nbr) or \
                    phonenumbers.is_valid_number(phone_nbr):
                number = phonenumbers.format_number(
                    phone_nbr, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.phonenumberutil.NumberParseException:
            pass
        except Exception as e:
            logger.warning('Normalize phone error: %s', e)
        # Strip the number if no phone validation installed or parse error.
        number = number.replace(' ', '')
        number = number.replace('(', '')
        number = number.replace(')', '')
        number = number.replace('-', '')
        return number

    def _get_asterisk_calls_count(self):
        for rec in self:
            rec.asterisk_calls_count = self.env[
                'asterisk_calls.call'].search_count([('lead', '=', rec.id)])

    def _search_lead_by_number(self, number):
        # Odoo < 12 does not have partner_address_phone field.
        open_stages_ids = [k.id for k in self.env['crm.stage'].search(
            [('is_won', '=', False)])]
        if release.version_info[0] < 12:
            domain = [
                ('active', '=', True),
                ('stage_id', 'in', open_stages_ids),
                '|',
                ('phone_normalized', '=', number),
                ('mobile_normalized', '=', number)]
        else:
            domain = [
                ('active', '=', True),
                ('stage_id', 'in', open_stages_ids),
                '|', '|',
                ('phone_normalized', '=', number),
                ('mobile_normalized', '=', number),
                ('partner_address_phone', '=', number)]
        # Get last open lead
        found = self.env['crm.lead'].search(domain, order='id desc')
        if len(found) == 1:
            logger.debug('FOUND LEAD %s BY NUMBER %s', found[0].id, number)
            return found[0]
        elif len(found) > 1:
            logger.warning('[ASTCALLS] MULTIPLE LEADS FOUND BY NUMBER %s', number)
            return found[0]
        else:
            logger.debug('LEAD BY NUMBER {} NOT FOUND'.format(number))
    
    def get_lead_by_number(self, number, country_code=None):
        if not number or 'unknown' in number or number == 's':
            logger.debug('GET LEAD BY NUMBER NO NUMBER PASSED')
            return
        lead = None
        # 1. Convert to E.164 and make a search
        e164_number = self._format_number(
            number, country_code=country_code, format_type='e164')
        lead = self._search_lead_by_number(e164_number)
        # 2. Make a search as as.
        if not lead:
            lead = self._search_lead_by_number(number)
        # 3. Add + and make a search.
        if not lead:
            number_plus = '+' + number if number[0] != '+' else number
            lead = self._search_lead_by_number(number_plus)
        logger.debug('GET LEAD BY NUMBER RESULT: %s',
                     lead.id if lead else None)
        return lead

    def _format_number(self, number, country_code=None, format_type='e164'):
        # Strip formatting if present
        number = number.replace(' ', '')
        number = number.replace('(', '')
        number = number.replace(')', '')
        number = number.replace('-', '')
        if len(self) == 1 and not country_code:
            # Called from partner object
            country_code = self._get_country_code()
            logger.debug(
                'COUNTRY FOR LEAD %s CODE %s', self, country_code)
        elif not country_code:
            # Get country code for requesting account
            country_code = self.env.user.partner_id._get_country_code()
            logger.debug('LEAD GOT COUNTRY CODE %s FROM ENV USER', country_code)
        elif not country_code:
            logger.debug('LEAD COULD NOT GET COUNTRY CODE')
        if country_code is False:
            # False -> None
            country_code = None
        try:
            phone_nbr = phonenumbers.parse(number, country_code)
            if not phonenumbers.is_possible_number(phone_nbr):
                logger.debug('LEAD PHONE NUMBER {} NOT POSSIBLE'.format(number))
            elif not phonenumbers.is_valid_number(phone_nbr):
                logger.debug('LEAD PHONE NUMBER {} NOT VALID'.format(number))
            elif format_type == 'out_of_country':
                # For out of country format we must get the Asterisk
                # agent country to format numbers according to it.
                country_code = self.env.user.partner_id._get_country_code()
                number = phonenumbers.format_out_of_country_calling_number(
                    phone_nbr, country_code)
                logger.debug(
                    'LEAD OUT OF COUNTRY FORMATTED NUMBER: %s', number)
            elif format_type == 'e164':
                number = phonenumbers.format_number(
                    phone_nbr, phonenumbers.PhoneNumberFormat.E164)
                logger.debug('LEAD E164 FORMATTED NUMBER: {}'.format(number))
            elif format_type == 'international':
                number = phonenumbers.format_number(
                    phone_nbr, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                logger.debug('LEAD INTERN FORMATTED NUMBER: {}'.format(number))
            else:
                logger.error('LEAD WRONG FORMATTING PASSED: %s', format_type)
        except phonenumberutil.NumberParseException:
            logger.debug('LEAD PHONE NUMBER {} PARSE ERROR'.format(number))
        except Exception:
            logger.exception('LEAD FORMAT NUMBER ERROR:')
        finally:
            return number
