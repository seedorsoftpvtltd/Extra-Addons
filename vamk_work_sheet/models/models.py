# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta
from pytz import timezone
from odoo.exceptions import UserError, ValidationError

class MrpInh(models.Model):
    _inherit = 'mrp.production'

    wfm1_ou = fields.Float("WFM1 O.U",store=True)
    wfm1_cu = fields.Float("WFM1 C.U",store=True)
    wfm2_ou = fields.Float("WFM2 O.U",store=True)
    wfm2_cu = fields.Float("WFM2 C.U",store=True)
    power_ou = fields.Float("Power O.U",store=True)
    power_cu = fields.Float("Power C.U",store=True)

class WoInh(models.Model):
    _inherit = 'mrp.workorder'

    center_code = fields.Char("Work Center Code",related='workcenter_id.code',store=True)
#    activity_user_id = fields.Many2one('res.users',"Resposible",store=True)
    bottle_feeder = fields.Many2one('hr.employee',"Bottle Feeder",store=True)
    filler = fields.Many2one('hr.employee',"Filler",store=True)
    cap_feeder = fields.Many2one('hr.employee',"Cap Feeder",store=True)
    capper = fields.Many2one('hr.employee',"Capper",store=True)
    cool_feeder = fields.Many2one('hr.employee',"Cooling Tank Feeder",store=True)
    check_by = fields.Many2one('hr.employee',"Check By",store=True)
    dirt_bottle = fields.Integer('Dirt Bottles',store=True)
    insect_bottle = fields.Integer('Insect Bottles',store=True)
    damaged_bottle = fields.Integer('Damaged Bottles',store=True)
    total_b = fields.Integer('Total',compute="_get_bottle_check",store=True)
    number_crates = fields.Integer('Number of Crates',store=True)
    bottle_unpack = fields.Integer('Bottle Left Unpacked',store=True)
    lab_sample = fields.Integer('Lab Sample',store=True)
    labour_ids = fields.Many2many('hr.employee','labour_group_rel', 'labour_id1','labour_id2','Labours')

    @api.depends('dirt_bottle','insect_bottle','damaged_bottle')
    def _get_bottle_check(self):    
        for record in self:
            record['total_b'] = record.dirt_bottle + record.insect_bottle + record.damaged_bottle

class MrpLineInh(models.Model):
    _inherit = 'mrp.production.request'

    tea_time = fields.Float('Tea Time-1',store=True)
    tea_time2 = fields.Float('Tea Time-2',store=True)
    lunch_time = fields.Float('Lunch Time',store=True)

class ProductTemplateInh(models.Model):
    _inherit = 'product.template'

    is_material = fields.Boolean(string='Is Purchase Material')    

class MrpWorkReport(models.TransientModel):
    _name = 'mrp.wrkreport'
    _description = "Work Sheet Report Wizard"

    from_date = fields.Date('From Date', default=lambda self: fields.Date.to_string(date.today().replace(day=1)),required=True)
    to_date = fields.Date("To Date", default=lambda self: fields.Date.to_string((datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()), required=True)
    batch_no = fields.Many2one('mrp.production','Batch No')
    cr_date = fields.Date('Current Date', default=lambda self: fields.Date.to_string(date.today()))

    def print_report(self):
        if not self.batch_no:
           domain = [('state','=','done')]
           mrp_order = self.env['mrp.production'].search(domain).filtered(lambda fl: fl.date_planned_start.date() >= self.from_date and fl.date_planned_start.date() <= self.to_date)
        else:
           domain = [('state','=','done'),('id','=',self.batch_no.id)]
           mrp_order = self.env['mrp.production'].search(domain)
        datas = []

 #       mrp_order = self.env['mrp.production'].search(domain).filtered(lambda fl: fl.date_planned_start.date() >= self.from_date and fl.date_planned_start.date() <= self.to_date)
        if not mrp_order:
           raise UserError(_('No Records Found !!!'))
        for mrp in mrp_order:
            if not self.batch_no:
               date_from = datetime.combine(fields.Datetime.from_string(str(self.from_date)), time.min)
               date_to = datetime.combine(fields.Datetime.from_string(str(self.to_date)), time.max)          
            else:
               date_from = datetime.combine(fields.Datetime.from_string(str(self.cr_date)), time.min)
               date_to = datetime.combine(fields.Datetime.from_string(str(self.cr_date)), time.max)          
            vamk_lot = [str(lt.lot_id.name) for lt in mrp.finished_move_line_ids]
            datas.append({                    
                    'name':mrp.name,
                    'mrp_date':mrp.date_planned_start.date(),
                    'mrp_target': mrp.product_qty,
                    'mrp_lot': ''.join(vamk_lot),
                    'tea_time':mrp.mrp_production_request_id.tea_time,
                    'tea_time2':mrp.mrp_production_request_id.tea_time2,
                    'lunch_time':mrp.mrp_production_request_id.lunch_time,
                    'mrp_scrap':[{'product':scr.product_id.name,'qty':scr.scrap_qty,'uom':scr.product_uom_id.name} for scr in mrp.scrap_ids],
                    'mrp_achieve': mrp.qty_produced,
                    'wfm1_ou':mrp.wfm1_ou,
                    'wfm1_cu':mrp.wfm1_cu,
                    'wfm2_ou':mrp.wfm2_ou,
                    'wfm2_cu':mrp.wfm1_cu,
                    'power_ou':mrp.power_ou,
                    'power_cu':mrp.power_cu,
                    'materials':[{'product':mm.product_id.name,'is_material':mm.product_id.is_material,'quantity':mm.quantity_done,'product_uom':mm.product_uom.name} for mm in mrp.move_raw_ids],
                    'work_order':[{'code':recs.workcenter_id.code,'wr_start':recs.date_start.astimezone(timezone('Asia/Kolkata')),'wr_end':recs.date_finished.astimezone(timezone('Asia/Kolkata')),'respons':[lab.name for lab in recs.labour_ids],'time_ids':[dur.date_start.astimezone(timezone('Asia/Kolkata')) for dur in recs.time_ids]} for recs in mrp.workorder_ids],
                    'work_order2':[{'code':recs2.workcenter_id.code,'bottle_feeder':recs2.bottle_feeder.name,'filler':recs2.filler.name,'cap_feeder':recs2.cap_feeder.name,'capper':recs2.capper.name,'cool_feeder':recs2.cool_feeder.name} for recs2 in mrp.workorder_ids],
                    'bottle_check':[{'code':recs3.workcenter_id.code,'check_by':recs3.check_by.name,'dirt_bottle':recs3.dirt_bottle,'insect_bottle':recs3.insect_bottle,'damaged_bottle':recs3.damaged_bottle,'total_b':recs3.total_b} for recs3 in mrp.workorder_ids],
                    'packing':[{'code':recs4.workcenter_id.code,'number_crates':recs4.number_crates,'bottle_unpack':recs4.bottle_unpack,'lab_sample':recs4.lab_sample} for recs4 in mrp.workorder_ids]
                })
        res = {
            'mrp':datas,
            'start_date': self.from_date,
            'end_date': self.to_date,
        }
        data = {
            'form': res,
        }
        return self.env.ref('vamk_work_sheet.report_vamk_wrk_sheet').report_action([],data=data)
