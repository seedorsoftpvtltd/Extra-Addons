from odoo import fields, models,api,_
from odoo.exceptions import ValidationError

class sale_order(models.Model):
      _inherit='sale.order'

      category = fields.Many2one('sale.job.category',string='Category')
      x_cb_type =fields.Selection(
        [("import", "Import"), ("export", "Export")],
        default="import",
        string="Service Type",)

      @api.onchange('category')
      def _compute_auto_fill(self):
          for rec in self:
                # print("zzzzzzzzz")
                if rec.category:
                  rec['medium_id'] = rec.category.job_types
                  rec['fright_direction'] = rec.category.freight_direction
                  rec['fright_transport'] = rec.category.freight_transport
                  rec['fright_ocean_shipping'] = rec.category.freight_ocean_shipping
                  rec['fright_land_shipping'] = rec.category.freight_land_shipping
                  rec['freight_air_shipping'] = rec.category.freight_air_shipping
                  rec['x_cb_type'] = rec.category.x_cb_type


class freight_category(models.Model):
    _name='sale.job.category'
    _rec_name = 'category'

    x_cb_type = fields.Selection(
        [("import", "Import"), ("export", "Export")],
        default="import",
        string="Service Type", )

    freight_direction = fields.Selection(
        [("import", "Import"), ("export", "Export"), ("cross_trade", "Cross Trade"),
         ("local_services", "Local Services"),
         ("customs_brokerage", "Customs Brokerage"), ("contract_logistics", "Contract logistics"), ('3pl', '3 PL'),
         ('rental', 'Rental'), ('value_added', 'Value Added Services'), ('cross_docking', 'Cross Docking')],
        string="Segment",
        default="import",
    )
    freight_transport = fields.Selection(
        [("land", "Land"), ("ocean", "Ocean"), ("air", "Air")],
        default="land",
        string="Transport",
    )
    freight_ocean_shipping = fields.Selection(
        [("fcl", "FCL"), ("lcl", "LCL"), ("bulk", "BULK")],
        string="Service Type",
        default="fcl",
        help="""FCL: Full Container Load.
            LCL: Less Container Load.""",
    )
    freight_land_shipping = fields.Selection(
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

    @api.constrains('category')
    def _check_category(self):
        for rec in self:
            domain = [('category', '=', rec.category)]
            count = self.sudo().search_count(domain)
            if count > 1:
                raise ValidationError(_("Same Category Already Exist"))



    @api.onchange('freight_direction','freight_transport','job_types','x_cb_type','freight_land_shipping','freight_ocean_shipping','freight_air_shipping')
    @api.depends('freight_direction','freight_transport','job_types','x_cb_type','freight_land_shipping','freight_ocean_shipping','freight_air_shipping')
    def _compute_category(self):
        for rec in self:
            # print("aaaaaaaaaaaa")
            # print(self.land_shipping[])

            if rec.job_types:

                if rec.freight_transport == 'land' :

                    if rec.freight_direction == 'customs_brokerage':
                        a = rec._fields['x_cb_type'].selection
                        code_dict = dict(a)
                        name1 = code_dict.get(rec.x_cb_type)
                        b = rec._fields['freight_transport'].selection
                        code_dict = dict(b)
                        name2 = code_dict.get(rec.freight_transport)
                        c = rec._fields['freight_direction'].selection
                        code_dict = dict(c)
                        name3 = code_dict.get(rec.freight_direction)
                        print(name1, name2, name3)
                        rec['category'] = rec.job_types.name + ' ' + name1 + ' ' + '-' + ' ' + name2 + ' ' + name3

                    else:
                        a = rec._fields['freight_land_shipping'].selection
                        code_dict = dict(a)
                        name1 = code_dict.get(rec.freight_land_shipping)
                        b = rec._fields['freight_transport'].selection
                        code_dict = dict(b)
                        name2 = code_dict.get(rec.freight_transport)
                        c = rec._fields['freight_direction'].selection
                        code_dict = dict(c)
                        name3 = code_dict.get(rec.freight_direction)
                        print(name1,name2,name3)

                        rec['category']=rec.job_types.name+ ' '+name1 + ' ' + '-' + ' ' +name2 + ' ' +name3
                elif rec.freight_transport == 'ocean' :
                    if rec.freight_direction == 'customs_brokerage':
                        a = rec._fields['x_cb_type'].selection
                        code_dict = dict(a)
                        name1 = code_dict.get(rec.x_cb_type)
                        b = rec._fields['freight_transport'].selection
                        code_dict = dict(b)
                        name2 = code_dict.get(rec.freight_transport)
                        c = rec._fields['freight_direction'].selection
                        code_dict = dict(c)
                        name3 = code_dict.get(rec.freight_direction)
                        rec['category'] = rec.job_types.name + ' ' + name1 + ' ' + '-' + ' ' + name2 + ' ' + name3
                    else:

                        a = rec._fields['freight_ocean_shipping'].selection
                        code_dict = dict(a)
                        name1 = code_dict.get(rec.freight_ocean_shipping)
                        b = rec._fields['freight_transport'].selection
                        code_dict = dict(b)
                        name2 = code_dict.get(rec.freight_transport)
                        c = rec._fields['freight_direction'].selection
                        code_dict = dict(c)
                        name3 = code_dict.get(rec.freight_direction)
                        rec['category'] = rec.job_types.name + ' ' + name1 + ' ' + '-' + ' ' + name2 + ' ' + name3
                elif rec.freight_transport == 'air' :
                    if rec.freight_direction == 'customs_brokerage':
                        a = rec._fields['x_cb_type'].selection
                        code_dict = dict(a)
                        name1 = code_dict.get(rec.x_cb_type)
                        b = rec._fields['freight_transport'].selection
                        code_dict = dict(b)
                        name2 = code_dict.get(rec.freight_transport)
                        c = rec._fields['freight_direction'].selection
                        code_dict = dict(c)
                        name3 = code_dict.get(rec.freight_direction)
                        rec['category'] = rec.job_types.name + ' ' + name1 + ' ' + '-' + ' ' + name2 + ' ' + name3
                    else:

                        a = rec._fields['freight_air_shipping'].selection
                        code_dict = dict(a)
                        name1 = code_dict.get(rec.freight_air_shipping)
                        b = rec._fields['freight_transport'].selection
                        code_dict = dict(b)
                        name2 = code_dict.get(rec.freight_transport)
                        c = rec._fields['freight_direction'].selection
                        code_dict = dict(c)
                        name3 = code_dict.get(rec.freight_direction)
                        rec['category'] = rec.job_types.name + ' ' + name1 + ' ' + '-' + ' ' + name2 + ' ' + name3

