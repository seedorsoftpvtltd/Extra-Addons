# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval

class TemplateSettingsInh(models.Model):
    """A model to store report template settings and styles to be applied on
    reports."""
    _inherit = "report.template.settings"
    _description = "Report Style Settings"

    @api.model
    def _default_so_template(self):
        def_tpl = self.env['ir.ui.view'].search(
            [('key', 'like', 'professional_templates.SO\_%\_document'),
             ('type', '=', 'qweb')],
            order='key asc',
            limit=1)
        return def_tpl or self.env.ref('sale.report_saleorder_document')

    @api.model
    def _default_po_template(self):
        def_tpl = self.env['ir.ui.view'].search(
            [('key', 'like', 'professional_templates.PO\_%\_document'),
             ('type', '=', 'qweb')],
            order='key asc',
            limit=1)
        return def_tpl or self.env.ref(
            'purchase.report_purchaseorder_document')

    @api.model
    def _default_rfq_template(self):
        def_tpl = self.env['ir.ui.view'].search(
            [('key', 'like', 'professional_templates.RFQ\_%\_document'),
             ('type', '=', 'qweb')],
            order='key asc',
            limit=1)
        return def_tpl or self.env.ref(
            'purchase.report_purchasequotation_document')

    @api.model
    def _default_dn_template(self):
        def_tpl = self.env['ir.ui.view'].search(
            [('key', 'like', 'professional_templates.DN\_%\_document'),
             ('type', '=', 'qweb')],
            order='key asc',
            limit=1)
        return def_tpl or self.env.ref('stock.report_delivery_document')

    @api.model
    def _default_pk_template(self):
        def_tpl = self.env['ir.ui.view'].search(
            [('key', 'like', 'professional_templates.PICK\_%\_document'),
             ('type', '=', 'qweb')],
            order='key asc',
            limit=1)
        return def_tpl or self.env.ref('stock.report_picking')

    @api.model
    def _default_inv_template(self):
        def_tpl = self.env['ir.ui.view'].search(
            [('key', 'like', 'professional_templates.INVOICE\_%\_document'),
             ('type', '=', 'qweb')],
            order='key asc',
            limit=1)
        return def_tpl or self.env.ref(
            'account.report_invoice_document_with_payments')

    template_inv = fields.Many2one(
        'ir.ui.view',
        'Invoice Template',
        default=_default_inv_template,
        domain=
        "[('type', '=', 'qweb'),'|',('key', 'like', 'professional_templates.INVOICE\_%\_document' ),('key', 'like', 'professional_templates_seedor.INVOICE\_%\_document' )]",
        required=False)
    template_so = fields.Many2one(
        'ir.ui.view',
        'Order/Quote Template',
        default=_default_so_template,
        domain=
        "[('type', '=', 'qweb'),'|',('key', 'like', 'professional_templates.SO\_%\_document' ),('key', 'like', 'professional_templates_seedor.SO\_%\_document' )]",
        required=False)

    template_po = fields.Many2one(
        'ir.ui.view',
        'Purchase Order Template',
        default=_default_po_template,
        domain=
        "[('type', '=', 'qweb'),'|', ('key', 'like', 'professional_templates.PO\_%\_document' ),('key', 'like', 'professional_templates_seedor.PO\_%\_document' )]",
        required=False)

    template_rfq = fields.Many2one(
        'ir.ui.view',
        'RFQ Template',
        default=_default_rfq_template,
        domain=
        "[('type', '=', 'qweb'),'|',('key', 'like', 'professional_templates.RFQ\_%\_document' ),('key', 'like', 'professional_templates_seedor.RFQ\_%\_document' )]",
        required=False)

    template_dn = fields.Many2one(
        'ir.ui.view',
        'Delivery Note Template',
        default=_default_dn_template,
        domain=
        "[('type', '=', 'qweb'),'|',('key', 'like', 'professional_templates.DN\_%\_document' ),('key', 'like', 'professional_templates_seedor.DN\_%\_document' )]",
        required=False)

    template_pk = fields.Many2one(
        'ir.ui.view',
        'Picking Slip Template',
        default=_default_pk_template,
        domain=
        "[('type', '=', 'qweb'),'|',('key', 'like', 'professional_templates.PICK\_%\_document' ),('key', 'like', 'professional_templates_seedor.PICK\_%\_document' )]",
        required=False)

