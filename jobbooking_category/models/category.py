from odoo import fields, models,api,_
from odoo.exceptions import UserError, ValidationError

class freight_operation(models.Model):
      _inherit='freight.operation'

      category = fields.Many2one('job.category',string='Category')

      description= fields.Char('Description')
      x_cb_type =fields.Selection(
        [("import", "Import"), ("export", "Export")],
        default="import",
        string="Service Type",)



      @api.onchange('category')
      def _compute_auto_fill(self):
          for rec in self:
                # print("zzzzzzzzz")
                if rec.category:
                  rec['x_job_type'] = rec.category.job_types
                  rec['direction'] = rec.category.direction
                  rec['transport'] = rec.category.transport
                  rec['ocean_shipping'] = rec.category.ocean_shipping
                  rec['land_shipping'] = rec.category.land_shipping
                  rec['freight_air_shipping'] = rec.category.freight_air_shipping
                  rec['x_cb_type'] = rec.category.x_cb_type




class freight_category(models.Model):
    _name='job.category'
    _rec_name = 'category'

    x_cb_type = fields.Selection(
        [("import", "Import"), ("export", "Export")],
        default="import",
        string="Service Type", )

    direction = fields.Selection(
        [("import", "Import"), ("export", "Export"), ("cross_trade", "Cross Trade"),
         ("local_services", "Local Services"),
         ("customs_brokerage", "Customs Brokerage"), ("contract_logistics", "Contract logistics"), ('3pl', '3 PL'),
         ('rental', 'Rental'), ('value_added', 'Value Added Services'), ('cross_docking', 'Cross Docking')],
        string="Segment",
        default="import",
    )
    transport = fields.Selection(
        [("land", "Land"), ("ocean", "Ocean"), ("air", "Air")],
        default="land",
        string="Transport",
    )
    ocean_shipping = fields.Selection(
        [("fcl", "FCL"), ("lcl", "LCL"), ("bulk", "BULK")],
        string="Service Type",
        default="fcl",
        help="""FCL: Full Container Load.
            LCL: Less Container Load.""",
    )
    land_shipping = fields.Selection(
        [("ftl", "FTL"), ("ltc", "LTL"), ("local_transport", "Local Transport"),("local_services", "Local Services")],
        string="Service Type",
        default="ftl",
        help="""FTL: Full Truckload.LTL: Less Then Truckload.""",
    )
    freight_air_shipping = fields.Selection(
        [("general", "General"), ("perishable", "Perishable"), ("temperature", "Temperature Control")],
        default="general",
        string="Service Type")
    category = fields.Char(string='Category')
    department_code = fields.Char(string='Department Code')
    job_types = fields.Many2one('utm.medium')
    #_sql_constraints = [("category_unique", "UNIQUE(category)", "Same Category Already Exist")]

    @api.constrains('category')
    def _check_category(self):
        for rec in self:
            domain = [('category', '=', rec.category)]
            count = self.sudo().search_count(domain)
            if count > 1:
                raise ValidationError(_("Same Category Already Exist"))


    @api.onchange('direction','transport','job_types','x_cb_type','land_shipping','ocean_shipping','freight_air_shipping')
    @api.depends('direction','transport','job_types','x_cb_type','land_shipping','ocean_shipping','freight_air_shipping')
    def _compute_category(self):
        for rec in self:
            # print("aaaaaaaaaaaa")
            # print(self.land_shipping[])

            if rec.job_types:

                if rec.transport == 'land' :

                    if rec.direction == 'customs_brokerage':
                        a = rec._fields['x_cb_type'].selection
                        code_dict = dict(a)
                        name1 = code_dict.get(rec.x_cb_type)
                        b = rec._fields['transport'].selection
                        code_dict = dict(b)
                        name2 = code_dict.get(rec.transport)
                        c = rec._fields['direction'].selection
                        code_dict = dict(c)
                        name3 = code_dict.get(rec.direction)
                        print(name1, name2, name3)
                        rec['category'] = rec.job_types.name + ' ' + name1 + ' ' + '-' + ' ' + name2 + ' ' + name3

                    else:
                        a = rec._fields['land_shipping'].selection
                        code_dict = dict(a)
                        name1 = code_dict.get(rec.land_shipping)
                        b = rec._fields['transport'].selection
                        code_dict = dict(b)
                        name2 = code_dict.get(rec.transport)
                        c = rec._fields['direction'].selection
                        code_dict = dict(c)
                        name3 = code_dict.get(rec.direction)
                        print(name1,name2,name3)

                        rec['category']=rec.job_types.name+ ' '+name1 + ' ' + '-' + ' ' +name2 + ' ' +name3
                elif rec.transport == 'ocean' :
                    if rec.direction == 'customs_brokerage':
                        a = rec._fields['x_cb_type'].selection
                        code_dict = dict(a)
                        name1 = code_dict.get(rec.x_cb_type)
                        b = rec._fields['transport'].selection
                        code_dict = dict(b)
                        name2 = code_dict.get(rec.transport)
                        c = rec._fields['direction'].selection
                        code_dict = dict(c)
                        name3 = code_dict.get(rec.direction)
                        rec['category'] = rec.job_types.name + ' ' + name1 + ' ' + '-' + ' ' + name2 + ' ' + name3
                    else:

                        a = rec._fields['ocean_shipping'].selection
                        code_dict = dict(a)
                        name1 = code_dict.get(rec.ocean_shipping)
                        b = rec._fields['transport'].selection
                        code_dict = dict(b)
                        name2 = code_dict.get(rec.transport)
                        c = rec._fields['direction'].selection
                        code_dict = dict(c)
                        name3 = code_dict.get(rec.direction)
                        rec['category'] = rec.job_types.name + ' ' + name1 + ' ' + '-' + ' ' + name2 + ' ' + name3
                elif rec.transport == 'air' :
                    if rec.direction == 'customs_brokerage':
                        a = rec._fields['x_cb_type'].selection
                        code_dict = dict(a)
                        name1 = code_dict.get(rec.x_cb_type)
                        b = rec._fields['transport'].selection
                        code_dict = dict(b)
                        name2 = code_dict.get(rec.transport)
                        c = rec._fields['direction'].selection
                        code_dict = dict(c)
                        name3 = code_dict.get(rec.direction)
                        rec['category'] = rec.job_types.name + ' ' + name1 + ' ' + '-' + ' ' + name2 + ' ' + name3
                    else:

                        a = rec._fields['freight_air_shipping'].selection
                        code_dict = dict(a)
                        name1 = code_dict.get(rec.freight_air_shipping)
                        b = rec._fields['transport'].selection
                        code_dict = dict(b)
                        name2 = code_dict.get(rec.transport)
                        c = rec._fields['direction'].selection
                        code_dict = dict(c)
                        name3 = code_dict.get(rec.direction)
                        rec['category'] = rec.job_types.name + ' ' + name1 + ' ' + '-' + ' ' + name2 + ' ' + name3

