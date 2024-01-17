odoo.define('attendance_geolocation_log.kiosk_confirm', function (require) {
    "use strict";
    
    var KioskConfirm = require('hr_attendance.kiosk_confirm');
    var session = require("web.session");
    var core = require('web.core');
    var _t = core._t;

    KioskConfirm.include({
        events: _.extend(KioskConfirm.prototype.events, {
            "click .o_hr_attendance_sign_in_out_icon":  _.debounce(function() {
                var self = this;
                self.update_attendance();
            }, 200, true),
            "click .o_hr_attendance_pin_pad_button_ok": _.debounce(function() {
                var self = this;
                self.pin_pad = true;
                self.update_attendance();
            }, 200, true),
        }),

        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.pin_pad = false;
        },

        update_attendance: function () {
            var self = this;
            if(session.log_attendance_geolocation){
                var geolocation= navigator.geolocation;
                if (window.location.protocol == 'https:'){                    
                    if (geolocation) {
                        geolocation.getCurrentPosition(self._manual_attendance.bind(self), self._getCurrentPositionErr, {
                            enableHighAccuracy: true,
                            timeout: 5000,
                            maximumAge: 0
                        });
                    }
                }else{
                    self.do_notify(false, _t("GEOLOCATION API MAY ONLY WORKS WITH HTTPS CONNECTIONS."));
                }
            }else{
                this._rpc({
                    model: 'hr.employee',
                    method: 'attendance_manual',
                    args: [[this.employee_id], this.next_action],
                })
                .then(function(result) {
                    if (result.action) {
                        self.do_action(result.action);
                    } else if (result.warning) {
                        self.do_warn(result.warning);
                    }
                });
            }
        },

        _manual_attendance: function (position) {
            var self = this;
            if (this.pin_pad) {
                this.$('.o_hr_attendance_pin_pad_button_ok').attr("disabled", "disabled");
            }

            self._rpc({
                model: 'hr.employee',
                method: 'attendance_manual',
                args: [[this.employee_id], this.next_action, this.$('.o_hr_attendance_PINbox').val(), [position.coords.latitude, position.coords.longitude]],
            })
            .then(function(r) {
                if (r.action) {
                    self.do_action(r.action);
                } else if (r.warning) {
                    self.do_warn(r.warning);
                    if (self.pin_pad) {
                        self.$('.o_hr_attendance_PINbox').val('');
                        setTimeout( function() {
                            self.$('.o_hr_attendance_pin_pad_button_ok').removeAttr("disabled");
                        }, 500);
                    }
                    self.pin_pad = false;
                }
            });

        },
        _getCurrentPositionErr: function(err){
            switch(err.code) {
                case err.PERMISSION_DENIED:
                  console.log("The request for geolocation was refused by the user.");
                  break;
                case err.POSITION_UNAVAILABLE:
                    console.log("There is no information about the location available.");
                  break;
                case err.TIMEOUT:
                    console.log("The request for the user's location was unsuccessful.");
                  break;
                case err.UNKNOWN_ERROR:
                    console.log("An unidentified error has occurred.");
                  break;
              }
        }

    })

})