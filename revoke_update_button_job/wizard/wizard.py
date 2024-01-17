from odoo import models, fields, api


class MyWizard(models.TransientModel):
    _name = 'my_wizard'

    # Define fields for the wizard


    # Define the action to be taken when the wizard is confirmed

    def action_confirm(self):
        # Perform some action when the wizard is confirmed
        active=self.env['freight.operation'].browse(self._context.get('active_ids',[]))

        inv_obj = self.env["account.move"]
        for operation in active:

              invs = inv_obj.search(
                  [
                      ("operation_id", "=", operation.id),
                      ("state", "in", ["draft", "cancel"]),
                      ("type", "=", "out_invoice"),
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
                  invs = inv_obj.search(
                      [
                          ("operation_id", "=", operation.id),
                          ("state", "in", ["draft", "cancel"]),
                          ("type", "=", "out_invoice"),
                          
                      ]
                  )
                  # if not line.invoice_id and not line.inv_line_id:
                  # we did the below code to update inv line id
                  # in service, other wise we can do that by
                  # creating common vals
                  #print("iiiiiiiiiiiiii")
                  for invs1 in invs:
                   invs1.write(
                      {
                          "invoice_line_ids": [
                              (
                                  0,
                                  0,
                                  {
                                      "move_id": invs1.id or False,
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

