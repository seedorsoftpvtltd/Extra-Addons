from odoo import api, models, fields, _
import datetime


class customer_supplier_wizard(models.AbstractModel):
    _name = "report.customer_supplier_wizard.report_pdf"

    @api.model
    def _get_report_values(self, docids, data):

        start_date1 = data.get('start_date')
        end_date1 = data.get('end_date')
        if start_date1 and end_date1:
            start_date = datetime.datetime.strptime(start_date1, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date1, "%Y-%m-%d").date()
        else:
            start_date=False
            end_date=False
        debit = 0
        credit = 0
        invoice=[]
        credit_notes=[]
        journals=[]
        miscellaneous1=[]
        entry_total=[]
        entry_total1=[]
        entry_list=[]
        partner = data['context']['active_id']
        bill = self.env['account.move'].search([('type', 'in', ['out_invoice','in_invoice']), ('partner_id', '=', partner),('state','=','posted')])
        debit_note = self.env['account.move'].search([('type', 'in', ['out_refund','in_refund']), ('partner_id', '=', partner),('state','=','posted')])
        journal_entries = self.env['account.move'].search([('type', '=', 'entry'), ('partner_id', '=', partner),('state','=','posted')])
        miscellaneous = self.env['account.move'].search([('type', '=', 'entry'),('state','=','posted')])
        record = self.env['res.partner'].search([('id', '=', partner)])

        if not start_date and not end_date:
            for entry1 in miscellaneous:
                if not entry1.invoice_line_ids.payment_id:
                    for entry2 in entry1.line_ids.filtered(lambda recc: recc.partner_id.id == partner):
                        if entry2.account_id.user_type_id.type == 'receivable' or entry2.account_id.user_type_id.type == 'payable':
                            credit = credit + entry2.credit
                            debit = debit + entry2.debit
                            miscellaneous1.append(entry1)

            for bills in bill:
                if bills.line_ids:
                    for lines in bills.line_ids.filtered(lambda rec: rec.account_id.user_type_id.type == 'receivable' or rec.account_id.user_type_id.type == 'payable'):
                        credit = credit + lines.credit
                        debit = debit + lines.debit
                        invoice.append(bills)

            for debit_note in debit_note:
                if debit_note.line_ids:
                    for lines in debit_note.line_ids.filtered(
                            lambda rec: rec.account_id.user_type_id.type == 'receivable' or rec.account_id.user_type_id.type == 'payable'):
                        credit = credit + lines.credit
                        debit = debit + lines.debit
                        credit_notes.append(debit_note)

            for journal_entries in journal_entries:
                if journal_entries.line_ids:
                    for lines in journal_entries.line_ids.filtered(
                            lambda rec: rec.account_id.user_type_id.type == 'receivable' or rec.account_id.user_type_id.type == 'payable'):
                        credit = credit + lines.credit
                        debit = debit + lines.debit
                        journals.append(journal_entries)


        elif start_date and end_date:

            for entry1 in miscellaneous:
                if entry1.date >= start_date and entry1.date <= end_date:
                    if not entry1.invoice_line_ids.payment_id:
                        for entry2 in entry1.line_ids.filtered(lambda recc: recc.partner_id.id == partner):
                            if entry2.account_id.user_type_id.type == 'receivable' or entry2.account_id.user_type_id.type == 'payable':
                                credit = credit + entry2.credit
                                debit = debit + entry2.debit
                                miscellaneous1.append(entry1)

            for bills in bill:
                if bills.date >= start_date and bills.date <= end_date:
                    if bills.line_ids:
                        for lines in bills.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'receivable' or rec.account_id.user_type_id.type == 'payable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            invoice.append(bills)

            for debit_note in debit_note:
                if debit_note.date >= start_date and debit_note.date <= end_date:
                    if debit_note.line_ids:

                        for lines in debit_note.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'receivable' or rec.account_id.user_type_id.type == 'payable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            credit_notes.append(debit_note)

            for journal_entries in journal_entries:
                if journal_entries.date >= start_date and journal_entries.date <= end_date:
                    if journal_entries.line_ids:

                        for lines in journal_entries.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'receivable' or rec.account_id.user_type_id.type == 'payable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            journals.append(journal_entries)


        elif start_date:
            for entry1 in miscellaneous:
                if entry1.date >= start_date:
                    if not entry1.invoice_line_ids.payment_id:

                        for entry2 in entry1.line_ids.filtered(lambda recc: recc.partner_id.id == partner):

                            if entry2.account_id.user_type_id.type == 'receivable' or entry2.account_id.user_type_id.type == 'payable':
                                credit = credit + entry2.credit
                                debit = debit + entry2.debit
                                miscellaneous1.append(entry1)

            for bills in bill:
                if bills.date >= start_date:
                    if bills.line_ids:

                        for lines in bills.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'receivable' or rec.account_id.user_type_id.type == 'payable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            invoice.append(bills)

            for debit_note in debit_note:
                if debit_note.date >= start_date:
                    if debit_note.line_ids:

                        for lines in debit_note.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'receivable' or rec.account_id.user_type_id.type == 'payable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            credit_notes.append(debit_note)

            for journal_entries in journal_entries:
                if journal_entries.date >= start_date:
                    if journal_entries.line_ids:

                        for lines in journal_entries.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'receivable' or rec.account_id.user_type_id.type == 'payable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            journals.append(journal_entries)


        else:
            for entry1 in miscellaneous:
                if entry1.date <= end_date:
                    if not entry1.invoice_line_ids.payment_id:
                        for entry2 in entry1.line_ids.filtered(lambda recc: recc.partner_id.id == partner):
                            if entry2.account_id.user_type_id.type == 'receivable' or entry2.account_id.user_type_id.type == 'payable':
                                credit = credit + entry2.credit
                                debit = debit + entry2.debit
                                miscellaneous1.append(entry1)

            for bills in bill:
                if bills.date <= end_date:
                    if bills.line_ids:

                        for lines in bills.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'receivable' or rec.account_id.user_type_id.type == 'payable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            invoice.append(bills)

            for debit_note in debit_note:
                if debit_note.date <= end_date:
                    if debit_note.line_ids:

                        for lines in debit_note.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'receivable' or rec.account_id.user_type_id.type == 'payable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            credit_notes.append(debit_note)

            for journal_entries in journal_entries:
                if journal_entries.date <= end_date:
                    if journal_entries.line_ids:

                        for lines in journal_entries.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'receivable' or rec.account_id.user_type_id.type == 'payable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            journals.append(journal_entries)


        balance = debit - credit
        entry_total=miscellaneous1+invoice
        entry_total1=credit_notes+journals
        entry_list=entry_total+entry_total1
        list_set = set(entry_list)
        sorted_entry1 = (list(list_set))
        sorted_entry = sorted(sorted_entry1, key=lambda r: r.date)




        return {
            'ending_balance': balance,
            'record': record,
            'start_date': start_date,
            'end_date': end_date,
            'invoice':invoice,
            'credit_note':credit_notes,
            'payment':journals,
            'miscellaneous1':miscellaneous1,
            'entry': sorted_entry,
        }




class supplier_wizard(models.AbstractModel):
    _name = "report.customer_supplier_wizard.supplier_report_pdf"

    @api.model
    def _get_report_values(self, docids, data):

        start_date1 = data.get('start_date')
        end_date1 = data.get('end_date')
        if start_date1 and end_date1:
            start_date = datetime.datetime.strptime(start_date1, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date1, "%Y-%m-%d").date()
        else:
            start_date=False
            end_date=False
        debit = 0
        credit = 0
        miscellaneous2=[]
        vendor_bills=[]
        debit_note1=[]
        journal1=[]
        bill_total=[]
        bill_total1=[]
        bill_list=[]

        partner = data['context']['active_id']
        bill = self.env['account.move'].search([('type', '=', 'in_invoice'), ('partner_id', '=', partner),('state','=','posted')])
        debit_note = self.env['account.move'].search([('type', '=', 'in_refund'), ('partner_id', '=', partner),('state','=','posted')])
        journal_entries = self.env['account.move'].search([('type', '=', 'entry'), ('partner_id', '=', partner),('state','=','posted')])
        miscellaneous = self.env['account.move'].search([('type', '=', 'entry'),('state','=','posted')])
        record = self.env['res.partner'].search([('id', '=', partner)])
        if not start_date and not end_date:
            for entry1 in miscellaneous:
                if not entry1.invoice_line_ids.payment_id:
                    for entry2 in entry1.line_ids.filtered(lambda recc: recc.partner_id.id == partner):
                        if entry2.account_id.user_type_id.type == 'payable' or entry2.account_id.user_type_id.type == 'receivable':
                            credit = credit + entry2.credit
                            debit = debit + entry2.debit
                            miscellaneous2.append(entry1)

            for bills in bill:
                if bills.line_ids:
                    for lines in bills.line_ids.filtered(lambda rec: rec.account_id.user_type_id.type == 'payable' or rec.account_id.user_type_id.type == 'receivable'):
                        credit = credit + lines.credit
                        debit = debit + lines.debit
                        vendor_bills.append(bills)
            for debit_note in debit_note:
                if debit_note.line_ids:
                    for lines in debit_note.line_ids.filtered(
                            lambda rec: rec.account_id.user_type_id.type == 'payable' or rec.account_id.user_type_id.type == 'receivable'):
                        credit = credit + lines.credit
                        debit = debit + lines.debit
                        debit_note1.append(debit_note)
            for journal_entries in journal_entries:
                if journal_entries.line_ids:
                    for lines in journal_entries.line_ids.filtered(
                            lambda rec: rec.account_id.user_type_id.type == 'payable' or rec.account_id.user_type_id.type == 'receivable'):
                        credit = credit + lines.credit
                        debit = debit + lines.debit
                        journal1.append(journal_entries)

        elif start_date and end_date:

            for entry1 in miscellaneous:
                if entry1.date >= start_date and entry1.date <= end_date:
                    if not entry1.invoice_line_ids.payment_id:
                        for entry2 in entry1.line_ids.filtered(lambda recc: recc.partner_id.id == partner):
                            if entry2.account_id.user_type_id.type == 'payable' or entry2.account_id.user_type_id.type == 'receivable':
                                credit = credit + entry2.credit
                                debit = debit + entry2.debit
                                miscellaneous2.append(entry1)
            for bills in bill:
                if bills.date >= start_date and bills.date <= end_date:
                    if bills.line_ids:
                        for lines in bills.line_ids.filtered(lambda rec: rec.account_id.user_type_id.type == 'payable' or rec.account_id.user_type_id.type == 'receivable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            vendor_bills.append(bills)
            for debit_note in debit_note:
                if debit_note.date >= start_date and debit_note.date <= end_date:
                    if debit_note.line_ids:

                        for lines in debit_note.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'payable' or rec.account_id.user_type_id.type == 'receivable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            debit_note1.append(debit_note)
            for journal_entries in journal_entries:
                if journal_entries.date >= start_date and journal_entries.date <= end_date:
                    if journal_entries.line_ids:

                        for lines in journal_entries.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'payable' or rec.account_id.user_type_id.type == 'receivable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            journal1.append(journal_entries)

        elif start_date:
            for entry1 in miscellaneous:
                if entry1.date >= start_date:
                    if not entry1.invoice_line_ids.payment_id:

                        for entry2 in entry1.line_ids.filtered(lambda recc: recc.partner_id.id == partner):

                            if entry2.account_id.user_type_id.type == 'payable' or entry2.account_id.user_type_id.type == 'receivable':
                                credit = credit + entry2.credit
                                debit = debit + entry2.debit
                                miscellaneous2.append(entry1)
            for bills in bill:
                if bills.date >= start_date:
                    if bills.line_ids:

                        for lines in bills.line_ids.filtered(lambda rec: rec.account_id.user_type_id.type == 'payable' or rec.account_id.user_type_id.type == 'receivable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            vendor_bills.append(bills)
            for debit_note in debit_note:
                if debit_note.date >= start_date:
                    if debit_note.line_ids:

                        for lines in debit_note.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'payable' or rec.account_id.user_type_id.type == 'receivable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            debit_note1.append(debit_note)
            for journal_entries in journal_entries:
                if journal_entries.date >= start_date:
                    if journal_entries.line_ids:

                        for lines in journal_entries.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'payable' or rec.account_id.user_type_id.type == 'receivable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            journal1.append(journal_entries)

        else:
            for entry1 in miscellaneous:
                if entry1.date <= end_date:
                    if not entry1.invoice_line_ids.payment_id:
                        for entry2 in entry1.line_ids.filtered(lambda recc: recc.partner_id.id == partner):
                            if entry2.account_id.user_type_id.type == 'payable' or entry2.account_id.user_type_id.type == 'receivable':
                                credit = credit + entry2.credit
                                debit = debit + entry2.debit
                                miscellaneous2.append(entry1)
            for bills in bill:
                if bills.date <= end_date:
                    if bills.line_ids:

                        for lines in bills.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'payable' or rec.account_id.user_type_id.type == 'receivable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            vendor_bills.append(bills)
            for debit_note in debit_note:
                if debit_note.date <= end_date:
                    if debit_note.line_ids:

                        for lines in debit_note.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'payable' or rec.account_id.user_type_id.type == 'receivable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            debit_note1.append(debit_note)
            for journal_entries in journal_entries:
                if journal_entries.date <= end_date:
                    if journal_entries.line_ids:

                        for lines in journal_entries.line_ids.filtered(
                                lambda rec: rec.account_id.user_type_id.type == 'payable' or rec.account_id.user_type_id.type == 'receivable'):
                            credit = credit + lines.credit
                            debit = debit + lines.debit
                            journal1.append(journal_entries)

        balance = debit - credit
        bill_total=miscellaneous2+vendor_bills
        bill_total1=debit_note1+journal1
        bill_list=bill_total+bill_total1

        sorted_bill = sorted(bill_list, key=lambda r: r.date)

        return {
            'ending_balance': balance,
            'record': record,
            'start_date':start_date,
            'end_date': end_date,
            'vendor_bills':vendor_bills,
            'debit_note1':debit_note1,
            'payment1':journal1,
            'miscellaneous2':miscellaneous2,
            'entry':sorted_bill


        }

