odoo.define('attendance_geolocation_log.my_attendances', function (require) {
    "use strict";
    
    var MyAttendances = require('hr_attendance.my_attendances');
    var session = require("web.session");
    var core = require('web.core');
    var _t = core._t;

    MyAttendances.include({
        init: function (parent, action) {
            this._super.apply(this, arguments);
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
                self._super();
            }            
        },
        _manual_attendance: function (position) {
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'attendance_manual',
                args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances', null, [position.coords.latitude, position.coords.longitude]],
            })
            .then(function(result) {
                if (result.action) {
                    self.do_action(result.action);
                } else if (result.warning) {
                    self.do_warn(result.warning);
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
    });


});