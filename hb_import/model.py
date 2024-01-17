from odoo import api, models, fields, _
import xlsxwriter
from odoo.tools.misc import str2bool, xlsxwriter, file_open
import base64
from io import BytesIO
import xlwt
import logging

_logger = logging.getLogger(__name__)


class Importhb(models.Model):
    _inherit = 'stock.move.line'

    company_id = fields.Many2one('res.company', string='Company', readonly=False, required=True, index=True)


    @api.model
    def create(self, vals):

        res = super(Importhb, self).create(vals)
#        res.picking_id.action_confirm()
        active_ids = self.env.context.get('active_ids', [])
        print(active_ids)
        active_model = self.env.context.get('active_model')
        print(active_model)
        _logger.info("--------------------------------------------------------%s " % self.env.context)
        _logger.info("-------------------------res1-------------------------------%s " % res.picking_id)
        _logger.info("--------------------------------------------------------%s " % self.env.context.get('params'))
        if not res.picking_id:
            _logger.info("--------------------------self1------------------------------%s " % self.picking_id)
            print(res.picking_id.picking_type_id.code)
            if not res.picking_id.picking_type_id.code:
                if active_model == 'stock.move':
                    id = self.env[active_model].browse(active_ids)
                    res['move_id'] = id
                if active_model == 'stock.picking':
                    id = self.env[active_model].browse(active_ids)
                    res['picking_id'] = id

        _logger.info("-------------------res2-------------------------------------%s " % res.picking_id)
        # res['picking_id'] = res.picking_id.id
        _logger.info("-------------------state-------------------------------------%s " % res.picking_id.state)


        return res


class Importhbpick(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        print('+++++++++++++++++++++++++++++++++++++=picking create IMPORT +++++++++++++++++++++++++++++++++++++++++')
        res = super(Importhbpick, self).create(vals)
        moves = res.move_ids_without_package.search([('picking_id','=',res.id)])
        move_lines = res.move_line_ids_without_package.search([('move_id','=', False), ('picking_id','=',res.id)])
        _logger.info("-------------------picking create-----------moves--------------------------%s " % moves)
        _logger.info("-------------------picking create------------move_lines-------------------------%s " % move_lines)
        for mlines in move_lines:
            ml = moves.search([('product_id','=',mlines.product_id.id), ('location_id','=', mlines.location_id.id)])
            _logger.info("-------------------picking create-----ml--------------------------------%s " % ml)

            for m in ml:
                _logger.info("-------------------picking create-----mlines.llocation_id--------------------------------%s " % mlines.location_id)
                _logger.info("-------------------picking create-----ml.llocation_id--------------------------------%s " % ml.location_id)

                mlines['move_id'] = m.id
                _logger.info("-------------------picking create-----mlines['move_id']--------------------------------%s " % mlines.move_id)

        return res



# class Importhb(models.Model):
#     _inherit = 'stock.picking'
    # def hb(self):
#         return {
#             'name': 'Report',
#             'view_mode': 'form',
#             # 'res_id': result_id.id,
#             'binding_model':'stock.picking',
#             'res_model': 'exp.report',
#             'view_type': 'form',
#             'type': 'ir.actions.act_window',
#             'target': 'new',
#         }
#
#
# class EmpPayslipReport(models.TransientModel):
#     _name = "exp.report"
#
#     file = fields.Binary("Download File")
#     file_name = fields.Char(string="File Name")
#     file_type = fields.Selection([('pdf', 'PDF'), ('xls', 'XLS')
#                                   ], 'File Type', default="xls")
#
#
#     def imp(self):
#         print("hhhhhhhhhhhhhhhhhhhhh")
#         print(self.get_metadata()[0].get('xmlid'))
#         active_ids = self.env.context.get('active_ids', [])
#         hb = self.env['stock.picking'].browse(active_ids)
#
#         for hbb in hb:
#             row = 1
#             name_of_file = 'Export Report.xls'
#             file_path = 'Export Report' + '.xls'
#             workbook = xlsxwriter.Workbook('/tmp/' + file_path)
#             header_format = workbook.add_format(
#                 {'bold': True, 'valign': 'vcenter', 'font_size': 16, 'align': 'center'})
#             title_format = workbook.add_format(
#                 {'border': 1, 'bold': True, 'valign': 'vcenter', 'align': 'center', 'font_size': 14,
#                  'bg_color': '#D8D8D8'})
#             cell_wrap_format_bold = workbook.add_format(
#                 {'border': 1, 'bold': True, 'valign': 'vjustify', 'valign': 'vcenter', 'align': 'center',
#                  'font_size': 12})  ##E6E6E6
#             cell_wrap_format = workbook.add_format(
#                 {'border': 1, 'valign': 'vjustify', 'valign': 'vcenter', 'align': 'left', 'font_size': 12,
#                  'align': 'center', 'text_wrap': True})  ##E6E6E6
#
#             sub_cell_wrap_format_bold = workbook.add_format(
#                 {'border': 1, 'valign': 'vjustify', 'valign': 'vcenter', 'align': 'center',
#                  'font_size': 12, 'text_wrap': True})
#             worksheet = workbook.add_worksheet('Export Report')
#             worksheet.write(0, 0, 'External Id')
#             worksheet.write(0, 1, 'hb1')
#             worksheet.write(0, 2, 'hb2')
#             worksheet.write(0, 3, 'hb3')
#             worksheet.write(0, 4, 'hb4')
#             worksheet.write(0, 5, 'hb5')
#             worksheet.write(0, 6, 'hb6')
#             worksheet.write(0, 7, 'hb7')
#             worksheet.write(0, 8, 'hb8')
#             worksheet.write(0, 9, 'hb9')
#             for rec in hbb.move_line_ids_without_package:
#                 # row = 1
#                 col = 1
#                 ext = rec.get_metadata()[0].get('xmlid')
#                 worksheet.write(row, 0, ', '.join(rec.mapped(str(ext))))
#                 worksheet.write(row, 1, ', '.join(rec.mapped('product_id.name')))
#                 worksheet.write(row, 2, ', '.join(rec.mapped('result_package_id.name')))
#                 worksheet.write(row, 3, ', '.join(rec.mapped('product_id.name')))
#                 worksheet.write(row, 4, ', '.join(rec.mapped('product_id.name')))
#                 worksheet.write(row, 5, ', '.join(rec.mapped('product_id.name')))
#                 worksheet.write(row, 6, ', '.join(rec.mapped('product_id.name')))
#                 worksheet.write(row, 7, ', '.join(rec.mapped('product_id.name')))
#                 worksheet.write(row, 8, ', '.join(rec.mapped('product_id.name')))
#                 worksheet.write(row, 9, ', '.join(rec.mapped('product_id.name')))
#
#                 row += 1
#                 # worksheet.write(col, 0, ', '.join(rec.mapped('product_id.name')))
#                 # worksheet.write(col, 1, ', '.join(rec.mapped('product_id.name')))
#                 # worksheet.write(col, 2, ', '.join(rec.mapped('product_id.name')))
#                 # worksheet.write(col, 3, ', '.join(rec.mapped('product_id.name')))
#                 # worksheet.write(col, 4, ', '.join(rec.mapped('product_id.name')))
#                 # worksheet.write(col, 5, ', '.join(rec.mapped('product_id.name')))
#                 # worksheet.write(col, 6, ', '.join(rec.mapped('product_id.name')))
#                 # worksheet.write(col, 7, ', '.join(rec.mapped('product_id.name')))
#                 # worksheet.write(col, 8, ', '.join(rec.mapped('product_id.name')))
#                 # worksheet.write(col, 9, ', '.join(rec.mapped('product_id.name')))
#                 # list = [rec.id, rec.product_id, rec.id, rec.product_id]
#                 # for l in list:
#                 #     worksheet.write(row, col, l, cell_wrap_format)
#
#             workbook.close()
#             export_id = base64.b64encode(open('/tmp/' + file_path, 'rb+').read())
#             result_id = self.env['exp.report'].create({'file': export_id, 'file_name': name_of_file})
#             # file_data = BytesIO()
#             # workbook.save(file_data)
#             # self.write({
#             #     'data': base64.encodestring(file_data.getvalue()),
#             #     'file_name': 'Report - %s.xls',
#             #     'state': 'done'
#             # })
#             return {
#                 'name': 'Export Report',
#                 'view_mode': 'form',
#                 'res_id': result_id.id,
#                 'res_model': 'exp.report',
#                 'view_type': 'form',
#                 'type': 'ir.actions.act_window',
#                 'target': 'new',
#             }

