import base64

import babel.dates
import collections
import datetime
from datetime import timedelta, MAXYEAR
from dateutil import rrule
from dateutil.relativedelta import relativedelta
import logging
from operator import itemgetter
import pytz
import re
import time
import uuid

from odoo import api, fields, models
from odoo import tools
from odoo.addons.base.models.res_partner import _tz_get
from odoo.osv import expression
from odoo.tools.translate import _
from odoo.tools.misc import get_lang
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, pycompat
from odoo.exceptions import UserError, ValidationError

VIRTUALID_DATETIME_FORMAT = "%Y%m%d%H%M%S"


def calendar_id2real_id(calendar_id=None, with_date=False):
    """ Convert a "virtual/recurring event id" (type string) into a real event id (type int).
        E.g. virtual/recurring event id is 4-20091201100000, so it will return 4.
        :param calendar_id: id of calendar
        :param with_date: if a value is passed to this param it will return dates based on value of withdate + calendar_id
        :return: real event id
    """
    if calendar_id and isinstance(calendar_id, str):
        res = [bit for bit in calendar_id.split('-') if bit]
        if len(res) == 2:
            real_id = res[0]
            if with_date:
                real_date = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT,
                                          time.strptime(res[1], VIRTUALID_DATETIME_FORMAT))
                start = datetime.datetime.strptime(real_date, DEFAULT_SERVER_DATETIME_FORMAT)
                end = start + timedelta(hours=with_date)
                return (int(real_id), real_date, end.strftime(DEFAULT_SERVER_DATETIME_FORMAT))
            return int(real_id)
    return calendar_id and int(calendar_id) or calendar_id

class Meeting(models.Model):
    _inherit = 'calendar.event'

    def read(self, fields=None, load='_classic_read'):

        if not fields:
            fields = list(self._fields)
        fields = list(fields)
        fields2 = fields and fields[:]
        EXTRAFIELDS = ('privacy', 'user_id', 'duration', 'allday', 'start', 'rrule')
        for f in EXTRAFIELDS:
            if fields and (f not in fields):
                fields2.append(f)

        select = [(x, calendar_id2real_id(x)) for x in self.ids]
        real_events = self.browse([real_id for calendar_id, real_id in select])
        real_data = super(Meeting, real_events).read(fields=fields2, load=load)
        real_data = dict((d['id'], d) for d in real_data)

        result = []
        for calendar_id, real_id in select:
            if not real_data.get(real_id):
                continue
            res = real_data[real_id].copy()
            ls = calendar_id2real_id(calendar_id, with_date=res and res.get('duration', 0) > 0 and res.get('duration') or 1)
            if not isinstance(ls, (str, int)) and len(ls) >= 2:
                res['start'] = ls[1]
                res['stop'] = ls[2]
                if 'display_time' in fields:
                    res['display_time'] = self._get_display_time(ls[1], ls[2], res['duration'], res['allday'])

            res['id'] = calendar_id
            result.append(res)

        recurrent_fields = self._get_recurrent_fields()
        public_fields = set \
            (recurrent_fields + ['id', 'active', 'allday', 'start', 'stop', 'display_start', 'display_stop', 'duration', 'user_id', 'state', 'interval', 'count', 'recurrent_id', 'recurrent_id_date', 'rrule'])
        for r in result:
            if r['user_id']:
                user_id = type(r['user_id']) in (tuple, list) and r['user_id'][0] or r['user_id']
                partner_id = self.env.user.partner_id.id
                if user_id == self.env.user.id or partner_id in r.get("partner_ids", []):
                    continue
            if r['privacy'] == 'private':
                for f in r:
                    if f not in public_fields:
                        if isinstance(r[f], list):
                            r[f] = []
                        else:
                            r[f] = False
                    if f in ['name', 'display_name']:
                        r[f] = _('Busy')

        for r in result:
            for k in EXTRAFIELDS:
                if (k in r) and (fields and (k not in fields)):
                    del r[k]
        return result