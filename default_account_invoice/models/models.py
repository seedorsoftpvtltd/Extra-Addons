from odoo import models, fields, api, _
import logging


_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit='account.move.line'


    def _get_computed_account(self):
        self.ensure_one()
        self = self.with_context(force_company=self.move_id.journal_id.company_id.id)

        if not self.product_id:
            return

        fiscal_position = self.move_id.fiscal_position_id
        accounts = self.product_id.product_tmpl_id.get_product_accounts(fiscal_pos=fiscal_position)
        if self.move_id.is_sale_document(include_receipts=True):

            _logger.info(accounts['income'], '--------------------------->>>>>>>>>>>>>accounts[income]')
            _logger.info(self.move_id.journal_id.default_debit_account_id.name, '--------------------------->>>>>>>>>>>>>self.journal_id.name')
            return accounts['income'] or self.move_id.journal_id.default_debit_account_id
        elif self.move_id.is_purchase_document(include_receipts=True):
            # In invoice.
            return accounts['expense'] or self.account_id