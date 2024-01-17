from odoo import api, fields, models, _

class revoke_update(models.Model):
    _inherit='freight.operation'

    def action_revoke(self):
        inv_obj = self.env["account.move"]
        for operation in self:
            # invs = inv_obj.search(
            #     [
            #         ("operation_id", "=", operation.id),
            #         ("state", "in", ["draft", "cancel"]),
            #     ]
            # )
            # invs.unlink()
            operation.write(
                {
                    "state": "draft",
                    "act_inv_payment": 0.0,
                    "act_bill_payment": 0.0,
                    "inv_amount_due": 0.0,
                    "bill_amount_due": 0.0,
                    "routes_ids": [],
                    "tracking_ids": [],
                    "service_ids": [],
                }
            )
            containers = operation.operation_line_ids.mapped("container_id")
            if containers:
                containers.write({"state": "available"})
            if operation.service_ids:
                operation.service_ids.write(
                    {
                        "invoice_id": False,
                        "inv_line_id": False,
                        "bill_id": False,
                        "bill_line_id": False,
                    }
                )


    def action_update_invoice(self):
        inv_obj = self.env["account.move"]
        for operation in self:
            if operation.invoice_count > 1:
                return {
                    'name': 'Update Invoice',
                    'type': 'ir.actions.act_window',
                    'res_model': 'my_wizard',
                    'view_id':self.env.ref('revoke_update_button_job.my_module_my_model_form_view').id,
                    'view_mode': 'form',
                    'target': 'new',
                }
            else:
                invs = inv_obj.search(
                    [
                        ("operation_id", "=", operation.id),
                        ("state", "in", ["draft", "cancel"]),
                        ("type", "in", ["out_invoice"]),
                    ]
                )
                print(invs)
                for inv1 in invs:
                    for line in inv1.line_ids:
                        print(line.account_id.name)
                        line.with_context(check_move_validity=False).unlink()

                    for inv_line in inv1.invoice_line_ids:
                        print(inv_line)
                        inv_line.unlink()
                for line in operation.service_ids:
                  for invs_line in invs:
                    # if not line.invoice_id and not line.inv_line_id:
                        # we did the below code to update inv line id
                        # in service, other wise we can do that by
                        # creating common vals
                        print("iiiiiiiiiiiiii")
                        invs_line.write(
                            {
                                "invoice_line_ids": [
                                    (
                                        0,
                                        0,
                                        {
                                            "move_id": invs_line.id or False,
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
                                            # 'service_id':line.id,
                                        },
                                    )
                                ]
                            }
                        )

    def update_multi_invoices(self):
        inv_obj = self.env["account.move"]
        for operation in self:

                invs = inv_obj.search(
                    [
                        ("operation_id", "=", operation.id),
                        ("state", "in", ["draft", "cancel"]),
                        ("type", "in", ["out_invoice"]),
                    ]
                )
                print(invs)
                for inv1 in invs:
                    for line in inv1.line_ids:
                        print(line.account_id.name)
                        line.with_context(check_move_validity=False).unlink()

                    for inv_line in inv1.invoice_line_ids:
                        print(inv_line)
                        inv_line.unlink()

                for line in operation.service_ids:
                    # if not line.invoice_id and not line.inv_line_id:
                    # we did the below code to update inv line id
                    # in service, other wise we can do that by
                    # creating common vals
                    print("iiiiiiiiiiiiii")
                    invs.write(
                        {
                            "invoice_line_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "move_id": invs.id or False,
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
                                        # 'service_id':line.id,
                                    },
                                )
                            ]
                        }
                    )
    def action_update_bill(self):
        bill_obj = self.env["account.move"]
        # bill_line_obj = self.env['account.move.line']
        for operation in self:
            for line in operation.service_ids:
                invs = bill_obj.search(
                    [
                        ("operation_id", "=", operation.id),
                        ("state", "in", ["draft", "cancel"]),
                        ("type", "in", ["in_invoice"]),
                        ("partner_id", "=", line.vendor_id.id),
                    ]
                )
                print(invs)
                for inv1 in invs:
                    for line in inv1.line_ids:
                        print(line.account_id.name)
                        line.with_context(check_move_validity=False).unlink()

                    for inv_line in inv1.invoice_line_ids:
                        print(inv_line)
                        print("tttttttttttttt")
                        inv_line.unlink()
            for line in operation.service_ids:
                    print("hiiii")
                    bill = bill_obj.search(
                        [
                            ("operation_id", "=", operation.id),
                            ("state", "in", ["draft", "cancel"]),
                            ("type", "in", ["in_invoice"]),
                            ("partner_id", "=", line.vendor_id.id),
                        ]


                    )

                    bill.write(
                        {
                            "invoice_line_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "move_id": bill.id,
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
                                    },
                                )
                            ]
                        }
                    )
                    ser_upd_vals = {
                        "bill_id": bill.id,
                    }
                    if bill.invoice_line_ids:
                        bill_l_id = bill.invoice_line_ids.search(
                            [
                                ("service_id", "=", line.id),
                                ("id", "in", bill.invoice_line_ids.ids),
                            ],
                            limit=1,
                        )
                        ser_upd_vals.update(
                            {"bill_line_id": bill_l_id and bill_l_id.id or False}
                        )
                    line.write(ser_upd_vals)
