from odoo import models, fields


class TaxConfiguration(models.Model):
    _name = 'tax.configuration'

    _rec_name = 'tax'

    income_range = fields.Char('Tax Slab Description')
    tax = fields.Float('Tax %')
    range_from = fields.Float('Applied From')
    range_to = fields.Float('Applied To')
    active = fields.Boolean('Active', default=True)

    def name_get(self):
        # return [(rec.id, "%s - %s" % (rec.code, rec.name)) for rec in self]
        return [(rec.id, "{range} - ({tax})%".format(range=rec.income_range, tax=rec.tax)) for rec in self]
