from odoo import models, fields, api, _


class TypeofPackages(models.Model):
    _name = "ofd.type"
    _description = "ofd types"

    name = fields.Char(string="Types", store=True)



class FreightOrder(models.Model):
    _inherit = "operation.service"

    x_ofd_type = fields.Many2one("ofd.type", string='OFD', compute='_compute_main_service_id', store=True)

    @api.depends('main_service_id')
    def _compute_main_service_id(self):
        for rec in self:
            if rec.main_service_id:
                rec['x_ofd_type'] = rec.main_service_id.x_ofd_type
            elif rec.x_ofd_type:
                rec.x_ofd_type = rec.x_ofd_type
            else:
                rec['x_ofd_type'] = None


class saleOrder(models.Model):
    _inherit = "sale.order.line"

    x_ofd_type = fields.Many2one("ofd.type", string='OFD')


