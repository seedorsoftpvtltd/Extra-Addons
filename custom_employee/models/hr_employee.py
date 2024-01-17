from odoo import api, fields, models, _



class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"
    
    labour_card_no = fields.Char(string='Labour Card No')
    expiry_date = fields.Date('Labour Card Expiry Date', tracking=True)
    passport_no = fields.Char(string='Passport No')
    passport_expiry_date = fields.Date('Passport Expiry Date', tracking=True)
    visa_nos = fields.Char(string='Visa No')
    visa_expiry_date = fields.Date('Visa Expiry Date', tracking=True)
    emirates_id_no = fields.Char(string='Emirates ID No')
    emirates_expiry_date = fields.Date('Emirates ID Expiry', tracking=True)
    arrival_date = fields.Date('Date of Arrival', tracking=True)
    joining_date = fields.Date('Date of Joining', tracking=True)
    in_visa_id = fields.Many2one('hr.job',string='In Visa')
    work_as_id = fields.Many2one('hr.job',string='As a Work')
    document_signed = fields.Char('Document Signed')
    leaving_date = fields.Date('Date of Leaving', tracking=True)
        
        
        
        
        
