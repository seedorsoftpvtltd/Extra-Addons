from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import itertools
from operator import itemgetter
import operator

class job_wizard(models.TransientModel):
    _name = 'job.wizard'
    _description = 'Job Category'

    category = fields.Many2one('job.category', string='Category')
    types =  fields.Many2one('utm.medium')

    @api.model
    def default_get(self,vals):
        res = super(job_wizard, self).default_get(vals)
        job = self.env['job.category'].search([]).job_types
        if job:
            for tr in job:
                tr.is_job_category_booking = True
        return res

    def apply_category(self):
       if not self.category:
            raise ValidationError(_("Select any of the above category"))

       else:
        return {
            'type': 'ir.actions.act_window',
            'name': _('Job Booking'),
            'res_model': 'freight.operation',
            'view_mode': 'form',
            'limit': 99999999,
            'search_view_id': self.env.ref('scs_freight.view_freight_operation_form').id,
            'context': {'default_direction': self.category.direction,
                        'default_transport':self.category.transport,
                        'default_ocean_shipping': self.category.ocean_shipping,
                        'default_land_shipping': self.category.land_shipping,
                        'default_freight_air_shipping': self.category.freight_air_shipping,
                        'default_x_job_type': self.category.job_types,
                        'default_x_cb_type':self.category.x_cb_type,
                        'default_category': self.category.id,


                        },
        }



