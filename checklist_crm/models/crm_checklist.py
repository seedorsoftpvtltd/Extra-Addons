from odoo import api, fields, models, tools, _

class CrmChecklistTemplate(models.Model):
    _name = 'crm.checklist.template'
    _description = 'Checklist Template'

    name = fields.Char(required=True)
    code = fields.Char(string='Reference', required=True)
    note = fields.Text(string='Description')
    checklist_ids = fields.Many2many('checklist.points', 'checklist_points_template_rel', 'template_id', 'checklist_id', string='Checklists')
    company_id = fields.Many2one('res.company', string='Company', required=True,
        copy=False, default=lambda self: self.env['res.company']._company_default_get())

class ChecklistPoints(models.Model):
    _name = 'checklist.points'
    _description = 'Checklist Points'

    name = fields.Char(string='Checklist', required=True)
    description = fields.Text(string='Description', required=True)
    instruction = fields.Html('Instructions')
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
        copy=False, default=lambda self: self.env['res.company']._company_default_get())

class CustomerChecklist(models.Model):
    _name = 'crm.checklist'
    _description = 'CRM Checklist'

    name = fields.Char(string='Name', required=True, related='checklist_id.name')
    description = fields.Text(string='Description', required=True, related='checklist_id.description')
    lead_id = fields.Many2one('crm.lead', 'Partner')
    checklist_id = fields.Many2one('checklist.points', 'Checklist')
    state = fields.Selection([
        ('new', 'Not started yet'),
        ('process', 'In Progress'),
        ('block', 'Failed'),
        ('done', 'Completed')], string='Status', default='new',)
    instruction = fields.Html('Instructions', related='checklist_id.instruction')
    reason = fields.Text('User Description')
    company_id = fields.Many2one('res.company', string='Company', required=True,
        copy=False, default=lambda self: self.env['res.company']._company_default_get())

    def confirm_checklist(self):
        self.write({'state':'process'})

    def mark_as_done(self):
        self.write({'state':'done'})

    def mark_as_hold(self):
        self.write({'state':'block'})

class CRMLead(models.Model):
    _inherit = 'crm.lead'

    checklist_ids = fields.One2many('crm.checklist', 'lead_id', 'Checklists')
    total_checklist = fields.Float('Total Checklist', compute='compute_checklists')
    completed_checklist = fields.Integer('Completed Checklist', compute='compute_checklists')
    inprogress_checklist = fields.Integer('In-progress Checklist', compute='compute_checklists')
    onhold_checklist = fields.Integer('Failed Checklist', compute='compute_checklists')
    template_id = fields.Many2one('crm.checklist.template', 'Checklist Template')

    def add_checklists(self):
        for lead in self:
            if lead.template_id:
                for checklist in lead.template_id.checklist_ids:
                    lead.checklist_ids.create({'name': checklist.name,
                                                 'description': checklist.description,
                                                 'lead_id': lead.id,
                                                 'checklist_id': checklist.id,
                                                 'instruction': checklist.instruction,
                                                 })

    def compute_checklists(self):
        for partner in self:
            partner.total_checklist = len(partner.checklist_ids)
            inprogress_checklist = 0
            onhold_checklist = 0
            completed_checklist = 0
            for checklist in partner.checklist_ids:
                if checklist.state == 'process':
                    inprogress_checklist+=1
                if checklist.state == 'block':
                    onhold_checklist+=1
                if checklist.state == 'done':
                    completed_checklist+=1
            partner.completed_checklist=completed_checklist
            partner.inprogress_checklist=inprogress_checklist
            partner.onhold_checklist=onhold_checklist