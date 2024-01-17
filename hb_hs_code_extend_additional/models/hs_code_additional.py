from odoo import api, fields, models, tools, osv, http, _


class HsCodeExt(models.Model):
    _inherit = "hs.code"

    # uom_id = fields.Many2one('uom.uom', string='UOM', store=True)
    # tax_id = fields.Many2many('account.tax', string='Taxes', strore=True)
    uom = fields.Selection([("m", "m"), ("cm", "cm"), ("inch", "inch")], default="cm", string="UOM", )
    productname = fields.Char(string='Name', store=True)
    x_length1 = fields.Float(string='Length', store=True)
    x_height1 = fields.Float(string='Height', store=True)
    x_width1 = fields.Float(string='Width', store=True)
    weight = fields.Float(string='Weight', store=True)
    x_vol = fields.Float(string='Volume', store=True)

    @api.depends("local_code")
    def _compute_hs_code(self):
        for this in self:
            this.hs_code = this.local_code

    @api.depends("local_code", "productname")
    def name_get(self):
        res = []
        for this in self:
            name = this.local_code
            if this.productname:
                name += " " + this.productname
            name = len(name) > 55 and name[:55] + "..." or name
            res.append((this.id, name))
        return res

    _sql_constraints = [
        (
            "local_code_company_uniq",
            "unique(local_code, company_id)",
            "This code already exists for this company !",
        )
    ]