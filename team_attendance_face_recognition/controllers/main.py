from odoo import http
from odoo.http import request
import base64

class HrAttendanceFaceRecognition(http.Controller):
    
#    @http.route('/team_attendance_face_recognition/loadLabeledImages/', type='json', auth="none")
#    def load_labeled_images(self):
#        descriptions = []
#        employees = request.env['hr.employee'].sudo().search([])
#        for employee in employees:
#            descriptors = []
#            for faces in employee.user_faces:
#                if faces.descriptor and faces.descriptor != 'false':
#                    descriptors.append(faces.descriptor)
 #                   print("descriptor---------------------------------")
 #           if descriptors:
 #               vals = {
 #                   "label": employee.id,
 #                   "descriptors": descriptors,
 #               }
 #               descriptions.append(vals)
 #               print("descriptor 2 ------------------------------------------")
 #       print("descriptors")
 #       return descriptions

    @http.route('/team_attendance_face_recognition/loadLabeledImages/', type='json', auth="none")
    def load_labeled_images(self):
        descriptions = []
        u = http.request.env.context.get('uid')
        # e = u.employee_id
        print(u, 'user')
        #  print(e.name)
        employees = request.env['hr.employee'].sudo().search([])
        print(employees)
        # emplo = request.env['hr.employee'].search([('user_id','=','u')])
        # print(emplo)

        for employee in employees.search([('user_id', '=', u)]):
            print(employee)
            # if employee.user_id.id == u:
            print('ytttttttttttttttttttt')
            descriptors = []
            for faces in employee.user_faces:
                if faces.descriptor and faces.descriptor != 'false':
                    descriptors.append(faces.descriptor)
                    print("descriptor---------------------------------")
            if descriptors:
                vals = {
                    "label": employee.id,
                    "descriptors": descriptors,
                }
                descriptions.append(vals)
                print("descriptor 2 ------------------------------------------")
                print("descriptors")
            return descriptions

    @http.route('/team_attendance_face_recognition/getName/<int:employee_id>/', type='json', auth="none")
    def get_name(self,employee_id):
        name = False
        if employee_id:
            employee = request.env['hr.employee'].sudo().search([('id', '=', int(employee_id))])
            name =  employee.name
        return name
