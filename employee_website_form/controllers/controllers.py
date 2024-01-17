# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
class PartnerForm(http.Controller):
    #mention class name
    @http.route(['/employee/form'], type='http', auth="public", website=True)

    def partner_form(self, **post):
        employee=request.env.user.employee_id
        partner = request.env.user.partner_id
        countries = request.env['res.country'].sudo().search([])
        department = request.env['hr.department'].sudo().search([])
        job = request.env['hr.job'].sudo().search([])

        print(countries)

        values= {}
        values.update({
            'employee': employee,
            'partner' : partner,
            "countries":countries,
            'department':department,
            'job':job,
        })


        return request.render("employee_website_form.tmp_customer_form", values)
    @http.route(['/employee/form/submit'], type='http', auth="public", website=True)
    #next controller with url for submitting data from the form#
    def customer_form_submit(self, **post):


        employee = request.env.user.employee_id
        partner =request.env.user.partner_id
        part=partner.update({
            'email': post.get('partner_email'),
        })
        emp=employee.update({
            'name': post.get('name'),
            'mobile_phone': post.get('mobile_phone'),
            'work_email': post.get('email'),
            'work_phone': post.get('phone'),
            'department_id': int(post.get('employee.department_id')),
            'job_id': int(post.get('employee.job_id')),
            # 'private_email':post.get('private_email'),
            'phone': post.get('private_phone'),
            'passport_id': post.get('passport_id'),
            'passport_expiry_date': post.get('passport_expiry_date'),
            'emergency_contact': post.get('emergency_contact'),
            'emergency_phone': post.get('emergency_phone'),
            'country_id': int(post.get('employee.country_id')),
            'gender': post.get('gender'),
            'marital': post.get('marital'),
            'birthday': post.get('bbirthday'),
            'place_of_birth': post.get('place_of_birth'),
            'country_of_birth': int(post.get('employee.country_of_birth')),
            'children': post.get('children'),
            'identification_id': post.get('identification_id'),
            'visa_no': post.get('visa_no'),
            'permit_no': post.get('permit_no'),
            'visa_expire': post.get('visa_expire'),


        })
        print(post.get('gender'))
        # print(post.get('maritall'))

        vals = {
            'employee': emp,
            'partner': part,
        }
        #inherited the model to pass the values to the model from the form#
        return request.render("employee_website_form.tmp_customer_form_success",vals)
        #finally send a request to render the thank you page#
