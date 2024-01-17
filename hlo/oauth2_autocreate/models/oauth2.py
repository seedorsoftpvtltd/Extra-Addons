from odoo import api, fields, models, _


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def create(self, values):
        user = super(ResUsers, self).create(values)
        firstname = values.get('firstname')
        lastname = values.get('lastname')
        name = values.get('name')
        if firstname and lastname:
            fullname = values.get('firstname') + values.get('lastname')
        elif firstname:
            fullname = values.get('firstname')
        elif lastname:
            fullname = values.get('lastname')
        elif name:
            fullname = values.get('name')

        self.env['muk_rest.oauth2'].create({
            'name': fullname,

            'client_id': fullname,
            'client_secret': values.get('login'),
            'state': 'client_credentials',
            'security': 'basic',
            'user': user.id,

        })
        print('name')
        return user

#    @api.model
    def _autoupdate(self, values):
        firstname = values.get('firstname', self.firstname)
        lastname = values.get('lastname', self.lastname)
        name = values.get('name', self.name)
        login=self.login
        print(login)
        if firstname and lastname:
            fullname1 = firstname + lastname
            fullname = fullname1.replace(" ", "")
        elif firstname:
            fullname2 = firstname
            fullname = fullname2.replace(" ", "")
        elif lastname:
            fullname3 = lastname
            fullname = fullname3.replace(" ", "")
        elif name:
            fullname4 = values.get('name')
            fullname = fullname4.replace(" ", "")
        print(values)
        self.env['muk_rest.oauth2'].search([('user', '=', self.id)]).write({'name': fullname})
        self.env['muk_rest.oauth2'].search([('user', '=', self.id)]).write({'client_id': fullname})
        self.env['muk_rest.oauth2'].search([('user', '=', self.id)]).write({'client_secret': login})

    def write(self, values):
        result = super(ResUsers, self).write(values)
        if 'firstname' in values or 'lastname' in values or 'login' in values:
            self._autoupdate(values) 
#       self._autoupdate(values)
        return result
