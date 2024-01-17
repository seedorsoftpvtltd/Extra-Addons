from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
import logging


_logger = logging.getLogger(__name__)

class UOM(models.Model):
    _inherit = "uom.uom"

    ratio=fields.Float(string='Base Unit Equivalent',default=1.0,digits=0)
    convertion=fields.Char(string='Unit Of Measure',store=True)

    @api.constrains('name')
    def _check_unique_name(self):
        for rec in self:

            uom_name = self.env['uom.uom'].search(
                [('name', '=', rec.name), ('id', '!=', rec.id),('category_id','=',rec.category_id.id)])
            if uom_name:
                raise ValidationError(_("Code '%s' already exists.") % rec.name)

    @api.onchange('ratio','name')
    def _onchange_ratio(self):
        if self.ratio:
            print("rrrrrrrr")
            if self.ratio == 1:

                self.uom_type='reference'
                self.factor_inv = 1.0
                self.factor = 1.0
            elif self.ratio > 1:

                self.uom_type='bigger'
                self.factor_inv = self.ratio
                categ = self.category_id.id
                ref_unit=self.env['uom.uom'].search(
                    [('category_id', '=',categ),('uom_type', '=','reference')])

                self.convertion = f"{self.name} * { self.factor_inv} = {ref_unit.name}"

            elif self.ratio < 1 and self.ratio > 0:
                self.uom_type = 'smaller'

                self.factor = self.ratio
                categ = self.category_id.id
                ref_unit = self.env['uom.uom'].search(
                    [('category_id', '=', categ), ('uom_type', '=', 'reference')])

                self.convertion = f"{self.name} * {self.factor} = {ref_unit.name}"

            elif self.ratio < 0:
                raise ValidationError (_("Base Unit Equivalent Should Be Greater Than 0"))


    @api.onchange('category_id')
    def _onchange_category_id(self):
            for rec in self:

                categ=rec.category_id.id
                uom_name = self.env['uom.uom'].search(
                    [('category_id', '=',categ)])

                if not uom_name:
                    self.uom_type = 'reference'
                    self.name=''
                    self.ratio=1.0



