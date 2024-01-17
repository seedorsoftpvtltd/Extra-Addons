from odoo import api, fields, models

class custom_clearance(models.Model):
    _inherit = "freight.operation"
    # rel=fields.Many2one('operation.custom',String='Relation')

    def custom_clear(self):
        res=self.env['operation.custom'].browse([])
        print(res)
        val=[]
        for rec in self:
            val.append((0, 0, {
                'product_id': rec.id,
                 'partner_id':rec.customer_id.id}))
        res.create({
            'operation_id':rec.id,
            'agent_id':rec.customer_id.id
        })