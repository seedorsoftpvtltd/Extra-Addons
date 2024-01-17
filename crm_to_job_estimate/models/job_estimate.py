from odoo import api, fields, models


class EstimateF(models.Model):
    _inherit = "sale.estimate.job"
    lead_ref =fields.Char(string='Lead Reference')
    estim_id = fields.Many2one('crm.lead', string='Estimate Job Req', store=True)

class crm_estimate(models.Model):
    _inherit='crm.lead'

    estimate_job_count = fields.Integer(string='Estimation', compute='_compute_jobb_estim_count')

    def _compute_jobb_estim_count(self):
        obj = self.env['sale.estimate.job'].search([])
        print(obj)
        for serv in self:
            cnt = obj.search_count([
                ('estim_id', '=', serv.id)])
            if cnt != 0:
                print("hii")
                serv['estimate_job_count'] = cnt
            else:
                print("hello")
                serv['estimate_job_count'] = 0

    def action_create_estimate_from_crm(self):
        print('pppppppppppppppppppppppppppp')
        val=[]
        res=self.env['sale.estimate.job'].browse(self._context.get('estim_id', []))
        # sale_pricelist = self.partner_id.property_product_pricelist
        print(res)
        # for rec in self:
        #     val.append([0, 0, {
        #         'partner_id': rec.partner_id.id,
        #
        #     }])
        res.create({
            'partner_id': self.partner_id.id,
            'pricelist_id': self.partner_id.property_product_pricelist.id,
            'estim_id':self.id,
            'lead_ref':self.code
        })


