from _datetime import datetime

from odoo import api, models, _
from odoo.exceptions import UserError


class ReportTax(models.AbstractModel):
    _inherit = 'report.base_accounting_kit.report_tax'

    @api.model
    def get_lines(self, options):
        taxes = {}
        for tax in self.env['account.tax'].search(
                [('type_tax_use', '!=', 'none')]):
            if tax.children_tax_ids:
                for child in tax.children_tax_ids:
                    if child.type_tax_use != 'none':
                        continue
                    taxes[child.id] = {'tax': 0, 'net': 0, 'name': child.name,
                                       'type': tax.type_tax_use}
            else:
                taxes[tax.id] = {'tax': 0, 'net': 0, 'name': tax.name,
                                 'type': tax.type_tax_use}
        if options['date_from'] and not options['date_to']:
            self.with_context(date_from=options['date_from'],
                              strict_range=True)._compute_from_amls(options,
                                                                    taxes)
        elif options['date_to'] and not options['date_from']:
            self.with_context(date_to=options['date_to'],
                              strict_range=True)._compute_from_amls(options,
                                                                    taxes)
        elif options['date_from'] and options['date_to']:
            self.with_context(date_from=options['date_from'],
                              date_to=options['date_to'],
                              strict_range=True)._compute_from_amls(options,
                                                                    taxes)
        else:
            date_to = str(datetime.today().date())
            self.with_context(date_to=date_to,
                              strict_range=True)._compute_from_amls(options,
                                                                    taxes)

        groups = dict((tp, []) for tp in ['sale', 'purchase'])
        for tax in taxes.values():
            if tax['tax'] or tax['net']:
                groups[tax['type']].append(tax)
        return groups
