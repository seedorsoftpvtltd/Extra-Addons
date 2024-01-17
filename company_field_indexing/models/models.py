from odoo import models, fields, api


class ItemMaster(models.Model):
    _inherit = 'item.master'

    company_id = fields.Many2one('res.company', string='Company', readonly=True, index=True, default=lambda self: self.env.company)


class MultiContainer(models.Model):
    _inherit = "multiple.container"

    company_id = fields.Many2one('res.company', string='Company', readonly=True, index=True, default=lambda self: self.env.company)


class StockKeep(models.Model):
    _inherit = 'stock.keep'

    company_id = fields.Many2one('res.company', string='Company', readonly=True, index=True, default=lambda self: self.env.company)


class ContainerPattern(models.Model):
    _inherit = "container.pattern"

    company_id = fields.Many2one('res.company', string='Company', readonly=True, index=True, default=lambda self: self.env.company)


class PatternTemplate(models.Model):
    _inherit = "pattern.template"

    company_id = fields.Many2one('res.company', string='Company', readonly=True, index=True, default=lambda self: self.env.company)


class JobEstimateProduct(models.Model):
    _inherit = "job.estimate.product"

    company_id = fields.Many2one('res.company', string='Company', readonly=True, index=True, default=lambda self: self.env.company)


class WarehousePackages(models.Model):
    _inherit = "warehouse.packages"

    company_id = fields.Many2one('res.company', string='Company', readonly=True, index=True, default=lambda self: self.env.company)


class WarehouseTag(models.Model):
    _inherit = "warehouse.tag"

    company_id = fields.Many2one('res.company', string='Company', readonly=True, index=True, default=lambda self: self.env.company)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    company_id = fields.Many2one('res.company', string='Company', readonly=True, index=True, default=lambda self: self.env.company)



class SaleEstimateJob(models.Model):
    _inherit = "sale.estimate.job"

    company_id = fields.Many2one('res.company', required=True,  index=True, default=lambda self: self.env.company, string='Company')

class Agreement(models.Model):
    _inherit = "agreement"

    company_id = fields.Many2one(
        "res.company", string="Company", index=True, default=lambda self: self.env.company)

class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    company_id = fields.Many2one('res.company', string='Company', index=True, required=True, default=lambda self: self.env.company)


class servicechargeagree(models.Model):
    _inherit = "agreement.charges"


    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)

class StockRule(models.Model):

    _inherit = 'stock.rule'

    company_id = fields.Many2one('res.company', 'Company', index=True, default=lambda self: self.env.company)

class HSCode(models.Model):
    _inherit = "hs.code"

    company_id = fields.Many2one("res.company",string="Company",readonly=True,required=True, index=True, default=lambda self: self._default_company_id())

# class InventoryChecklistTemplate(models.Model):
#     _inherit = 'inventory.checklist.template'
#
#     company_id = fields.Many2one('res.company', string='Company', required=True,index=True,
#                                  copy=False, default=lambda self: self.env['res.company']._company_default_get())
#
# class ChecklistPoints(models.Model):
#     _inherit = 'checklist.points'
#
#     company_id = fields.Many2one('res.company', string='Company', required=True,index=True,
#         copy=False, default=lambda self: self.env['res.company']._company_default_get())
#
# class InventoryChecklist(models.Model):
#     _inherit = 'inventory.checklist'
#
#     company_id = fields.Many2one('res.company', string='Company', required=True,index=True,
#         copy=False, default=lambda self: self.env['res.company']._company_default_get())

# class CrmChecklistTemplate(models.Model):
#     _inherit = 'crm.checklist.template'
#
#     company_id = fields.Many2one('res.company', string='Company', required=True,index=True,
#         copy=False, default=lambda self: self.env['res.company']._company_default_get())
#
# class ChecklistPoints(models.Model):
#     _inherit = 'checklist.points'
#
#     company_id = fields.Many2one('res.company', string='Company', required=True,index=True,
#         copy=False, default=lambda self: self.env['res.company']._company_default_get())
#
# class CustomerChecklist(models.Model):
#     _inherit = 'crm.checklist'
#
#     company_id = fields.Many2one('res.company', string='Company', required=True,index=True,
#         copy=False, default=lambda self: self.env['res.company']._company_default_get())

# class DeliveryCarrier(models.Model):
#     _inherit = 'delivery.carrier'
#
#     company_id = fields.Many2one('res.company', string='Company', related='product_id.company_id', store=True,index=True,
#                                  readonly=False)

# class VisitorGatePass(models.Model):
#     _inherit = 'visitor.gate.pass.custom'
#
#     gate_company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.user.company_id,index=True,
#                                       string='Company', readonly=True)

class InvoiceApproval(models.Model):
    _inherit = 'invoice.approval'

    company_id=fields.Many2one('res.company',string='Company',index=True,default=lambda self: self.env.company)

class servicecharge(models.Model):

    _inherit = "service.charges"

    company_id = fields.Many2one('res.company', string='Company',index=True, default=lambda self: self.env.company.id)

class FreightOperation(models.Model):
    """Freight Operation Model."""

    _inherit = "freight.operation"

    company_id = fields.Many2one(
        "res.company", string="Company", index=True, default=lambda self: self.env.company
    )

    operator_id = fields.Many2one(
        "res.users", string="Operator", index=True, default=lambda self: self.env.user.id
    )

class AccountMove(models.Model):
    _inherit = "account.move"

    company_id = fields.Many2one(comodel_name='res.company', string='Company',store=True, readonly=True, index=True, compute='_compute_company_id')

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('approve', 'Approved'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled')
    ], string='Status', required=True, readonly=True, copy=False, tracking=True, index=True,
        default='draft')

    partner_id = fields.Many2one('res.partner', readonly=True, tracking=True,
        states={'draft': [('readonly', False)]}, index=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        string='Partner', change_default=True, ondelete="restrict")

class account_payment(models.Model):
    _inherit = "account.payment"

    company_id = fields.Many2one('res.company', related='journal_id.company_id', string='Company', readonly=True,
                                 store=True, index=True,)

    payment_type = fields.Selection(
        [('outbound', 'Send Money'), ('inbound', 'Receive Money'), ('transfer', 'Internal Transfer')],
        string='Payment Type', index=True, required=True, readonly=True, states={'draft': [('readonly', False)]})

    partner_id = fields.Many2one('res.partner', string='Partner', tracking=True, readonly=True, index=True, states={'draft': [('readonly', False)]}, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    company_id = fields.Many2one(related='move_id.company_id', store=True, index=True, readonly=True)

    display_type = fields.Selection([
        ('line_section', 'Section'),
        ('line_note', 'Note'),
    ], default=False, index=True, help="Technical field for UX purpose.")

class AccountAccount(models.Model):
    _inherit = "account.account"

    company_id = fields.Many2one('res.company', string='Company', index=True, required=True,
        default=lambda self: self.env.company)

class SubJob(models.Model):
    _inherit = 'sub.job'

    company_id = fields.Many2one('res.company', string='Company', required=True, index=True,
                                 default=lambda self: self.env.company)

class warehouseOrderLine(models.Model):
    _inherit = 'warehouse.order.line'

    company_id = fields.Many2one('res.company', related='order_id.company_id', string='Company', store=True,
                                 index=True, readonly=True)

class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    company_id = fields.Many2one(related='picking_id.company_id', store=True, index=True)

class AccountCashRounding(models.Model):

    _inherit = 'account.cash.rounding'

    company_id = fields.Many2one('res.company', related='account_id.company_id',store=True, index=True)


