from odoo import api, fields, models, _


class Picking(models.Model):
    _inherit = "stock.picking"

    incoterm_id = fields.Many2one('account.incoterms', string='Incoterm',
                                  help='International Commercial Terms are a series of predefined commercial terms used in international transactions.')

    @api.model
    def create(self, vals):
        res = super(Picking, self).create(vals)

        ware_id = self.env['warehouse.order'].search([('name','=',res.origin)])
        print(ware_id.incoterm_id)
        if ware_id.incoterm_id:
            print('adasd')
            res.update({'incoterm_id': ware_id.incoterm_id.id})
        return res