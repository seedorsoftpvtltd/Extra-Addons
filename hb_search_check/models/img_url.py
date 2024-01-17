from odoo.http import request
from odoo import api, fields, models, tools, osv, http, _
import odoo.osv.osv


class searchheck(models.Model):
    _inherit = "res.company"

    def check(self):
        search_partner = self.env['res.partner'].search([])
        searchids = []
        searchcompanyids = []
        for part in search_partner:
            searchids.append(part.id)
            searchcompanyids.append(part.company_id)
        searchread_partnerids = self.env['res.partner'].search_read(fields=['id'])
        searchread_partnercomp =  self.env['res.partner'].search_read(fields=['company_id'])
        self['x_testtest'] = str(searchids) + str(searchcompanyids) + str(searchread_partnerids) + str(searchread_partnercomp)
        return searchids, searchcompanyids, searchread_partnerids, searchread_partnercomp


