from odoo import api, fields, models, _


class AttachmentInh(models.Model):
    _inherit = "ir.attachment"

    def publicattach(self):
        print(self.res_model)
        if self.res_model == 'hr.announcement':
            self.public = True

