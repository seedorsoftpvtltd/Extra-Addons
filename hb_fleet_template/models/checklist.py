from odoo import _, api, fields, models


class FleetChecklistTemplate(models.Model):
    _name = 'fleet.checklist.template'
    _description = 'Checklist Template'

    name = fields.Char(required=True)
    code = fields.Char(string='Reference', required=True)
    # note = fields.Text(string='Description')
    checklist_ids = fields.Many2many('checklist.checklist', 'checklist_checklist_template_rel', 'tempcheck_id',
                                     'checklist_id', string='Checklists')

class CheckFleet(models.Model):
    _name = 'fcheck.fcheck'
    _description = 'Checklist'

    name = fields.Many2one('product.product', string="check name")
    fcheck_id = fields.Many2one('checklist.checklist')
    checkk_id = fields.Many2one('fleet.checklist', required=False)
    green = fields.Boolean('Green', default=False)
    yellow = fields.Boolean('Yellow', default=False)
    red = fields.Boolean('Red', default=False)
    reason = fields.Text('User Description')
    qty = fields.Float('Quantity', default="0")
    # display_name = fields.Char('Display Name',compute='_compute_name')
    result = fields.Selection(
        [("todo", "Todo"), ("success", "Success"), ("failure", "Failure")],
        "Result",
        default="todo",
        readonly=True,
        required=False,
        copy=False,
    )
    statee = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancel", "Cancelled")],
        #  related="template_id.statee",
        string="Template Status",
        readonly=True,
        copy=False,
        store=True,
        default="draft",
    )

    def action_item_success(self):
        return self.write({"result": "success"})

    def action_item_failure(self):
        return self.write({"result": "failure"})

    # @api.constrains('name')
    # def _compute_name(self):
    #     for rec in self:
    #         rec['display_name'] = rec.name.name

    @api.depends("statee")
    def _compute_result(self):
        for rec in self:
            #  if rec.checklist:
            if any(rec.result == "todo"):
                rec.result = "todo"
            elif any(rec.result == "failure"):
                rec.result = "failure"
            else:
                rec.result = "success"

            # else:
            #     rec.result = "todo"

    # def create(self):
    #     for rec in self:
    #         print("createeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    #         rec['qty']=0
    #         rec['green']=True
    #         rec['red']=True
    #         rec['yellow']=True


class CheckFleet(models.Model):
    _name = 'check.check'
    _description = 'Checklist'

    name = fields.Many2one('product.product', string="check name")
    check_id = fields.Many2one('checklist.checklist')
  #  checkk_id = fields.Many2one('fleet.checklist')
    green = fields.Boolean('Green', default=False)
    yellow = fields.Boolean('Yellow', default=False)
    red = fields.Boolean('Red', default=False)
    reason = fields.Text('User Description')
    qty = fields.Float('Quantity', default="0")
    display_name = fields.Char('Display Name',compute='_compute_name')
    result = fields.Selection(
        [("todo", "Todo"), ("success", "Success"), ("failure", "Failure")],
        "Result",
        default="todo",
        readonly=True,
        required=False,
        copy=False,
    )
    statee = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancel", "Cancelled")],
        #  related="template_id.statee",
        string="Template Status",
        readonly=True,
        copy=False,
        store=True,
        default="draft",
    )

    def action_item_success(self):
        return self.write({"result": "success"})

    def action_item_failure(self):
        return self.write({"result": "failure"})

    @api.constrains('name')
    def _compute_name(self):
        for rec in self:
            rec['display_name'] = rec.name.name

    @api.depends("statee")
    def _compute_result(self):
        for rec in self:
            #  if rec.checklist:
            if any(rec.result == "todo"):
                rec.result = "todo"
            elif any(rec.result == "failure"):
                rec.result = "failure"
            else:
                rec.result = "success"

            # else:
            #     rec.result = "todo"

    # def create(self):
    #     for rec in self:
    #         print("createeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    #         rec['qty']=0
    #         rec['green']=True
    #         rec['red']=True
    #         rec['yellow']=True



class ChecklistFleet(models.Model):
    _name = 'checklist.checklist'
    _description = 'Checklist'

    checklist = fields.One2many('check.check', 'check_id', string="check")
    checkf = fields.One2many('fcheck.fcheck', 'fcheck_id', string="check")
    checklistf = fields.Many2one('fleet.checklist', string="check")
    qty = fields.Float('Quantity')
    active = fields.Boolean('Active', default=True)
    display_name = fields.Char('Name', compute='_compute_name')
    type = fields.Char(string='Type')
    green = fields.Boolean('Green')
    yellow = fields.Boolean('Yellow')
    red = fields.Boolean('Red')
    reason = fields.Text('User Description')
    image = fields.Binary("Image")

    # result = fields.Selection(
    #     [("todo", "Todo"), ("success", "Success"), ("failure", "Failure")],
    #     "Result",
    #     default="todo",
    #     readonly=True,
    #     required=False,
    #     copy=False,
    # )
    # statee = fields.Selection(
    #     [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancel", "Cancelled")],
    #     #  related="template_id.statee",
    #     string="Template Status",
    #     readonly=True,
    #     copy=False,
    #     store=True,
    #     default="draft",
    # )
    #
    # def action_item_success(self):
    #     return self.write({"result": "success"})
    #
    # def action_item_failure(self):
    #     return self.write({"result": "failure"})

    @api.constrains('type')
    def _compute_name(self):
        for rec in self:
            rec['display_name'] = rec.type

    # @api.depends("checklist", "statee")
    # def _compute_result(self):
    #     for rec in self:
    #         if rec.checklist:
    #             if any(l.result == "todo" for l in rec.checklist):
    #                 rec.result = "todo"
    #             elif any(l.result == "failure" for l in rec.checklist):
    #                 rec.result = "failure"
    #             else:
    #                 rec.result = "success"
    #         else:
    #             rec.result = "todo"


class CustomerChecklist(models.Model):
    _name = 'fleet.checklist'
    _description = 'Fleet Checklist'

    # service_prod = fields.Many2one('product.product', string='Name', required=True, related='checklist_id.service_prod')
    # qty = fields.Float('Quantity')
    image = fields.Binary("Image")
    # description = fields.Text(string='Description', required=True, related='checklist_id.description')
    # checklist_id = fields.One2many('checklist.checklist','checklistf')
    service_id = fields.Many2one('fleet.vehicle.log.services', 'Services')
    checklist_id = fields.Many2one('checklist.checklist', 'Checklist')
    checklist = fields.One2many('fcheck.fcheck', 'checkk_id', string="check")



class FleetVehicleInh(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    checklist_ids = fields.One2many('fleet.checklist', 'service_id', 'Checklists')
    model = fields.Many2one('fleet.vehicle.model','Model',related='vehicle_id.model_id')
    # total_checklist = fields.Float('Total Checklist', compute='compute_checklists')
    # completed_checklist = fields.Integer('Completed Checklist', compute='compute_checklists')
    # inprogress_checklist = fields.Integer('In-progress Checklist', compute='compute_checklists')
    # onhold_checklist = fields.Integer('Failed Checklist', compute='compute_checklists')
    tempcheck_id = fields.Many2one('fleet.checklist.template', 'Checklist Template')

    def add_checklists(self):

        for service in self:
            if service.tempcheck_id:
                print("1111111111111111111111111111111111111111111111111111111111111111111111111111")
                for checklist in service.tempcheck_id.checklist_ids:
                    print("222222222222222222222222222222222222222222222222222222222222222222222")
                    print(service.tempcheck_id.checklist_ids)
                    vals=[]
                    for check in checklist.checklist:
                        val = (0, 0, {
                            'name' : check.name.id,
                            'qty':0,
                            'red':False,
                            'green':False,
                            'yellow':False,
                            'checkk_id':checklist.id

                        })
                        vals.append(val)
                        print(vals)

                    service.checklist_ids.create({
                        'checklist_id': checklist.id,
                        'checklist':vals,
                        'service_id': service.id,
                        'image':checklist.image,

                        # 'qty':0,
                        # 'red':False,
                        # 'green':False,
                        # 'yellow':False,

                    })
                    print(service.checklist_ids.checklist)


    # def compute_checklists(self):
    #     for partner in self:
    #         partner.total_checklist = len(partner.checklist_ids)
    #         inprogress_checklist = 0
    #         onhold_checklist = 0
    #         completed_checklist = 0
    #         for checklist in partner.checklist_ids:
    #             if checklist.statee == 'process':
    #                 inprogress_checklist += 1
    #             if checklist.statee == 'block':
    #                 onhold_checklist += 1
    #             if checklist.statee == 'done':
    #                 completed_checklist += 1
    #         partner.completed_checklist = completed_checklist
    #         partner.inprogress_checklist = inprogress_checklist
    #         partner.onhold_checklist = onhold_checklist
