from odoo import _, api, fields, models


class FleetOperations(models.Model):
    """Fleet Operations model."""

    _inherit = 'fleet.vehicle'

    state = fields.Selection([('new', 'New'),
                              ('inspection', 'Inspection'),
                              ('in_progress', 'In Service'),
                              ('contract', 'On Contract'),
                              ('rent', 'On Rent'), ('complete', 'Active'),
                              ('released', 'Released'),
                              ('write-off', 'Write-Off'),
                              ('custody', 'Custody')],
                             string='Vehicle State', default='new')


class FleetReturn(models.Model):
    _inherit = 'employee.fleet'

    @api.constrains('state', 'fleet')
    def inspection(self):
        for rec in self:
            if rec.state == 'return':
                for veh in rec.fleet:
                    veh.state = 'inspection'
            if rec.state == 'confirm':
                for veh in rec.fleet:
                    veh.state = 'custody'


class FleetVehicInh(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    @api.constrains('state')
    def inservice(self):
        for rec in self:
            if rec.state == 'draft':
                for ser in rec.vehicle_id:
                    ser.state = 'new'
            # if rec.state == 'confirm':
            #     for ser in rec.vehicle_id:
            #         ser.state = 'in_progress'
                # rec.state = 'in_progress'
            if rec.state == 'done':
                for ser in rec.vehicle_id:
                    ser.state = 'complete'
                # rec.state = 'complete'


# class FleetVh(models.Model):
#     _inherit = 'account.move'
#
#
#     def cgst(self):
#         for rec in self:
#                 print(x[3])
