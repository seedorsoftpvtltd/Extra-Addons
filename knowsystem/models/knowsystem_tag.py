# -*- coding: utf-8 -*-

from odoo import api, fields, models


class knowsystem_tag(models.Model):
    """
    The model to systemize article tags
    """
    _name = "knowsystem.tag"
    _inherit = ["knowsystem.node"]
    _description = "Tag"

    name = fields.Char(
        string="Tag title",
        required=True,
        translate=False,
    )
    description = fields.Html(
        string="Tag Description",
        translate=False,
    )
    apply_to_all = fields.Boolean(
        string="Apply to all Documents",
        help="""If checked this tag articles would be visible in all Seedor objects""",
    )
    filter_ids = fields.One2many(
        "knowsystem.filter",
        "tag_id",
        string="Applied to Documents",
    )
    parent_id = fields.Many2one(
        "knowsystem.tag",
        string="Parent Tag",
    )
    child_ids = fields.One2many(
        "knowsystem.tag",
        "parent_id",
        string="Child Tags"
    )
    color = fields.Integer(
        string='Color index',
        default=10,
    )
    article_ids = fields.Many2many(
        "knowsystem.article",
        "knowsystem_tag_know_system_article_r_table",
        "knowsystem_atricle_r_id",
        "knowsystem_tag_r_id",
        string="Articles",
    )

    _order = "sequence, id"

    def return_edit_form(self):
        """
        The method to return tag editing form
        """
        view_id = self.env.ref('knowsystem.knowsystem_tag_view_form').id
        return view_id

    @api.model
    def _return_tags_for_document(self, res_model, res_id):
        """
        The method to find all available tags for this document

        Args:
         * res_model - model name
         * res_id - id of document

        Methods:
         * _check_document of knowsystem.filter

        Returns:
         * knowsystem.tag recordset
        """
        filters = self.env["knowsystem.filter"].search([("model", "=", res_model)])
        if res_id:
            filters = filters.filtered(lambda filt: filt._check_document(res_id=res_id))
        filter_tags = filters.mapped("tag_id")
        global_tags = self.env["knowsystem.tag"].search([("apply_to_all", "=", True)])
        tags = filter_tags + global_tags
        return tags
