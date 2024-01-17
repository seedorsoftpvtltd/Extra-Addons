from odoo import api, fields, models


class ProjectF(models.Model):
    _inherit = "project.team.custom"
    project_id = fields.Many2one('project.project', store=True)


class ProjectTeams(models.Model):
    _inherit = "project.project"
    project_teams_count = fields.Integer('Project Teams', compute='_compute_teams_count')

    def _compute_teams_count(self):
        obj = self.env['project.team.custom']
        for rec in self:
            count = obj.search_count([('project_manager_id', '!=', False)])
            if count != 0:
                rec['project_teams_count'] = count
            else:
                rec['project_teams_count'] = 0
