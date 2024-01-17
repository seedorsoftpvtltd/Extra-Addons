#coding: utf-8

from odoo import  fields, models
from odoo.addons.http_routing.models.ir_http import slug


class knowsystem_article(models.Model):
    """
    Overwrite to add attribute required for documentation
    """
    _name = "knowsystem.article"
    _inherit = "knowsystem.article"

    def _compute_anchor_href(self):
        """
        Compute method for anchor_href
        """
        for article in self:
            article.anchor_href = slug(article)


    anchor_href = fields.Char(
        string="Acnhor",
        compute=_compute_anchor_href,
    )

    def _check_article_public(self):
        """
        Overwrite to make sure attachments in documentation builder works disregarding website settings

        Methods:
         * _check_website_options

        Returns:
         * True if no error registered
        """
        result = True
        if not self._context.get("docu_builder"):
            result = super(knowsystem_article, self)._check_article_public()
        return result
