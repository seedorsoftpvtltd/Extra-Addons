# Copyright (C) 2011 Julius Network Solutions SARL <contact@julius.fr>
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Move Stock Location",
    "version": "13.0.1.2.0",
    "author": "Julius Network Solutions, Odoo Community Association (OCA)",
    "summary": "This module allows to move all stock "
    "in a stock location to an other one.",
    "website": "https://github.com/OCA/stock-logistics-warehouse",
    "license": "AGPL-3",
    "depends": ["stock"],
    "category": "Stock",
    "data": [
        "security/ir.model.access.csv",
        "data/stock_quant_view.xml",
        "views/stock_picking_type_views.xml",
        "wizard/stock_move_location.xml",

    ],
    "post_init_hook": "enable_multi_locations",
}
