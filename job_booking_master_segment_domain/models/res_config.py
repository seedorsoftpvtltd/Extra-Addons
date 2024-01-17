from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
   _inherit = 'res.config.settings'

   enable_domain = fields.Boolean(string="Enable Master Segment")

   def set_values(self):
      res = super(ResConfigSettings, self).set_values()
      self.env['ir.config_parameter'].set_param('job_booking_master_segment_domain.enable_domain', self.enable_domain)
      return res


   def get_values(self):
      res = super(ResConfigSettings, self).get_values()
      value = self.env['ir.config_parameter'].sudo().get_param('job_booking_master_segment_domain.enable_domain')
      res.update({
         'enable_domain': value
      })
      return res
