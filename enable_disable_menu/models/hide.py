from odoo import api, fields, models, _


class menu(models.Model):
    _inherit = 'ir.ui.menu'

    category=fields.Many2one('menu.category',string='Category',store=True)

    def manual_enable(self):
        for rec in self:
            rec['active']=True

    def manual_disable(self):
        for rec in self:
            rec['active'] = False


    def button(self,category):
        cat_disable = category

        # categ = self.env['ir.ui.menu'].search([('category', '=', cat_disable)])
        # hide_group = self.env.ref('enable_disable_menu.group_menu_hide').id
        # if not categ:
        #     return False
        # for rec in categ:
        #     # rec['active']=False
        #     rec.write({'groups_id': [(5, 0, 0), (4, hide_group)]})
        # return categ
        query = """
                        SELECT id, name, action,active,category
                        FROM ir_ui_menu
                        WHERE category = %s
                    """
        self.env.cr.execute(query, tuple([cat_disable]))
        result1 = self.env.cr.dictfetchall()
        if result1:
            for result in result1:
                menu_id = result['id']
                menu = self.env['ir.ui.menu'].browse(menu_id)
                if menu.exists():
                    menu.active = False
                else:
                    return False
        else:
            return False
        return True
        # for rec in query:
        #     rec.active = False

    def button_enable(self, category):
        cat_enable = category
        query = """
                                SELECT id, name, action,active,category
                                FROM ir_ui_menu
                                WHERE category = %s
                            """
        self.env.cr.execute(query, tuple([cat_enable]))
        result1 = self.env.cr.dictfetchall()
        if result1:
            for result in result1:
                menu_id = result['id']
                menu = self.env['ir.ui.menu'].browse(menu_id)
                if menu.exists():
                    menu.active = True
                else:
                    return False
        else:
            return False
        return True
        # categ = self.env['ir.ui.menu'].search([('category', '=', cat_enable)])
        #
        # hide_group = self.env.ref('enable_disable_menu.group_menu_hide').id
        # if not categ:
        #     return False
        # for rec in categ:
        #     rec['active'] = True
        #     # rec.write({'groups_id': [(5, 0, [hide_group])]})


class category(models.Model):
    _name="menu.category"
    _rec_name = 'category'

    category=fields.Char(string="Menu Category")
