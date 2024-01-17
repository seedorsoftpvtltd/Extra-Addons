from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


    
class MrpReportWizard(models.TransientModel):
    
    _name = 'mrp.report.wizard'      
        
    date_start = fields.Date(string="Date", default=fields.Date.today)
  #  name = fields.Char('mrp.production', required=False)    
    
    
    
    def get_report(self):
       
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {                
                'date_start': self.date_start,
                      
            },
        }  

                
        return self.env.ref('mrp_pdf.mrp_report').report_action(self, data=data)
        
  



class ReportMrp(models.AbstractModel):   
    
    _name = 'report.mrp_pdf.mrp_report_view'   
    
    
    def _get_report_values(self, docids, data=None):
        docs = self.env['mrp.production'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'mrp.production',
            'docs': docs,
            'proforma': True
        }
        
        
        # date_end = data['form']['date_end']
        # date_start_obj = datetime.strptime(date_start, DATE_FORMAT)
        # date_end_obj = datetime.strptime(date_end, DATE_FORMAT)
        # date_diff = (date_end_obj - date_start_obj).days + 1        
        # project_id = data['form']['project_id']
        # employee_id = data['form']['employee_id']
        
            
           
        # docs = []
        # employees = self.env['account.analytic.line'].search([])
        # for employee in employees:
            # docs.append({
                # 'project_id': employee.project_id.name,                
                # 'employee_id': employee.employee_id.name,
                # 'task_id': employee.task_id.name,
                # 'dd': employee.date,                
                # 'unit_amount': employee.unit_amount,
                # 'project': employee.project_id,                
                # 'employe': employee.employee_id,
                
            # })
            
          
        # tests = []
        # studs = self.env['project.task'].search([])
        # for stud in studs:
            # tests.append({
                # 'planned_hours': stud.planned_hours,
                # 'planned_start_date': stud.x_adate,
                # 'planned_end_date': stud.date_deadline,
                # 'actual_start_date': stud.x_asdate,
                # 'actual_end_date': stud.x_aedate,
                # 'actual_hrs': stud.effective_hours,
            # })
            
        

            
            #'date_end': date_end,                        
            #'docs': docs,            
            #'tests': tests,
           # 'project_id': project_id,
           # 'employee_id': employee_id,
    