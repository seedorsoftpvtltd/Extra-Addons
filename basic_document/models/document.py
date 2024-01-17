# Copyright 2018-2019 Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class Document(models.Model):
    _name = "doc.management"

    name = fields.Char('Name', required=True)
    current_user_id = fields.Many2one('res.users',string='Created by', default=lambda self: self.env.user, store=True,)
    doc_line_ids = fields.One2many('doc.management.line', 'doc_source_id', string='Files')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    custom_create_date = fields.Datetime(string='Create Date', readonly=True,
                                         default=lambda self: fields.Datetime.now())
    from_date = fields.Datetime(string="From Date")
    to_date = fields.Datetime(string="To Date")
    notes = fields.Text(string='Notes')

class DocLine(models.Model):
    _name = "doc.management.line"

    doc_source_id = fields.Many2one('doc.management', string="Doc")
    name = fields.Char("Name", required=True)
    file_doc = fields.Binary("File")
    file_name = fields.Char('File Name')
    details = fields.Char('Details')