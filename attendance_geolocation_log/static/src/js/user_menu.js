odoo.define("attendance_geolocation_log.user_menu", function (require) {
    "use strict";

    var UserMenu = require("web.UserMenu");
    var session = require("web.session");

    UserMenu.include({
        _onMenuGeolocation: function() {
            var self = this;
            this.trigger_up("clear_uncommitted_changes", {
                callback: function() {
                    self._rpc({
                        route: "/web/action/load", 
                        params: { 
                            action_id: "attendance_geolocation_log.action_simple_attendance_geolocation_log"
                        }
                    }).then(function(result) {
                        result.res_id = session.uid;
                        self.do_action(result);
                    });
                },
            });
        },
    });

});