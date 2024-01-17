import datetime
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta


class warehouseCntcompany(models.Model):
    _inherit = 'res.company'

    cnt_asn = fields.Integer(string="ASN Count", compute='_cnt_asn')
    cnt_grn = fields.Integer(string="GRN Count", compute='_cnt_grn')
    cnt_del = fields.Integer(string="DELIVERY Count", compute='_cnt_del')
    cnt_stock = fields.Integer(string="STOCK Count")

    def _cnt_asn(self):
        for rec in self:
            asn = self.env['warehouse.order'].sudo().search_count([('company_id', '=', rec.id)])
            if asn:
                rec['cnt_asn'] = asn
            else:
                rec['cnt_asn'] = ''
            print(rec.cnt_asn, 'cnt_asn')

    def _cnt_grn(self):
        for rec in self:
            grn = self.env['stock.picking'].sudo().search_count(
                [('picking_type_code', '!=', 'incoming'), ('user_id', '=', rec.id)])
            if grn:
                rec['cnt_grn'] = grn
            else:
                rec['cnt_grn'] = ''
            print(rec.cnt_grn, 'cnt_grn')

    def _cnt_del(self):
        for rec in self:
            grn = self.env['stock.picking'].sudo().search_count(
                [('picking_type_code', '!=', 'outgoing'), ('user_id', '=', rec.id)])
            if grn:
                rec['cnt_del'] = grn
            else:
                rec['cnt_del'] = ''
            print(rec.cnt_del, 'cnt_del')


# class warehouseCntpartner(models.Model):
#     _inherit = 'res.partner'
#
#     cnt_asn = fields.Integer(string="ASN Count", compute='_cnt_asn')
#     cnt_grn = fields.Integer(string="GRN Count", compute='_cnt_grn')
#     cnt_del = fields.Integer(string="DELIVERY Count", compute='_cnt_del')
#     cnt_stock = fields.Integer(string="STOCK Count")
#
#     def _cnt_asn(self):
#         for rec in self:
#             asn = self.env['warehouse.order'].sudo().search_count([('partner_id', '=', rec.id)])
#             if asn:
#                 rec['cnt_asn'] = asn
#             else:
#                 rec['cnt_asn'] = ''
#             print(rec.cnt_asn, 'cnt_asn')
#
#     def _cnt_grn(self):
#         for rec in self:
#             grn = self.env['stock.picking'].sudo().search_count(
#                 [('picking_type_code', '!=', 'incoming'), ('partner_id', '=', rec.id)])
#             if grn:
#                 rec['cnt_grn'] = grn
#             else:
#                 rec['cnt_grn'] = ''
#             print(rec.cnt_grn, 'cnt_grn')
#
#     def _cnt_del(self):
#         for rec in self:
#             grn = self.env['stock.picking'].sudo().search_count(
#                 [('picking_type_code', '!=', 'outgoing'), ('partner_id', '=', rec.id)])
#             if grn:
#                 rec['cnt_del'] = grn
#             else:
#                 rec['cnt_del'] = ''
#             print(rec.cnt_del, 'cnt_del')



# class warehouseCntproduct(models.Model):
#     _inherit = 'product.product'
#
#     cnt_asn = fields.Integer(string="ASN Count", compute='_cnt_asn')
#     cnt_grn = fields.Integer(string="GRN Count", compute='_cnt_grn')
#     cnt_del = fields.Integer(string="DELIVERY Count", compute='_cnt_del')
#     cnt_stock = fields.Integer(string="STOCK Count")
#
#     def _cnt_asn(self):
#         for rec in self:
#             asn = self.env['warehouse.order.line'].sudo().search_count([('product_id', '=', rec.id)])
#             if asn:
#                 rec['cnt_asn'] = asn
#             else:
#                 rec['cnt_asn'] = ''
#             print(rec.cnt_asn, 'cnt_asn')
#
#     def _cnt_grn(self):
#         for rec in self:
#             grn = self.env['stock.picking'].sudo().search_count(
#                 [('picking_type_code', '!=', 'incoming'), ('product_id', '=', rec.id)])
#             if grn:
#                 rec['cnt_grn'] = grn
#             else:
#                 rec['cnt_grn'] = ''
#             print(rec.cnt_grn, 'cnt_grn')
#
#     def _cnt_del(self):
#         for rec in self:
#             grn = self.env['stock.picking'].sudo().search_count(
#                 [('picking_type_code', '!=', 'outgoing'), ('product_id', '=', rec.id)])
#             if grn:
#                 rec['cnt_del'] = grn
#             else:
#                 rec['cnt_del'] = ''
#             print(rec.cnt_del, 'cnt_del')

