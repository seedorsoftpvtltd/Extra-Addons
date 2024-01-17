from odoo import api, exceptions, fields, models, _
from odoo.tools.safe_eval import safe_eval
from odoo.tools.translate import _
from odoo.exceptions import RedirectWarning
from odoo.exceptions import UserError, Warning


class Baseuserscount(models.Model):
    _inherit = "res.company"

    internal_usrcnt = fields.Integer('Internal Users Count', compute='_internal_usrcnt')
    empportal_usrcnt = fields.Integer('Internal Users Count', compute='_empportal_usrcnt')
    portal_usrcnt = fields.Integer('Internal Users Count', compute='_portal_usrcnt')

    def _internal_usrcnt(self):
        for rec in self:
            int = self.env['res.users'].sudo().search_count([('usertype', '=', 'intuser'), ('active', '=', True)])
            rec['internal_usrcnt'] = int


    def _empportal_usrcnt(self):
        for rec in self:
            int = self.env['res.users'].sudo().search_count([('usertype', '=', 'empuser'), ('active', '=', True)])
            rec['empportal_usrcnt'] = int


    def _portal_usrcnt(self):
        for rec in self:
            int = self.env['res.users'].sudo().search_count([('usertype', '=', 'portuser'), ('active', '=', True)])
            rec['portal_usrcnt'] = int



class BaseLimituser(models.Model):
    _inherit = "res.users"

    usertype = fields.Selection(
        [('empuser', 'Employee User'),('intuser', 'Internal User'),
         ('portuser', 'Portal User'), ('publicuser', 'Public User')], required="True", string="Type",
        store="True", readonly=False)

    @api.model
    def create(self, vals):
        res = super(BaseLimituser, self).create(vals)
        if res.usertype == 'empuser':
            u = res.id
            g = self.env.ref('base.group_user')
            g.write({'users': [(3, u)]})
            grp = self.env.ref('base.group_portal')
            grp.write({'users': [(4, u)]})
            # res['sel_groups_1_8_9'] = 8
            # emp = {
            #     'name': res.name,
            #     'user_id': res.id,
            #     'work_email': res.login,
            # }
            # self.env['hr.employee'].create(emp)
            # print(emp)
            # res['employee_id'] = t.id
            res.action_reset_password()
        if res.usertype == 'intuser':
            emp = {
                'name': res.name,
                'user_id': res.id,
                'work_email': res.login,
                'usertype':res.usertype,
            }
            namee = res.name
            nm = self.env['hr.employee'].search([('name','=',namee)])
            if not nm:
                h =self.env['hr.employee'].create(emp)
                # res['employee_id'] = t.id
        return res


class EmpExtend(models.Model):
    _inherit = "hr.employee"

    usertype = fields.Selection(
        [('empuser', 'Employee User'), ('intuser', 'Internal User')], required="True", string="Type",
        store="True", readonly=False)
    
    def grant_access(self):
        for rec in self:
            rec.ensure_one()
            if not rec.work_email:
                raise Warning(_('Please Enter Work Email !'))
            user_val = {
                'active': True,
                # 'is_employee': True,
                'employee_id': rec.id,
                'login': rec.work_email,
                'email':rec.work_email,
                'name': rec.name,
                'usertype':'empuser'if rec.usertype == 'empuser' else 'intuser',
                # 'image': rec.image
            }
            user_obj = self.env['res.users']
            user_created = user_obj.sudo().create(user_val)
            if user_created:
                # rec.write({'is_user': True})
                if not rec.address_id:
                    rec.address_id = user_created.partner_id.id
                    rec.address_id.email = rec.work_email
                    rec.address_id.mobile = rec.mobile_phone
                    rec.address_id.phone = rec.work_phone
                if not rec.user_id:
                    rec.user_id = user_created.id
        

    # def grant_access(self):
    #     self.ensure_one()
    #     user_val = {
    #         'active': True,
    #         # 'is_employee': True,
    #         'employee_id': self.id,
    #         'login': self.work_email,
    #         'name': self.name,
    #         # 'image': self.image
    #     }
    #     user_obj = self.env['res.users']
    #     user_created = user_obj.sudo().create(user_val)
    #     if user_created:
    #         # self.write({'is_user': True})
    #         if not self.address_id:
    #             self.address_id = user_created.partner_id.id
    #             self.address_id.email = self.work_email
    #             self.address_id.mobile = self.mobile_phone
    #             self.address_id.phone = self.work_phone
    #         if not self.user_id:
    #             self.user_id = user_created.id

    # @api.model
    # def write(self, vals):
    #     res = super(EmpExtend, self).write(vals)
    #     print('Hlo')
    #
    #     if 'work_email' in vals:
    #         user = self.env['res.users'].sudo().search(
    #             ['&', ('id', '=', self.user_id.id), ('usertype', '=', 'empuser')])
    #         print(user)
    #         usr = {
    #             'name': self.name,
    #             'login': self.work_email,
    #         }
    #         print(usr)
    #         user.write(usr)
    #         # self.hb()
    #     return res

    # @api.model
    # def create(self, vals):
    #     res = super(EmpExtend, self).create(vals)
    #     part =  {
    #         'name':'res.name',
    #         'user_id':
    #     }
    #     cnt = self.env['res.partner'].create(part)
    #     print(cnt.id)
    #     usr = {
    #         'name': res.name,
    #         'user_id': res.id,
    #         'login': res.work_email,
    #         'usertype':'empuser',
    #         # 'partner_id':cnt.id,
    #     }
    #     self.env['res.users'].create(usr)
    #     print(usr)


# class BaseLimitRecordsNumberinh(models.Model):
#     _inherit = "base.limit.records_number"
#
#     # usertype = fields.Selection(
#     #     [('empuser', 'Is Employee User'),('intuser', 'Is Internal User'),
#     #      ('portuser', 'Is Portal User'), ('publicuser', 'Is Public User')], string="Type", store="True",
#     #     readonly=False)
#
#     # @api.depends('model_id')
#     # def create(self):
#     #     # res = super(BaseLimitRecordsNumberinh, self).create(vals)
#     #     # print(res.usertype)
#     #     for rec in self:
#     #         if rec.model_id.model == 'res.users':
#     #             print("if")
#     #             if rec:
#     #                 print("iif")
#     #                 raise Warning(_('Please select the User Type'))
#
#
#
#
#
#
#
#     @api.model
#     def verify_table_extend(self):
#         print("EXTENDED")
#         """ Get parameters and verify. Raise exception if limit """
#         model_name = self.env.context["active_model"]
#         print(model_name)
#         if model_name == 'res.users':
#             print(self.env.context.get('active_ids'))
#             active_id = self.env.context.get('active_id')
#             rec = self.env[model_name].browse(active_id)
#             print(rec)
#             print(rec.usertype)
#             if rec.usertype == 'empuser':
#                 for rule in self.search(['&', ("model_id.model", "=", model_name), ("usertype", "=", "empuser")]):
#                     records_count = self.env[model_name].search_count(safe_eval(rule.domain))
#                     if records_count > rule.max_records:
#                         raise exceptions.Warning(
#                             _(
#                                 'Maximimum allowed records in table "%(model_name)s" is %(max_records)s, while after this update you would have %(records_count)s'
#                             )
#                             % {
#                                 "model_name": rule.model_id.name,
#                                 "max_records": rule.max_records,
#                                 "records_count": records_count,
#                             }
#                         )
#             if rec.usertype == 'portuser':
#                 for rule in self.search([("model_id.model", "=", model_name), ("usertype", "=", "portuser")]):
#                     records_count = self.env[model_name].search_count(safe_eval(rule.domain))
#                     if records_count > rule.max_records:
#                         raise exceptions.Warning(
#                             _(
#                                 'Maximimum allowed records in table "%(model_name)s" is %(max_records)s, while after this update you would have %(records_count)s'
#                             )
#                             % {
#                                 "model_name": rule.model_id.name,
#                                 "max_records": rule.max_records,
#                                 "records_count": records_count,
#                             }
#                         )
#             if rec.usertype == 'intuser':
#                 for rule in self.search([("model_id.model", "=", model_name), ("usertype", "=", "intuser")]):
#                     records_count = self.env[model_name].search_count(safe_eval(rule.domain))
#                     if records_count > rule.max_records:
#                         raise exceptions.Warning(
#                             _(
#                                 'Maximimum allowed records in table "%(model_name)s" is %(max_records)s, while after this update you would have %(records_count)s'
#                             )
#                             % {
#                                 "model_name": rule.model_id.name,
#                                 "max_records": rule.max_records,
#                                 "records_count": records_count,
#                             }
#                         )
#             if rec.usertype == 'publicuser':
#                 for rule in self.search([("model_id.model", "=", model_name), ("usertype", "=", "publicuser")]):
#                     records_count = self.env[model_name].search_count(safe_eval(rule.domain))
#                     if records_count > rule.max_records:
#                         raise exceptions.Warning(
#                             _(
#                                 'Maximimum allowed records in table "%(model_name)s" is %(max_records)s, while after this update you would have %(records_count)s'
#                             )
#                             % {
#                                 "model_name": rule.model_id.name,
#                                 "max_records": rule.max_records,
#                                 "records_count": records_count,
#                             }
#                         )
#         else:
#             """ Get parameters and verify. Raise exception if limit """
#             model_name = self.env.context["active_model"]
#             for rule in self.search([("model_id.model", "=", model_name)]):
#                 records_count = self.env[model_name].search_count(safe_eval(rule.domain))
#                 if records_count > rule.max_records:
#                     raise exceptions.Warning(
#                         _(
#                             'Maximimum allowed records in table "%(model_name)s" is %(max_records)s, while after this update you would have %(records_count)s'
#                         )
#                         % {
#                             "model_name": rule.model_id.name,
#                             "max_records": rule.max_records,
#                             "records_count": records_count,
#                         }
#                     )
#         return super(BaseLimitRecordsNumberinh, self).verify_table()

