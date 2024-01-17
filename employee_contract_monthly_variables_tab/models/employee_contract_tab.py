from odoo import models, fields, api, _


class Contract(models.Model):
	_inherit = 'hr.contract'

	local_leaves = fields.Float(string="Local Leaves", store=True, copy=True)
	sick_leaves = fields.Float(string="Sick Leave", store=True, copy=True)
	working_days = fields.Float(string="Working Days", store=True, copy=True)
	absent_days = fields.Float(string="Absent Days", store=True, copy=True)
	days_pay = fields.Float(string="Days to Pay", store=True, copy=True, compute="_compute_daystopay")
	bonus = fields.Monetary(string="Bonus", store=True, copy=True)
	ot_worked_hours = fields.Float(string="OT Worked Hours", store=True, copy=True)
	normal_ot_paid = fields.Monetary(string="Normal OT Paid", store=True, readonly=True, compute="_compute_normalotpaid")

	sundays = fields.Float(string="Sundays", store=True, copy=True)
	sunday_paid = fields.Monetary(string="Sunday Paid", store=True, readonly=True, compute="_compute_sundaypaid")
	ph_hours = fields.Float(string="PH Hours", store=True, copy=True)
	ph = fields.Monetary(string="PH", store=True, readonly=True, compute="_compute_ph")
	cyclone_hours = fields.Float(string="Cyclone Hours", store=True, copy=True)
	cyclone = fields.Monetary(string="Cyclone", store=True, readonly=True, compute="_compute_cyclone")
	early_leaving_hours = fields.Float(string="Early Leaving Hours", store=True, copy=True)
	early_leave_deduction = fields.Monetary(string="Early Leave Deduction", store=True, readonly=True, compute="_compute_early_leave_deduction")
	absence = fields.Float(string="Absence", store=True, copy=True)
	absence_deduction = fields.Monetary(string="Absences Deduction", store=True, readonly=True, compute="_compute_absence_deduction")

	ctc = fields.Monetary(string="CTC", store=True, copy=True)
	rate_per_hour = fields.Monetary(string="Rate Per Hour", store=True, copy=True)
	rate_per_day = fields.Monetary(string="Rate per day", store=True, copy=True)
	uniform_allow = fields.Monetary(string="TEWF", store=True, copy=True)


	@api.depends('working_days', 'absent_days')
	def _compute_daystopay(self):
		for record in self:
			record.days_pay = record.working_days - record.absent_days

	@api.depends('rate_per_hour', 'ot_worked_hours')
	def _compute_normalotpaid(self):
		for record in self:
			record.normal_ot_paid = record.rate_per_hour * record.ot_worked_hours * 1.5


	@api.depends('rate_per_hour', 'sundays')
	def _compute_sundaypaid(self):
		for record in self:
			record.sunday_paid = record.rate_per_hour * record.sundays * 2.0

	@api.depends('rate_per_hour', 'ph_hours')
	def _compute_ph(self):
		for record in self:
			record.ph = record.rate_per_hour * record.ph_hours * 2.0

	@api.depends('rate_per_hour', 'cyclone_hours')
	def _compute_cyclone(self):
		for record in self:
			record.cyclone = record.rate_per_hour * record.cyclone_hours * 2.0

	@api.depends('rate_per_hour', 'early_leaving_hours')
	def _compute_early_leave_deduction(self):
		for record in self:
			record.early_leave_deduction = record.rate_per_hour * record.early_leaving_hours

	@api.depends('rate_per_hour', 'absence')
	def _compute_absence_deduction(self):
		for record in self:
			record.absence_deduction = record.rate_per_hour * record.absence
