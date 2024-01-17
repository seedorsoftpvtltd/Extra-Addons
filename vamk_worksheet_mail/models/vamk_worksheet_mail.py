# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta
from pytz import timezone
from odoo.http import request
from odoo.exceptions import UserError, ValidationError
import base64

class MRPWorkSheetInh(models.Model):
    _inherit = 'res.company'

    worksheet_mail = fields.Char('Worksheet Mail',store=True)

    def print_report(self):
        domain = [('state','=','done')]
        datas = []

        vamk_date = datetime.now().date()
        mrp_order = self.env['mrp.production'].search(domain).filtered(lambda fl: fl.date_planned_finished.date() == vamk_date)
        if not mrp_order:
           return
        fmt = "%Y-%m-%d %H:%M:%S"
        for mrp in mrp_order:
            date_from = datetime.combine(fields.Datetime.from_string(str(vamk_date)), time.min)
            date_to = datetime.combine(fields.Datetime.from_string(str(vamk_date)), time.max)          
            datas.append({                    
                    'name':mrp.name,
                    'mrp_date':mrp.date_planned_start.date(),
                    'mrp_target': mrp.product_qty,
                    'mrp_achieve': mrp.qty_produced,
                    'wfm1_ou':mrp.wfm1_ou,
                    'wfm1_cu':mrp.wfm1_cu,
                    'wfm2_ou':mrp.wfm2_ou,
                    'wfm2_cu':mrp.wfm1_cu,
                    'power_ou':mrp.power_ou,
                    'power_cu':mrp.power_cu,
                    'materials':[{'product':mm.product_id.name,'is_material':mm.product_id.is_material,'quantity':mm.quantity_done,'product_uom':mm.product_uom.name} for mm in mrp.move_raw_ids],
                    'work_order':[{'code':recs.workcenter_id.code,'wr_start':recs.date_start.astimezone(timezone('Asia/Kolkata')).strftime(fmt),'wr_end':recs.date_finished.astimezone(timezone('Asia/Kolkata')).strftime(fmt),'respons':recs.activity_user_id.name,'time_ids':[dur.date_start.astimezone(timezone('Asia/Kolkata')).strftime(fmt) for dur in recs.time_ids]} for recs in mrp.workorder_ids],
                    'work_order2':[{'code':recs2.workcenter_id.code,'bottle_feeder':recs2.bottle_feeder.name,'filler':recs2.filler.name,'cap_feeder':recs2.cap_feeder.name,'capper':recs2.capper.name,'cool_feeder':recs2.cool_feeder.name} for recs2 in mrp.workorder_ids],
                    'bottle_check':[{'code':recs3.workcenter_id.code,'check_by':recs3.check_by.name,'dirt_bottle':recs3.dirt_bottle,'insect_bottle':recs3.insect_bottle,'damaged_bottle':recs3.damaged_bottle,'total_b':recs3.total_b} for recs3 in mrp.workorder_ids],
                    'packing':[{'code':recs4.workcenter_id.code,'number_crates':recs4.number_crates,'bottle_unpack':recs4.bottle_unpack,'lab_sample':recs4.lab_sample} for recs4 in mrp.workorder_ids]
                })
        res = {
            'mrp':datas,
            'start_date': vamk_date,
            'end_date': vamk_date,
        }
        data = {
            'form': res,
        }
#        return self.env.ref('vamk_work_sheet.report_vamk_wrk_sheet').report_action([],data=data)
        return datas

    def get_attachment(self,task):    
        result, format = self.env.ref('vamk_worksheet_mail.report_vamk_wrksheet_email').render_qweb_pdf(task.ids)
        result = base64.b64encode(result) # Use this in attachment creation in datas field
        ATTACHMENT_NAME = "Mrp Worksheet"
        vamk_attac = self.env['ir.attachment'].create({
                    'name': ATTACHMENT_NAME,           
                    'type': 'binary',           
                    'datas': result,
                    'name': ATTACHMENT_NAME + '.pdf',           
                    'store_fname': ATTACHMENT_NAME,
                    'res_model': 'res.company',           
                    'res_id': task.id,           
                    'mimetype': 'application/x-pdf'           
                    })
        return vamk_attac

    @api.model
    def _send_mail_admin(self):
        su_id = self.env['res.partner'].browse(SUPERUSER_ID)
        for recs in self.env['res.company'].search([('worksheet_mail','!=',None)]):
            mail_body = ('<p>Dear %s,</p>\
                       <p>This mail is intimate for the mrp worksheet report,</p>\
                       ') \
                       % (recs.name)
            mail_values_approval = {'email_to':recs.worksheet_mail ,'subject': 'Work Sheet Report','body_html': mail_body,'notification': True}          
            mail = self.env['mail.mail'].create(mail_values_approval)
            mail.write({'attachment_ids': [(4, self.get_attachment(recs).id)]})
            mail.send()
            return True
