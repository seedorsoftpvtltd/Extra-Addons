from datetime import datetime
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF


class SOLineExtendd(models.Model):
    _inherit = "sale.order.line"

    currency_id = fields.Many2one('res.currency', store=False, string="Currency")


class SOExtendd(models.Model):
    _inherit = "sale.order"

    # fright_transport = fields.Selection(
    #     [("land", "Land"), ("ocean", "Ocean"), ("air", "Air"), ("customs_clearance", "Customs Clearance"),
    #      ("cross_trade", "Cross Trade"), ("local_transport", "Local Transport"), ("local_services", "Local Services"),
    #      ("customs_brokerage", "Customs Brokerage"), ("contract_logistics", "Contract logistics")],
    #     default="land",
    #     string="Transport",
    # )

    fright_direction = fields.Selection(
        [("import", "Import"), ("export", "Export"), ("cross_trade", "Cross Trade"),
         ("local_services", "Local Services"), ("control_move", "Control Move"), ("local_move", "Local Move"),
         ("customs_brokerage", "Customs Brokerage"), ("contract_logistics", "Contract logistics"),('3pl', '3 PL'),
         ('rental', 'Rental'), ('value_added', 'Value Added Services'), ('cross_docking', 'Cross Docking')],
        string="Direction",
        default="import",
    )
    freight_air_shipping = fields.Selection(
        [("general", "General"), ("perishable", "Perishable"), ("temperature", "Temperature Control")],
        string="Air Shipping")

    fright_ocean_shipping = fields.Selection(
        [("fcl", "FCL"), ("lcl", "LCL"), ("bulk", "BULK")],
        string="Ocean Shipping",
        help="""FCL: Full Container Load.
                    LCL: Less Container Load.""",
    )
    fright_land_shipping = fields.Selection(
        [("ftl", "FTL"), ("ltc", "LTL"), ("local_transport", "Local Transport"), ("local_services", "Local Services") ],
        string="Land Shipping",
        help="""FTL: Full Truckload.LTL: Less Then Truckload.""",
    )


class FreightOperationExtendd(models.Model):
    _inherit = "freight.operation"

    # transport = fields.Selection(
    #     [("land", "Land"), ("ocean", "Ocean"), ("air", "Air"), ("customs_clearance", "Customs Clearance"),
    #      ("cross_trade", "Cross Trade"), ("local_transport", "Local Transport"), ("local_services", "Local Services"),
    #      ("customs_brokerage", "Customs Brokerage"), ("contract_logistics", "Contract logistics")],
    #     default="land",
    #     string="Transport",
    # )
    direction = fields.Selection(
        [("import", "Import"), ("export", "Export"), ("cross_trade", "Cross Trade"), ("local_services", "Local Services"),
         ("customs_brokerage", "Customs Brokerage"), ("contract_logistics", "Contract logistics"),('3pl', '3 PL'),
         ('rental', 'Rental'), ('value_added', 'Value Added Services'), ('cross_docking', 'Cross Docking')],
        string="Direction",
        default="import",
    )
    freight_air_shipping = fields.Selection(
        [("general", "General"), ("perishable", "Perishable"), ("temperature", "Temperature Control")],
        string="Air Shipping")
    ocean_shipping = fields.Selection(
        [("fcl", "FCL"), ("lcl", "LCL"), ("bulk", "BULK")],
        string="Ocean Shipping",
        help="""FCL: Full Container Load.
                LCL: Less Container Load.""",
    )
    land_shipping = fields.Selection(
        [("ftl", "FTL"), ("ltc", "LTL"), ("local_transport", "Local Transport"),("local_services", "Local Services")],
        string="Land Shipping",
        help="""FTL: Full Truckload.LTL: Less Then Truckload.""",
    )
