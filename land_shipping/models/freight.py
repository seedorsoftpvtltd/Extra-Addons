from odoo import _, api, fields, models


class FreightOperationExtendd(models.Model):
    _inherit = "freight.operation"

    def land_select(self):
        return [("ftl", "FTL"), ("ltl", "LTL"), ("local_transport", "Local Transport"),
                ("local_services", "Local Services")]

    land_shipping = fields.Selection(land_select,
                                     string="Land Shipping",
                                     help="""FTL: Full Truckload.LTL: Less Then Truckload.""",
                                     )


class SOExtendd(models.Model):
    _inherit = "sale.order"

    def land_select(self):
        return [("ftl", "FTL"), ("ltl", "LTL"), ("local_transport", "Local Transport"),
                ("local_services", "Local Services")]

    fright_land_shipping = fields.Selection(
        land_select,
        string="Land Shipping",
        help="""FTL: Full Truckload.LTL: Less Then Truckload.""",
    )
