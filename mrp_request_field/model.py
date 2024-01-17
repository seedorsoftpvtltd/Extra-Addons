from odoo import api, models, fields

class ManufacturingRequest(models.Model):
    _inherit = "mrp.production.request"      

    starting_power_unit = fields.Integer('Starting Power Unit')
    ending_power_unit = fields.Integer('Ending Power Unit')
    unit_price = fields.Float('Unit Price')
    total_costs = fields.Float(compute='_get_sum')
 
    
    @api.depends('starting_power_unit', 'ending_power_unit', 'unit_price')

    def _get_sum(self):

        for rec in self:

           rec.update({

                'total_costs': (rec.starting_power_unit-rec.ending_power_unit)*rec.unit_price,

            })

 
 
class ManufacturingWorkOrder(models.Model):
    _inherit = "mrp.workorder"      

    total_workers = fields.Integer('Total Number of Workers')
    