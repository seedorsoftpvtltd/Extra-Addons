import json
import requests
from odoo import api, fields, models, _
import json.decoder
from odoo.exceptions import UserError


class EmployeeFace(models.Model):
    _inherit = "hr.employee.faces"

    user = fields.Many2one('res.users', related='employee_id.user_id')
#    logging = fields.Many2one('ir.logging', string="Logging")
#    dbname = fields.Char(string="DB Name", related='logging.dbname')


    def add_employee_face(self):
        print(self.env.cr.dbname)
        payload = json.dumps({"image": self.image.decode('utf-8'), "employee_id": str(self.employee_id.id), "user_id":str(self.user.id), "client_id":str(self.env.cr.dbname)})
        print(payload)
        headers = {
            'Content-Type': 'application/json'
        }
#        url = "http://eiuat.seedors.com:5000/add-employee-face"
        url = "http://miprod.seedors.com:5000/add-employee-face"
        #print(url)
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        print(response.text)
        print(response)
        print(response.status_code)
        print('Face Recognition Status Code-------------->' + str(response.status_code))
        if response.status_code == 501:
            raise UserError(_('Could not find face in entered photo'))
        elif response.status_code == 400:
            raise UserError(_('Invalid Credentials: Please link the user'))


#    def unlink(self):
#        payload = json.dumps(
#            {"employee_id": str(self.employee_id.id), "user_id": str(self.user.id),
#             "client_id": str(self.env.cr.dbname)})

#        print(payload)
#        headers = {
#            'Content-Type': 'application/json'
#        }
#        url = "http://miprod.seedors.com:5000/remove-employee-face"
#        url = "http://eiuat.seedors.com:5000/remove-employee-face"
#        print(url)
#        response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)
#        print(response.text)
#        print(response)
#        print(response.status_code)
#        if response.status_code != 200:
#            raise UserError(_('Could not delete face'))
#        return super(EmployeeFace, self).unlink()
