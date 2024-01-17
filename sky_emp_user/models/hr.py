# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning


class Employee(models.Model):
    _inherit = 'hr.employee'

    automatic_user_create = fields.Boolean('Create User Automatically?',
                                           default=lambda self: self.env.user.
                                           company_id.automatic_user_create,
                                           copy=False,
                                           help="automatic user\
                                           creation along with employee")

    @api.model
    def create(self, vals):
        """
        Overridden create method to create a user
        and set working address for employee
        -----------------------------------------
        @param self: object pointer
        @param vals: A dictionary containing fields and values
        """
        # template for sending an email
        template = self.env.ref('sky_emp_user.email_template_login_credentials'
                                )
        # if automatic user creation is enabled
        if vals.get('automatic_user_create'):
            # user creation vals
            usr_vals = {
                'name': vals['name'],
                'login': vals['work_email'],
                'email': vals['work_email'],
            }
            # password needs to be set in configuration
            if not self.env.user.company_id.password:
                err_msg = _('Please set password in configuration.')
                redir_msg = _('Go to the configuration panel')
                raise RedirectWarning(err_msg, self.env.ref(
                    'hr.hr_config_settings_action').id, redir_msg)
            job_obj = self.env['hr.job']
            usr_obj = self.env['res.users']
            job = job_obj.browse(vals.get('job_id'))
            group_ids = job.group_ids and job.group_ids.ids or []
            # update user vals with password
            if self.env.user.company_id.pwd_email == 'send_pwd':
                usr_vals.update({
                    'password': self.env.user.company_id.password
                })
            if group_ids:
                usr_vals.update({
                    'groups_id': [(4, g_id) for g_id in group_ids]
                })
            # Create User
            user = usr_obj.sudo().with_context(
                no_reset_password=True, create_user=True).create(usr_vals)
            template.email_to = user.partner_id.email
            # sending invitation link for credentials
            if self.env.user.company_id.pwd_email == 'send_link':
                user.action_reset_password()
            user.partner_id.parent_id = user.company_id.partner_id.id
            # Link the user to the Employee along with the Work Address
            vals.update({
                'user_id': user.id,
                'address_id': user.partner_id.id
            })
        res = super(Employee, self).create(vals)
        # send password in email
        if self.env.user.company_id.pwd_email == 'send_pwd':
            template.send_mail(res.id, force_send=True, raise_exception=True)
        return res

    def write(self, vals):
        """
        Overridden write method to update the groups of the user
        in case the job position of the employee is updated
        ---------------------------------------------------
        @param self: object pointer
        @param vals: a dictionary containing fields and values
        """
        job_obj = self.env['hr.job']
        for emp in self:
            # If Job position is updated in employee the groups
            # must be updated in the related user
            if vals.get('job_id', False):
                job = job_obj.browse(vals['job_id'])
                group_ids = job.group_ids and job.group_ids.ids or []
                if group_ids:
                    emp.user_id.write({
                        'groups_id': [(4, g_id) for g_id in group_ids]
                    })
            # If Employee is archived or unarchived also User should be updated
            if vals.get('active'):
                emp.user_id.active = vals['active']
                emp.user_id.partner_id.active = vals['active']
        return super(Employee, self).write(vals)

    def unlink(self):
        """
        This method will unlink the related user and partner
        ----------------------------------------------------
        @param self : object pointer
        """
        for emp in self:
            if emp.user_id:
                emp.user_id.unlink()
                emp.user_id.partner_id.unlink()
        return super(Employee, self).unlink()


class Job(models.Model):
    _inherit = 'hr.job'

    group_ids = fields.Many2many('res.groups', string='Groups')
