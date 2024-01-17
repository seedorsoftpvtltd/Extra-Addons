from odoo import api, fields, models, _

class revoke_update(models.Model):
    _inherit='freight.operation'


    def action_update_invoice1(self):
        inv_obj = self.env["account.move"]
        for operation in self:
            for line in operation.service_ids:
                if line.revoke_invoice == True:
                    invs = inv_obj.search(
                        [
                            ("operation_id", "=", operation.id),
                            ("state", "in", ["draft", "cancel"]),
                            ("type", "in", ["out_invoice"]),
                        ]
                    )

                    for inv1 in invs:
                        for move_lines in inv1.invoice_line_ids:

                            if line == move_lines.service_id:
                                self.moveuninvlink(inv1,move_lines)


                                for invoices in inv1:
                                    # if not line.invoice_id and not line.inv_line_id:
                                        # we did the below code to update inv line id
                                        # in service, other wise we can do that by
                                        # creating common vals
                                        print("iiiiiiiiiiiiii")
                                        invoices.write(
                                            {
                                                "invoice_line_ids": [
                                                    (
                                                        0,
                                                        0,
                                                        {
                                                            "move_id": invoices.id or False,
                                                            "service_id": line.id or False,
                                                            # 'account_id': account_id.id or False,
                                                            "name": line.product_id
                                                                    and line.product_id.name
                                                                    or "",
                                                            "product_id": line.product_id
                                                                          and line.product_id.id
                                                                          or False,
                                                            "quantity": line.qty or 0.0,
                                                            "product_uom_id": line.uom_id
                                                                              and line.uom_id.id
                                                                              or False,
                                                            "price_unit": line.list_price or 0.0,
                                                            'tax_ids': [(6, 0, line.x_sale_tax.ids)] or [(6, 0, line.product_id.taxes_id.ids)],
                                                        },
                                                    )
                                                ]
                                            }
                                        )
                line['revoke_invoice'] = False

    def moveuninvlink(self, inv1,move_lines):
        for line in inv1.line_ids:

            if line == move_lines:

                line.with_context(check_move_validity=False).unlink()

        # for inv in inv1.invoice_line_ids:
        #     inv.unlink()

    # def update_multi_invoices(self):
    #     inv_obj = self.env["account.move"]
    #     for operation in self:
    #
    #             invs = inv_obj.search(
    #                 [
    #                     ("operation_id", "=", operation.id),
    #                     ("state", "in", ["draft", "cancel"]),
    #                     ("type", "in", ["out_invoice"]),
    #                 ]
    #             )
    #             print(invs)
    #             for inv1 in invs:
    #
    #                 for line in inv1.line_ids:
    #                     print(line.account_id.name)
    #                     line.with_context(check_move_validity=False).unlink()
    #
    #                 for inv_line in inv1.invoice_line_ids:
    #                     print(inv_line)
    #                     inv_line.unlink()
    #
    #             for line in operation.service_ids:
    #                 # if not line.invoice_id and not line.inv_line_id:
    #                 # we did the below code to update inv line id
    #                 # in service, other wise we can do that by
    #                 # creating common vals
    #                 print("iiiiiiiiiiiiii")
    #                 invs.write(
    #                     {
    #                         "invoice_line_ids": [
    #                             (
    #                                 0,
    #                                 0,
    #                                 {
    #                                     "move_id": invs.id or False,
    #                                     "service_id": line.id or False,
    #                                     # 'account_id': account_id.id or False,
    #                                     "name": line.product_id
    #                                             and line.product_id.name
    #                                             or "",
    #                                     "product_id": line.product_id
    #                                                   and line.product_id.id
    #                                                   or False,
    #                                     "quantity": line.qty or 0.0,
    #                                     "product_uom_id": line.uom_id
    #                                                       and line.uom_id.id
    #                                                       or False,
    #                                     "price_unit": line.list_price or 0.0,
    #                                     # 'service_id':line.id,
    #                                 },
    #                             )
    #                         ]
    #                     }
    #                 )
    def action_update_bill1(self):
        bill_obj = self.env["account.move"]
        # bill_line_obj = self.env['account.move.line']
        for operation in self:
            for line in operation.service_ids:
              if line.revoke_bill == True:
                invs = bill_obj.search(
                    [
                        ("operation_id", "=", operation.id),
                        ("state", "in", ["draft", "cancel"]),
                        ("type", "in", ["in_invoice"]),
                        ("partner_id", "=", line.vendor_id.id),
                    ]
                )


                for inv1 in invs:

                    for move_lines in inv1.invoice_line_ids:

                        if line == move_lines.service_id:
                            self.moveunlink(inv1)
                            for rr in inv1:

                                        rr.write(
                                            {
                                                "invoice_line_ids": [
                                                    (
                                                        0,
                                                        0,
                                                        {
                                                            "move_id": rr.id,
                                                            "service_id": line.id or False,
                                                            "product_id": line.product_id
                                                                          and line.product_id.id
                                                                          or False,
                                                            "name": line.product_id
                                                                    and line.product_id.name
                                                                    or "",
                                                            "quantity": line.qty or 1.0,
                                                            "product_uom_id": line.uom_id
                                                                              and line.uom_id.id
                                                                              or False,
                                                            "price_unit": line.cost_price or 0.0,
                                                            'tax_ids': [(6, 0, line.x_tax_ids.ids)] or [
                                                                (6, 0, line.product_id.taxes_id.ids)],
                                                        },
                                                    )
                                                ]
                                            }
                                        )
                                        ser_upd_vals = {
                                            "bill_id": rr.id,
                                        }
                                        if inv1.invoice_line_ids:
                                            bill_l_id = inv1.invoice_line_ids.search(
                                                [
                                                    ("service_id", "=", line.id),
                                                    ("id", "in", inv1.invoice_line_ids.ids),
                                                ],
                                                limit=1,
                                            )
                                            ser_upd_vals.update(
                                                {"bill_line_id": bill_l_id and bill_l_id.id or False}
                                            )
                                        line.write(ser_upd_vals)
              line['revoke_bill'] = False
    def moveunlink(self,inv1):

                for line in inv1.line_ids:

                    line.with_context(check_move_validity=False).unlink()


