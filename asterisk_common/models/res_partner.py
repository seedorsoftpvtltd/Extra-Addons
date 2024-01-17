import logging
import phonenumbers
from phonenumbers import phonenumberutil
from odoo import models, fields, api, tools, _

logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    phone_normalized = fields.Char(compute='_get_phone_normalized',
                                   index=True, store=True,
                                   string='E.164 phone')
    mobile_normalized = fields.Char(compute='_get_phone_normalized',
                                    index=True, store=True,
                                    string='E.164 mobile')
    phone_extension = fields.Char(help=_(
        'Prefix with # to add 1 second pause before entering. '
        'Every # adds 1 second pause. Example: ###1001'))

    @api.model
    def create(self, vals):
        res = super(Partner, self).create(vals)
        if res and not self.env.context.get('no_clear_cache'):
            self.clear_caches()
        return res

    def write(self, values):
        res = super(Partner, self).write(values)
        if res and not self.env.context.get('no_clear_cache'):
            self.clear_caches()
        return res

    def unlink(self):
        res = super(Partner, self).unlink()
        if res and not self.env.context.get('no_clear_cache'):
            self.clear_caches()
        return res

    @api.depends('phone', 'mobile', 'country_id')
    def _get_phone_normalized(self):
        for rec in self:
            if rec.phone:
                rec.phone_normalized = rec.normalize_phone(rec.phone)
            else:
                rec.phone_normalized = False
            if rec.mobile:
                rec.mobile_normalized = rec.normalize_phone(rec.mobile)
            else:
                rec.mobile_normalized = False

    @api.model
    def originate_extension(self, partner_id):
        partner = self.browse(partner_id)
        number = partner.phone
        extension = partner.phone_extension or ''
        # Minimum 1 second delay.
        dtmf_delay = extension.count('#') or 1
        # Now strip # and have only extension.
        dtmf_digits = extension.strip('#')
        self.env['asterisk_common.user'].originate_call(
            number, model='res.partner', res_id=partner.id,
            variables={'__dtmf_digits': dtmf_digits,
                       '__dtmf_delay': dtmf_delay})

    def _get_country_code(self):
        partner = self
        if partner and partner.country_id:
            # Return partner country code
            return partner.country_id.code
        elif partner and partner.parent_id and partner.parent_id.country_id:
            # Return partner's parent country code
            return partner.parent_id.country_id.code
        elif partner and partner.company_id and partner.company_id.country_id:
            # Return partner's company country code
            return partner.company_id.country_id.code
        elif self.env.user and self.env.user.company_id.country_id:
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
        # Strip the number if parse error.
        number = number.replace(' ', '')
        number = number.replace('(', '')
        number = number.replace(')', '')
        number = number.replace('-', '')
        return number

    @api.model
    def _format_number(self, number, country_code=None,
                       format_type='e164'):
        logger.debug('FORMAT_NUMBER %s COUNTRY %s FORMAT %s',
                     number, country_code, format_type)
        # Strip formatting if present
        number = number.replace(' ', '')
        number = number.replace('(', '')
        number = number.replace(')', '')
        number = number.replace('-', '')
        if len(self) == 1 and not country_code:
            # Called from partner object
            country_code = self._get_country_code()
            logger.debug(
                'GOT COUNTRY FOR PARTNER %s CODE %s', self, country_code)
        elif not country_code:
            # Get country code for requesting account
            country_code = self.env.user.partner_id._get_country_code()
            logger.debug('GOT COUNTRY CODE %s FROM ENV USER', country_code)
        elif not country_code:
            logger.debug('COULD NOT GET COUNTRY CODE')
        if country_code is False:
            # False -> None
            country_code = None
        try:
            phone_nbr = phonenumbers.parse(number, country_code)
            if not phonenumbers.is_possible_number(phone_nbr):
                logger.debug('PHONE NUMBER {} NOT POSSIBLE'.format(number))
            elif not phonenumbers.is_valid_number(phone_nbr):
                logger.debug('PHONE NUMBER {} NOT VALID'.format(number))
            # We have a parsed number, let check what format to return.
            elif format_type == 'out_of_country':
                # For out of country format we must get the Asterisk
                # agent country to format numbers according to it.
                country_code = self.env.user.partner_id._get_country_code()
                number = phonenumbers.format_out_of_country_calling_number(
                    phone_nbr, country_code)
                logger.debug(
                    'OUT OF COUNTRY FORMATTED NUMBER: %s', number)
            elif format_type == 'e164':
                number = phonenumbers.format_number(
                    phone_nbr, phonenumbers.PhoneNumberFormat.E164)
                logger.debug('E164 FORMATTED NUMBER: {}'.format(number))
            elif format_type == 'international':
                number = phonenumbers.format_number(
                    phone_nbr, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                logger.debug('INTERN FORMATTED NUMBER: {}'.format(number))
            else:
                logger.error('WRONG FORMATTING PASSED: %s', format_type)
        except phonenumberutil.NumberParseException:
            logger.debug('PHONE NUMBER {} PARSE ERROR'.format(number))
        except Exception:
            logger.exception('FORMAT NUMBER ERROR:')
        finally:
            return number

    def _search_partner_by_number(self, number):
        found = self.env['res.partner'].search([
            '|',
            ('phone_normalized', '=', number),
            ('mobile_normalized', '=', number)])
        logger.debug('SEARCH_PARTNER_BY_NUMBER %s FOUND: %s', number, found)
        parents = found.mapped('parent_id')
        # 1-st case: just one partner, perfect!
        if len(found) == 1:
            logger.debug('FOUND PARTNER BY NUMBER {}'.format(number))
            return found[0]
        # 2-nd case: Many partners, no parent company / many companies
        elif len(parents) == 0 and len(found) > 1:
            logger.warning('MANY PARTNERS FOR NUMBER %s', number)
            return
        # 3-rd case: many partners, many companies
        elif len(parents) > 1 and len(found) > 1:
            logger.warning(
                'MANY PARTNERS DIFFERENT COMPANIES FOR NUMBER %s', number)
            return
        # 4-rd case: 1 partner from one company
        elif len(parents) == 1 and len(found) == 2 and len(
                found.filtered(
                    lambda r: r.parent_id.id in [k.id for k in parents])) == 1:
            logger.debug('ONE PARTNER FROM ONE PARENT FOUND')
            return found.filtered(
                lambda r: r.parent_id.id in [k.id for k in parents])[0]
        # 5-rd case: many partners same parent company
        elif len(parents) == 1 and len(found) > 1 and len(found.filtered(
                lambda r: r.parent_id.id in [k.id for k in parents])) > 1:
            logger.debug(
                'MANY PARTNERS SAME PARENT COMPANY %s', number)
            return parents[0]
        # 6-rd case: Nothing found
        else:
            logger.debug('NO PARTNERS FOUND FOR NUMBER %s', number)

    @api.model
    @tools.ormcache('number', 'country_code')
    def get_partner_by_number(self, number, country_code=None):
        # Default values
        partner_info = {'name': _('Unknown'), 'id': False}
        logger.debug(
            'GET_PARTNER_BY_NUMBER {} COUNTRY {}'.format(number, country_code))
        if not number:
            logger.debug('NO NUMBER PASSED')
            return partner_info
        if 'unknown' in number or number == 's':
            logger.debug('<UNKNOWN>/s NUMBER PASSED')
            return partner_info
        partner = None
        # 1. Convert to E.164 and make a search
        e164_number = self._format_number(
            number, country_code=country_code, format_type='e164')
        partner = self._search_partner_by_number(e164_number)
        # 2. Make a search as as.
        if not partner:
            partner = self._search_partner_by_number(number)
        # 3. Add + and make a search.
        if not partner:
            number_plus = '+' + number if number[0] != '+' else number
            partner = self._search_partner_by_number(number_plus)
        if partner:
            # We have partner, populate result data.
            partner_info['id'] = partner.id
            if partner.parent_name:
                partner_info['name'] = u'{} ({})'.format(partner.name,
                                                         partner.parent_name)
            else:
                partner_info['name'] = partner.name
                # On Odoo 10 we have to use unicode formatting!
                logger.debug(u'FOUND PARTNER {}'.format(partner_info['name']))
        else:
            logger.debug('NO PARTNER FOUND')
        return partner_info
