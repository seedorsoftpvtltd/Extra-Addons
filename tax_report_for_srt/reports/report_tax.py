from _datetime import datetime
from odoo import api, models, _
from odoo.exceptions import UserError


class ReportTax(models.AbstractModel):
    _name = 'report.tax_report_for_srt.report_tax_srt'
    _description = 'Tax Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(
                _("Form content is missing, this report cannot be printed."))
        return {
            'data': data['form'],
            'income': self.get_lines_income(data.get('form')),
            'cost': self.get_lines_cost(data.get('form')),
            # 'others': self.get_lines_others(data.get('form')),
        }

    def _sql_from_amls_one(self):
        sql = """SELECT "account_move_line".tax_line_id, COALESCE(SUM("account_move_line".debit-"account_move_line".credit), 0)
                    FROM %s
                    WHERE %s AND "account_move_line".tax_exigible GROUP BY "account_move_line".tax_line_id"""
        return sql

    def _sql_from_amls_two(self):
        sql = """SELECT r.account_tax_id, COALESCE(SUM("account_move_line".debit-"account_move_line".credit), 0)
                 FROM %s
                 INNER JOIN account_move_line_account_tax_rel r ON ("account_move_line".id = r.account_move_line_id)
                 INNER JOIN account_tax t ON (r.account_tax_id = t.id)
                 WHERE %s AND "account_move_line".tax_exigible GROUP BY r.account_tax_id"""
        return sql

    def _compute_from_amls(self, options, taxes):
        # compute the tax amount
        sql = self._sql_from_amls_one()
        tables, where_clause, where_params = self.env[
            'account.move.line']._query_get()
        query = sql % (tables, where_clause)
        self.env.cr.execute(query, where_params)
        results = self.env.cr.fetchall()
        for result in results:
            if result[0] in taxes:
                taxes[result[0]]['tax'] = abs(result[1])

        # compute the net amount
        sql2 = self._sql_from_amls_two()
        query = sql2 % (tables, where_clause)
        self.env.cr.execute(query, where_params)
        results = self.env.cr.fetchall()
        for result in results:
            if result[0] in taxes:
                taxes[result[0]]['net'] = abs(result[1])

    def get_lines_income(self, options):
        if options['date_from'] and options['date_to']:
            date_from = (datetime.strptime(options['date_from'],'%Y-%m-%d')).date()
            date_to = (datetime.strptime(options['date_to'],'%Y-%m-%d')).date()
        else:
            date_from = options['date_from']
            date_to = options['date_to']
        if options['target_move'] == 'posted':
            if options['client_id'] and not options['coa_ids']:
                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('partner_id','in',options['client_id']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['out_invoice', 'out_refund'])
                                                             ])
            elif options['coa_ids'] and not options['client_id']:
                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['out_invoice', 'out_refund'])
                                                             ])
            elif options['coa_ids'] and options['client_id']:

                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('partner_id', 'in', options['client_id']),
                                                             ('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['out_invoice', 'out_refund'])
                                                             ])
            else:
                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['out_invoice', 'out_refund'])
                                                             ])


        else: # all entries
            if options['client_id'] and not options['coa_ids']:
                data = self.env['account.move.line'].search([('partner_id', 'in', options['client_id']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['out_invoice', 'out_refund'])
                                                             ])
            elif options['coa_ids'] and not options['client_id']:
                data = self.env['account.move.line'].search([('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['out_invoice', 'out_refund'])
                                                             ])
            elif options['coa_ids'] and options['client_id']:
                data = self.env['account.move.line'].search([('partner_id', 'in', options['client_id']),
                                                             ('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['out_invoice', 'out_refund'])
                                                             ])
            else:
                data = self.env['account.move.line'].search([('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['out_invoice', 'out_refund'])
                                                             ])

        move_values = data.read(
            ["id", "move_id", "account_id", "move_name", "product_id", "tax_line_id", "partner_id",
             "date", "credit", "debit", "tax_ids"])
        for i in range(0, len(move_values)):
            if move_values[i]["partner_id"]:
                move_values[i]["partner_id"] = move_values[i]["partner_id"][1]
            else:
                move_values[i]["partner_id"] = '-'
            move_values[i]["account_id"] = move_values[i]["account_id"][1]
        # initializing key
        op_key = 'move_name'

        # Unique Values of Key in Dictionary
        # Using loop + set()
        res = []
        for sub in move_values:
            res.append(sub[op_key])
        res = list(set(res))
        groups = dict((tp, []) for tp in res)
        for move in move_values:
            groups[move['move_name']].append(move)

        new_income = []
        for sub in groups:

            for a in groups[sub]:
                my_dict = {'date': '', 'move_name': '', 'client': '', 'taxes_account': '',
                           'sub_total': 0, 'taxes': 0, 'total': 0}
                if a['product_id'] and bool(a['tax_ids']):
                    my_dict['date'] = a['date']
                    my_dict['move_name'] = a['move_name']
                    my_dict['taxes_account'] = a['account_id']
                    my_dict['client'] = a['partner_id']
                    if a['credit']:
                        subtotal = a['credit']
                        taxe = self.env['account.tax'].browse(a['tax_ids'][0]).amount
                        tax = subtotal * (taxe / 100)
                        total = subtotal + tax
                        my_dict['sub_total'] = round(subtotal,3)
                        my_dict['taxes'] = round(tax, 3)
                        my_dict['total'] = round(total,3)
                    elif a['debit']:
                        subtotal = a['debit']
                        taxe = self.env['account.tax'].browse(a['tax_ids'][0]).amount
                        tax = subtotal * (taxe / 100)
                        total = subtotal + tax
                        my_dict['sub_total'] = round((-1 * subtotal),3)
                        my_dict['taxes'] = round((-1 * tax), 3)
                        my_dict['total'] = round((-1 * total),3)
                    new_income.append(my_dict)

        entry_receive = self.get_lines_receive(options)
        new_income.extend(entry_receive)
        cust = self.get_payment(options, 'customer')
        new_income.extend(cust)
        return new_income

    def get_lines_receive(self, options):
        if options['date_from'] and options['date_to']:
            date_from = (datetime.strptime(options['date_from'], '%Y-%m-%d')).date()
            date_to = (datetime.strptime(options['date_to'], '%Y-%m-%d')).date()
        else:
            date_from = options['date_from']
            date_to = options['date_to']
        if options['target_move'] == 'posted':
            if options['client_id'] and not options['coa_ids']:
                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('partner_id','in',options['client_id']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])
            elif options['coa_ids'] and not options['client_id']:
                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])
            elif options['coa_ids'] and options['client_id']:

                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('partner_id', 'in', options['client_id']),
                                                             ('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])
            else:
                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])


        else: # all entries
            if options['client_id'] and not options['coa_ids']:
                data = self.env['account.move.line'].search([('partner_id', 'in', options['client_id']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])
            elif options['coa_ids'] and not options['client_id']:
                data = self.env['account.move.line'].search([('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])
            elif options['coa_ids'] and options['client_id']:
                data = self.env['account.move.line'].search([('partner_id', 'in', options['client_id']),
                                                             ('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])
            else:
                data = self.env['account.move.line'].search([('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])
        record_receive = data.filtered(lambda r: r.move_id.move_type in ['receivable', 'receivable_refund'])

        if record_receive:
            move_receive = record_receive.read(
                ["id", "move_id", "account_id", "move_name", "tax_line_id", "partner_id",
                 "price_unit", "date", "balance", "tax_ids"])
            for i in range(0, len(move_receive)):
                if move_receive[i]["partner_id"]:
                    move_receive[i]["partner_id"] = move_receive[i]["partner_id"][1]
                else:
                    move_receive[i]["partner_id"] = '-'
                if move_receive[i]["account_id"]:
                    move_receive[i]["account_id"] = move_receive[i]["account_id"][1]

            # initializing key
            op_key = 'move_name'

            # Unique Values of Key in Dictionary
            # Using loop + set()
            res = []
            for sub in move_receive:
                res.append(sub[op_key])
            res = list(set(res))
            groups = dict((tp, []) for tp in res)
            for move in move_receive:
                groups[move['move_name']].append(move)
            new_other = []
            for sub in groups:

                for a in groups[sub]:
                    my_dict = {'date': '', 'move_name': '', 'client': '', 'taxes_account': '',
                               'sub_total': 0, 'taxes': 0, 'total': 0}
                    if a['tax_ids']:
                        tax = self.env['account.tax'].browse(a['tax_ids'][0]).amount
                        my_dict['date'] = a['date']
                        my_dict['move_name'] = a['move_name']
                        my_dict['client'] = a['partner_id']
                        my_dict['taxes_account'] = a['account_id']
                        if self.env['account.move'].browse(a['move_id'][0]).move_type == 'receivable_refund':
                            sub_total = a['balance']
                            taxe = sub_total * (tax / 100)
                            total = sub_total + taxe
                            my_dict['sub_total'] = round(a['balance'],3)
                            my_dict['taxes'] = round(taxe, 3)
                            my_dict['total'] = round(total,3)
                        else:
                            sub_total = abs(a['balance'])
                            taxe = sub_total * (tax / 100)
                            total = sub_total + taxe
                            my_dict['sub_total'] = round((abs(a['balance'])),3)
                            my_dict['taxes'] = round(taxe, 3)
                            my_dict['total'] = round(total,3)
                        new_other.append(my_dict)

        else:
            new_other = []
        return new_other

    def get_lines_cost(self, options):
        if options['date_from'] and options['date_to']:
            date_from = (datetime.strptime(options['date_from'], '%Y-%m-%d')).date()
            date_to = (datetime.strptime(options['date_to'], '%Y-%m-%d')).date()
        else:
            date_from = options['date_from']
            date_to = options['date_to']
        if options['target_move'] == 'posted':
            if options['client_id'] and not options['coa_ids']:
                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('partner_id','in',options['client_id']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['in_invoice', 'in_refund'])
                                                             ])
            elif options['coa_ids'] and not options['client_id']:
                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['in_invoice', 'in_refund'])
                                                             ])
            elif options['coa_ids'] and options['client_id']:

                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('partner_id', 'in', options['client_id']),
                                                             ('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['in_invoice', 'in_refund'])
                                                             ])
            else:
                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['in_invoice', 'in_refund'])
                                                             ])


        else: # all entries
            if options['client_id'] and not options['coa_ids']:
                data = self.env['account.move.line'].search([('partner_id', 'in', options['client_id']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['in_invoice', 'in_refund'])
                                                             ])
            elif options['coa_ids'] and not options['client_id']:
                data = self.env['account.move.line'].search([('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['in_invoice', 'in_refund'])
                                                             ])
            elif options['coa_ids'] and options['client_id']:
                data = self.env['account.move.line'].search([('partner_id', 'in', options['client_id']),
                                                             ('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['in_invoice', 'in_refund'])
                                                             ])
            else:
                data = self.env['account.move.line'].search([('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', 'in', ['in_invoice', 'in_refund'])
                                                             ])

        move_values = data.read(
            ["id", "move_id", "account_id", "move_name", "product_id", "tax_line_id",
             "partner_id", "date", "credit", 'debit', 'tax_ids'])
        for i in range(0, len(move_values)):
            if move_values[i]["partner_id"]:
                move_values[i]["partner_id"] = move_values[i]["partner_id"][1]
            else:
                move_values[i]["partner_id"] = '-'
            move_values[i]["account_id"] = move_values[i]["account_id"][1]
        # initializing key
        op_key = 'move_name'

        # Unique Values of Key in Dictionary
        # Using loop + set()
        res = []
        for sub in move_values:
            res.append(sub[op_key])
        res = list(set(res))
        groups = dict((tp, []) for tp in res)
        for move in move_values:
            groups[move['move_name']].append(move)
        new_cost = []
        for sub in groups:
            for a in groups[sub]:
                my_dict = {'date': '', 'move_name': '', 'client': '', 'taxes_account': '',
                           'sub_total': '', 'taxes': '', 'total': ''}
                if a['product_id'] and bool(a['tax_ids']):
                    my_dict['date'] = a['date']
                    my_dict['move_name'] = a['move_name']
                    my_dict['taxes_account'] = a['account_id']
                    my_dict['client'] = a['partner_id']
                    if a['credit']:
                        subtotal = round(a['credit'],3)
                        taxe = round((self.env['account.tax'].browse(a['tax_ids'][0]).amount), 3)
                        tax = subtotal * (taxe / 100)
                        total = round((subtotal + tax),3)
                        my_dict['sub_total'] = "(" + str(subtotal) + ")"
                        my_dict['taxes'] = "(" + str(tax) + ")"
                        my_dict['total'] = "(" + str(total) + ")"
                    elif a['debit']:
                        subtotal = round(a['debit'],3)
                        taxe = round((self.env['account.tax'].browse(a['tax_ids'][0]).amount), 3)
                        tax = subtotal * (taxe / 100)
                        total = round((subtotal + tax),3)
                        my_dict['sub_total'] = str(subtotal)
                        my_dict['taxes'] = str(tax)
                        my_dict['total'] = str(total)
                    new_cost.append(my_dict)
        entry_pay = self.get_lines_payable(options)
        new_cost.extend(entry_pay)
        supply = self.get_payment(options,'supplier')
        new_cost.extend(supply)
        return new_cost

    def get_lines_payable(self, options):
        if options['date_from'] and options['date_to']:
            date_from = (datetime.strptime(options['date_from'], '%Y-%m-%d')).date()
            date_to = (datetime.strptime(options['date_to'], '%Y-%m-%d')).date()
        else:
            date_from = options['date_from']
            date_to = options['date_to']
        if options['target_move'] == 'posted':
            if options['client_id'] and not options['coa_ids']:
                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('partner_id','in',options['client_id']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])
            elif options['coa_ids'] and not options['client_id']:
                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])
            elif options['coa_ids'] and options['client_id']:
                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('partner_id', 'in', options['client_id']),
                                                             ('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])
            else:
                data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])


        else: # all entries
            if options['client_id'] and not options['coa_ids']:
                data = self.env['account.move.line'].search([('partner_id', 'in', options['client_id']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])
            elif options['coa_ids'] and not options['client_id']:
                data = self.env['account.move.line'].search([('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])
            elif options['coa_ids'] and options['client_id']:
                data = self.env['account.move.line'].search([('partner_id', 'in', options['client_id']),
                                                             ('account_id', 'in', options['coa_ids']),
                                                             ('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])
            else:
                data = self.env['account.move.line'].search([('date', '>=', date_from),
                                                             ('date', '<=', date_to),
                                                             ('move_id.type', '=', 'entry')
                                                             ])

        record_payable = data.filtered(lambda r: r.move_id.move_type in ['payable', 'payable_refund'])
        if record_payable:
            move_receive = record_payable.read(
                ["id", "move_id", "account_id", "move_name", "tax_line_id", "partner_id",
                 "price_unit", "date", "balance", "tax_ids"])
            for i in range(0, len(move_receive)):
                if move_receive[i]["partner_id"]:
                    move_receive[i]["partner_id"] = move_receive[i]["partner_id"][1]
                else:
                    move_receive[i]["partner_id"] = '-'
                if move_receive[i]["account_id"]:
                    move_receive[i]["account_id"] = move_receive[i]["account_id"][1]

            # initializing key
            op_key = 'move_name'

            # Unique Values of Key in Dictionary
            # Using loop + set()
            res = []
            for sub in move_receive:
                res.append(sub[op_key])
            res = list(set(res))
            groups = dict((tp, []) for tp in res)
            for move in move_receive:
                groups[move['move_name']].append(move)
            new_other = []
            for sub in groups:

                for a in groups[sub]:
                    my_dict = {'date': '', 'move_name': '', 'client': '', 'taxes_account': '',
                               'sub_total': 0, 'taxes': 0, 'total': 0}
                    if a['tax_ids']:
                        tax = self.env['account.tax'].browse(a['tax_ids'][0]).amount
                        my_dict['date'] = a['date']
                        my_dict['move_name'] = a['move_name']
                        my_dict['client'] = a['partner_id']
                        my_dict['taxes_account'] = a['account_id']
                        if self.env['account.move'].browse(a['move_id'][0]).move_type == 'payable_refund':
                            sub_total = round((abs(a['balance'])),3)
                            taxe = round((sub_total * (tax / 100)), 3)
                            total = round((sub_total + taxe),3)
                            my_dict['sub_total'] = "(" + str(a['balance']) + ")"
                            my_dict['taxes'] = "(" + str(taxe) + ")"
                            my_dict['total'] = "(" + str(total) + ")"
                        else:
                            sub_total = round((abs(a['balance'])),3)
                            taxe = round((sub_total * (tax / 100)), 3)
                            total = round((sub_total + taxe),3)
                            my_dict['sub_total'] = str(a['balance'])
                            my_dict['taxes'] = str(taxe)
                            my_dict['total'] = str(total)

                        new_other.append(my_dict)
        else:
            new_other = []
        return new_other

    def get_payment(self,options,type):
        if options['date_from'] and options['date_to']:
            date_from = (datetime.strptime(options['date_from'], '%Y-%m-%d')).date()
            date_to = (datetime.strptime(options['date_to'], '%Y-%m-%d')).date()
        else:
            date_from = options['date_from']
            date_to = options['date_to']
        if options['target_move'] == 'posted':
            if options['client_id'] and not options['coa_ids']:
                data_pay = self.env['account.payment.linee'].search([('payment_id.state', '=', 'posted'),
                                                                     ('payment_id.partner_id', 'in', options['client_id']),
                                                                     ('payment_id.payment_date', '>=',
                                                                      date_from),
                                                                     ('payment_id.payment_date', '<=',
                                                                      date_to),
                                                                     ('payment_id.partner_type', '=', type)
                                                                     ])
            elif options['coa_ids'] and not options['client_id']:
                data_pay = self.env['account.payment.linee'].search([('payment_id.state', '=', 'posted'),
                                                                     ('account_id', 'in', options['coa_ids']),
                                                                     ('payment_id.payment_date', '>=',
                                                                      date_from),
                                                                     ('payment_id.payment_date', '<=',
                                                                      date_to),
                                                                     ('payment_id.partner_type', '=', type)
                                                                     ])
            elif options['coa_ids'] and options['client_id']:
                data_pay = self.env['account.payment.linee'].search([('payment_id.state', '=', 'posted'),
                                                                     ('payment_id.partner_id', 'in', options['client_id']),
                                                                     ('account_id', 'in', options['coa_ids']),
                                                                     ('payment_id.payment_date', '>=',
                                                                      date_from),
                                                                     ('payment_id.payment_date', '<=',
                                                                      date_to),
                                                                     ('payment_id.partner_type', '=', type)
                                                                     ])
            else:
                data_pay = self.env['account.payment.linee'].search([('payment_id.state', '=', 'posted'),
                                                                     ('payment_id.payment_date', '>=',
                                                                      date_from),
                                                                     ('payment_id.payment_date', '<=',
                                                                      date_to),
                                                                     ('payment_id.partner_type', '=', type)
                                                                     ])

        else: # all entries
            if options['client_id'] and not options['coa_ids']:
                data_pay = self.env['account.payment.linee'].search([('payment_id.partner_id', 'in', options['client_id']),
                                                                     ('payment_id.payment_date', '>=',
                                                                      date_from),
                                                                     ('payment_id.payment_date', '<=',
                                                                      date_to),
                                                                     ('payment_id.partner_type', '=', type)
                                                                     ])
            elif options['coa_ids'] and not options['client_id']:
                data_pay = self.env['account.payment.linee'].search([('account_id', 'in', options['coa_ids']),
                                                                     ('payment_id.payment_date', '>=',
                                                                      date_from),
                                                                     ('payment_id.payment_date', '<=',
                                                                      date_to),
                                                                     ('payment_id.partner_type', '=', type)
                                                                     ])
            elif options['coa_ids'] and options['client_id']:
                data_pay = self.env['account.payment.linee'].search([('payment_id.partner_id', 'in', options['client_id']),
                                                                     ('account_id', 'in', options['coa_ids']),
                                                                     ('payment_id.payment_date', '>=',
                                                                      date_from),
                                                                     ('payment_id.payment_date', '<=',
                                                                      date_to),
                                                                     ('payment_id.partner_type', '=', type)
                                                                     ])
            else:
                data_pay = self.env['account.payment.linee'].search([('payment_id.payment_date', '>=',
                                                                      date_from),
                                                                     ('payment_id.payment_date', '<=',
                                                                      date_to),
                                                                     ('payment_id.partner_type', '=', type)
                                                                     ])
        pay_values = data_pay.read(["id", "payment_id", "account_id","amount"])
        # initializing key
        op_key = 'payment_id'

        # Unique Values of Key in Dictionary
        # Using loop + set()
        res = []
        for sub in pay_values:
            res.append(sub[op_key])
        res = list(set(res))
        groups = dict((tp, []) for tp in res)
        for move in pay_values:
            groups[move['payment_id']].append(move)
        acc_pay  = self.env['account.payment']
        new_pay = []
        tax_contain_payment = []
        for sub in groups:
            for a in groups[sub]:
                istax = self.env['account.account'].browse(a['account_id'][0]).tax_flag
                if istax:
                    tax_contain_payment.append(sub)
        for sub in tax_contain_payment:
            my_dict = {'date': '', 'move_name': '', 'client': '', 'taxes_account': '',
                       'sub_total': 0,'taxes':0,'total': 0 }
            for a in groups[sub]:
                istax = self.env['account.account'].browse(a['account_id'][0]).tax_flag
                if not istax:
                    my_dict['date'] = acc_pay.browse(a["payment_id"][0]).payment_date
                    my_dict['move_name'] = acc_pay.browse(a["payment_id"][0]).name
                    my_dict['taxes_account'] = a['account_id'][1]
                    my_dict['client'] = acc_pay.browse(a["payment_id"][0]).partner_id.name
                    my_dict['sub_total'] = round(a['amount'],3)
                if istax:
                    my_dict['taxes'] = round((a["amount"]),3)
                    my_dict['total'] = round((my_dict['sub_total'] + my_dict['taxes']),3)
            new_pay.append(my_dict)
        # print(sadsd)
        return new_pay



