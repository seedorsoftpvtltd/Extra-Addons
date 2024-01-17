from odoo import api, models, fields

class Document(models.Model):
    _name = 'document.attach'
    _rec_name = 'text4'
    text4 = fields.Char(string="Document Name")
    attachment_field = fields.Binary(string="Attachment")
    attachment1_field = fields.Binary(string="Attachment")
    attachment2_field = fields.Binary(string="Attachment")
    attachment3_field = fields.Binary(string="Attachment")
    text = fields.Text(string="Point to be Noted")
    text1 = fields.Char(string="Document Name")
    text2 = fields.Char(string="Document Name")
    text3 = fields.Char(string="Document Name")