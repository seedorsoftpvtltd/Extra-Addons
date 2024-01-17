# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class HolidaysType(models.Model):

    _inherit = 'hr.leave.type'

    carry_fwd = fields.Boolean('Carry Foward?')
    cf_leaves = fields.Float('Carry Forward Leaves')

    def lapse_leaves(self):
        """
        This method is used to lapse the leaves \
        which are more than what can be carry forwarded.
        """
        emp_obj = self.env['hr.employee']
        leave_obj = self.env['hr.leave']
        emps = emp_obj.search([])
        for leave_type in self:
            # Need to check all the employees for their remaining leaves
            for emp in emps:
                lapse_leave = False
                leaves_dict = leave_type.get_days(emp.id)
                leaves_to_lapse = leaves_dict[leave_type.id].get(
                    'remaining_leaves', 0.0)
                # If Carry Forward of leaves to be done.
                if leave_type.carry_fwd:
                    if leaves_to_lapse > leave_type.cf_leaves:
                        leaves_to_lapse -= leave_type.cf_leaves
                        lapse_leave = True
                    else:
                        lapse_leave = False
                else:
                    lapse_leave = True
                # Creating the Leaves to Lapse
                if lapse_leave:
                    vals = {
                        'employee_id': emp.id,
                        'holiday_status_id': leave_type.id,
                        'number_of_days': leaves_to_lapse,
                        'name': 'Lapse Leaves for : ' + emp.name,
                        'request_date_from': False,
                        'request_date_to': False,
                        'lapse': True
                    }
                    leave = leave_obj.create(vals)
                    # Approve Leave for Employee
                    leave.action_approve()
                    # Validate Leave for Employee
                    if leave.holiday_status_id.validation_type == 'both':
                        leave.action_validate()

    @api.model
    def _auto_lapse_leaves(self):
        """
        This is a scheduler method to lapse the leaves \
        which are more than what can be carry forwarded.
        ----------------------------------------------------------------------------
        @param self: object pointer
        """
        # Search for leave types which have carry forward configuration
        leave_types = self.search([('carry_fwd', '=', True), ('cf_leaves', '>', 0)])
        # Lapse Leaves
        leave_types.lapse_leaves()


class HolidayRequest(models.Model):
    _inherit = 'hr.leave'

    lapse = fields.Boolean('Lapse')

    @api.constrains('date_from', 'date_to', 'state', 'employee_id')
    def _check_date(self):
        for holiday in self.filtered('employee_id'):
            if not holiday.lapse:
                domain = [
                    ('date_from', '<', holiday.date_to),
                    ('date_to', '>', holiday.date_from),
                    ('employee_id', '=', holiday.employee_id.id),
                    ('id', '!=', holiday.id),
                    ('state', 'not in', ['cancel', 'refuse']),
                ]
                nholidays = self.search_count(domain)
                if nholidays:
                    raise ValidationError(
                        _('You can not set 2 times off that \
                        overlaps on the same day for the same employee.'))

    def action_validate(self):
        """
        Inherited Action Validate method to \
        delete the calendar event for lapse leaves
        ------------------------------------------------------------------------------
        @param self: object pointer
        """
        res = super(HolidayRequest, self).action_validate()
        for rec in self:
            if rec.lapse and rec.holiday_status_id.create_calendar_meeting and rec.meeting_id:
                rec.meeting_id.unlink()
        return res

