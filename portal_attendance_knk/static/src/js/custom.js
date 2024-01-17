odoo.define('portal_attendance_knk.custom', function(require) {
"use strict";
    var sAnimations = require('website.content.snippets.animation');

    sAnimations.registry.HrAttendances = sAnimations.Class.extend({
        selector: '.portal_attendance_knk',
        events: {
            'click .o_hr_attendance_sign_in_out_icon': '_update_attendance',
        },
        _update_attendance: function (ev) {
            var self = this;
            const employee_id = $(ev.currentTarget).data('id');
            this._rpc({
                    model: 'hr.employee',
                    method: 'attendance_manual',
                    args: [[employee_id], 'hr_attendance.hr_attendance_action_my_attendances'],
                })
                .then(function(result) {
                    if (result.action) {
                        self.do_action(result.action);
                    } else if (result.warning) {
                        self.do_warn(result.warning);
                    }
                    window.location.reload();
                });
        },
    });
});