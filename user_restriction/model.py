from odoo import api, models, fields, _
from odoo.exceptions import UserError


class UserInherit(models.Model):
    _inherit = "res.users"

    def write(self, values):
        if self.env.user.name == 'Super User':
            return super(UserInherit, self).write(values)
        else:
            if self.name != 'Super User':
                return super(UserInherit, self).write(values)
            else:
                raise UserError(_('You are not allowed to make changes!'))


