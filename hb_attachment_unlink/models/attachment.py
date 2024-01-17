import logging
import os

from odoo import api, models, fields, http, _
_logger = logging.getLogger(__name__)
from odoo.tools import config
import os


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def unlink(self):
        # Delete files from the filestore before deleting the attachments
        for attachment in self:
            if attachment.res_model == 'hr.attendance':
                if attachment.store_fname:
                    full_path = os.path.join(
                        self._filestore(), attachment.store_fname)
                    if os.path.exists(full_path):
                        os.remove(full_path)
        return super(IrAttachment, self).unlink()


