odoo.define('schedule_send_mail.schedule_send_mail', function (require) {
"use strict";

var Activity = require('mail.Activity');
var AttachmentBox = require('mail.AttachmentBox');
var ChatterComposer = require('mail.composer.Chatter');
var Dialog = require('web.Dialog');
var Followers = require('mail.Followers');
var ThreadField = require('mail.ThreadField');
var mailUtils = require('mail.utils');

var concurrency = require('web.concurrency');
var config = require('web.config');
var core = require('web.core');
var Widget = require('web.Widget');
var chatter = require('mail.Chatter');

var _t = core._t;
var QWeb = core.qweb;

    chatter.include({
        events: _.extend(chatter.prototype.events, {
            'click .o_chatter_button_schedule_send_message': '_onScheduleMessage',
        }),

        _onScheduleMessage: function () {
            this.scheduleActivity();
        },

        scheduleActivity: function (id, callback) {
            var action = {

                type: 'ir.actions.act_window',
                res_model: 'schedule.send.message',
                view_mode: 'form',
                views: [[false, 'form']],
                target: 'new',
                context: this.context,
                res_id: id || false,
            };
            return this.do_action(action, { on_close: callback });
        },

    });

// -----------------------------------------------------------------------------
// Activities Widget for Form views ('mail_activity' widget)
// -----------------------------------------------------------------------------

});