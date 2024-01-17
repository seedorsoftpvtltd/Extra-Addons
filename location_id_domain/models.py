from odoo import models, fields,api

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.model
    def _domain_location_dest_domain(self):
            stock_ware=self.env['stock.warehouse'].search([('company_id','=',self.env.company.id)])
            lot_id=stock_ware.lot_stock_id
            return [('usage', '=', 'internal'), '|', ('location_id', '=', stock_ware.lot_stock_id.id), ('id', '=', lot_id.id)]  # Apply a domain filter for incoming picking types


    location_dest_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
        domain=lambda self: self._domain_location_dest_domain(),
    )

class StockLocation(models.Model):
    _inherit = 'stock.location'

    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #     current_company_id = self.env.company.id
    #     args.append(('company_id', '=', current_company_id))
    #     return super(StockLocation, self).search(args, offset, limit, order, count)

    @api.model
    def _location_id_default(self):

            stock_ware = self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)])
            lot_id = stock_ware.lot_stock_id
            return lot_id

    location_id = fields.Many2one(
        'stock.location', 'Parent Location', index=True, ondelete='cascade', check_company=True,default = lambda self: self._location_id_default(),
        help="The parent location that includes this location. Example : The 'Dispatch Zone' is the 'Gate 1' parent location.")


    @api.onchange('usage')
    def onchange_usage(self):
       for rec in self:
           if rec.usage != 'internal':
               rec.location_id=''
           else:
               lot= self._location_id_default()
               rec.location_id=lot

