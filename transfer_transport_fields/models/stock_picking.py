from odoo import fields, models, api

class Picking(models.Model):
    _inherit = "stock.picking"

    driver_id = fields.Char(string='Driver Id', store=True, )
    x_deliveryreceivedby = fields.Many2one('res.partner', string="Delivery Received By", store=True)
    x_driver1 = fields.Char(string="Driver Name", store=True)
    x_driver_number = fields.Char(string="Driver Phone Number", store=True)
    truck_in_date = fields.Date(string="Truck In Date", store=True)
    x_truck_out_date = fields.Date(string="Truck Out Date", store=True)
    x_deliverydate = fields.Date(string="Delivery Date", store=True)

    x_cargoreceivedby = fields.Many2one('res.partner', string="Cargo Received By", store=True)
    x_receiver_name = fields.Many2one('res.partner', string="Receiver Name", store=True)
    x_received_date = fields.Date(string="Received Date", store=True)
    x_sign = fields.Char(string="Sign & Seal", store=True)

    custom_officer_name = fields.Char(string='Custom Officer Name', store=True, )
    custom_officer_id = fields.Char(string='Custom Officer Id', store=True, )