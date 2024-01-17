# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Order Line Sequence",
    "summary": "Propagates PO line sequence.",
    "version": "12.0.0",
    "author": "Kinsoft Indonesia, "
			  "Eficent, "
              "Serpent CS, "
              "Odoo Community Association (OCA), ",
    "category": "Purchase",
    "website": "kinsoft.id",
    "license": "AGPL-3",
    'data': [
        'views/purchase_view.xml',
        'views/report_purchaseorder.xml'
    ],
    "depends": [
        "purchase",
    ],
    'post_init_hook': 'post_init_hook',
    "installable": True,
}
