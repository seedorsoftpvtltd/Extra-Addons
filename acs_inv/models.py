from odoo import api, models, fields

class GSTDetails(models.Model):
    _inherit = "account.move"    
    
    enable_eway = fields.Boolean('E-Way Bill Details',store=True)
    bill_no = fields.Char('E-Way Bill No')
    tran_name = fields.Char('Transport Name')
    del_thr = fields.Selection([('1', 'Road'),('2', 'Rail'),('3', 'Air'),('4', 'Ship'),],string='Delivery Through')
    veh_no = fields.Char('Vehicle Name')
    # gst_value = fields.Many2many('account.tax', 'acs_rel','acs_id','taxs_id',string='GST',compute='_compute_gst')
    
    
    # @api.depends('invoice_line_ids')
    # def _compute_gst(self):
        # for record in self:
            # tsx = []
            # for recs in record.invoice_line_ids:
                # for tx in recs.tax_ids:
                    # tsx.append(tx.id)            
            # record['gst_value'] = tsx

                       
  