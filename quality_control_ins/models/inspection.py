from odoo import api, fields, models, _
import datetime

class WarehouseDelMove(models.Model):
    _inherit = 'stock.move'

#    inspection_created = fields.Boolean(string="Inspection Created")


    def ins(self):
        for rec in self:
            id = self.env['stock.move'].search([('id', '=', rec.id)])
            idd = 'stock.move,%s' % rec.id
            test_categ = self.env['qc.test.category'].search([('name', '=', 'Generic')])
            test = self.env['qc.test'].search([('category', '=', test_categ.id)])
            
            vals = {'object_id': idd,
                    'name': self.env['ir.sequence'].next_by_code('qc.inspection'),
                    'date': datetime.datetime.now(),
                    'test': test.id,
                    }
            print(vals, rec.id, id)

            ins = self.env['qc.inspection'].create(vals)
            ins.inspection_lines = ins._prepare_inspection_lines(ins.test)
            print(ins, 'Automated quality control running', rec.id, id)
            rec.inspection_created = True


    def write(self, vals):

        res = super(WarehouseDelMove, self).write(vals)
        print(vals, 'valsssssssssssssssssssssssssssss')
        for rec in self:
            if rec.inspection_created == False:
                rec.ins()
        return res

