from odoo import api, fields, models, _
from odoo.exceptions import AccessError

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _description = 'Stock Picking'


#     # Restrict create and edit access for a particular group
#     @api.model
#     def create(self, vals):
#         if self.env.user.has_group('roles_srt.group_create_edit_access_rec'):
#             raise AccessError("You do not have permission to create record.")
#         return super(StockPicking, self).create(vals)
#
#     def write(self, vals):
#         if self.env.user.has_group('roles_srt.group_create_edit_access_rec'):
#             raise AccessError("You do not have permission to edit this record.")
#         return super(StockPicking, self).write(vals)
#
#
# class WarehouseOrder(models.Model):
#     _inherit = 'warehouse.order'
#     _description = 'Warehouse Order'
#
#
#     # Restrict create and edit access for a particular group
#     @api.model
#     def create(self, vals):
#         if self.env.user.has_group('roles_srt.group_create_edit_access_rec'):
#             raise AccessError("You do not have permission to create record.")
#         return super(WarehouseOrder, self).create(vals)
#
#     def write(self, vals):
#         if self.env.user.has_group('roles_srt.group_create_edit_access_rec'):
#             raise AccessError("You do not have permission to edit this record.")
#         return super(WarehouseOrder, self).write(vals)
#
# class GoodsIssueOrder(models.Model):
#     _inherit = 'goods.issue.order'
#     _description = 'Goods Issue Order'
#
#
#     # Restrict create and edit access for a particular group
#     @api.model
#     def create(self, vals):
#         if self.env.user.has_group('roles_srt.group_create_edit_access_rec'):
#             raise AccessError("You do not have permission to create record.")
#         return super(GoodsIssueOrder, self).create(vals)
#
#     def write(self, vals):
#         if self.env.user.has_group('roles_srt.group_create_edit_access_rec'):
#             raise AccessError("You do not have permission to edit this record.")
#         return super(GoodsIssueOrder, self).write(vals)

# class ProductTemplate(models.Model):
#     _inherit = 'product.template'
#     _description = 'Product Template'
#
#
#     # Restrict create and edit access for a particular group
#     @api.model
#     def create(self, vals):
#         if self.env.user.has_group('roles_srt.group_create_edit_access_rec'):
#             raise AccessError("You do not have permission to create record.")
#         return super(ProductTemplate, self).create(vals)
#
#     def write(self, vals):
#         if self.env.user.has_group('roles_srt.group_create_edit_access_rec'):
#             raise AccessError("You do not have permission to edit this record.")
#         return super(ProductTemplate, self).write(vals)

class Agreement(models.Model):
    _inherit = 'agreement'
    _description = 'Agreement'


    # Restrict create and edit access for a particular group
    @api.model
    def create(self, vals):
        if self.env.user.has_group('roles_srt.group_create_edit_access_agrecfs_rec') or self.env.user.has_group('roles_srt.group_create_edit_access_agre_rec'):
            raise AccessError("You do not have permission to create record.")
        return super(Agreement, self).create(vals)

    def write(self, vals):
        if self.env.user.has_group('roles_srt.group_create_edit_access_agrecfs_rec') or self.env.user.has_group('roles_srt.group_create_edit_access_agre_rec'):
            raise AccessError("You do not have permission to edit this record.")
        return super(Agreement, self).write(vals)

# class AccountMove(models.Model):
#     _inherit = 'account.move'
#     _description = 'Account Move'
#
#
#     # Restrict create and edit access for a particular group
#     @api.model
#     def create(self, vals):
#         if self.env.user.has_group('roles_srt.group_account_rec'):
#             raise AccessError("You do not have permission to create record.")
#         return super(AccountMove, self).create(vals)
#
#     def write(self, vals):
#         if self.env.user.has_group('roles_srt.group_account_rec'):
#             raise AccessError("You do not have permission to edit this record.")
#         return super(AccountMove, self).write(vals)
