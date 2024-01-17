odoo.define('rt_activity_alarm.systray.activity_reminder', function (require) {
"use strict";

var core = require('web.core');
var session = require('web.session');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');
var QWeb = core.qweb;

var _t = core._t;
var time = require('web.time');


/**
 * Menu item appended in the systray part of the navbar, redirects to the next
 * activities of all app
 */
var rt_activity_alarm_activity_reminder = Widget.extend({
    name: 'rt_activity_alarm_activity_reminder',
    template:'rt_activity_alarm.systray.activity_reminder',
    events: {
        'click .js_cls_mail_activity_action': '_onActivityActionClick',
        'click .js_cls_activity_alarm_open_single_model_record': '_onOpenSingleModelRecordClick',
        'click .js_cls_activity_alarm_edit_schedule_activity': '_onClickScheduleActivity',
        'show.bs.dropdown': '_onActivityMenuShow',
        'hide.bs.dropdown': '_onActivityMenuHide',
    },


    start: function () {
		this._list_times = [];
        this._$activitiesPreview = this.$('.o_mail_systray_dropdown_items');
        //Component.env.bus.on('activity_updated', this, this._updateCounter);
        this.call('mail_service', 'getMailBus').on('activity_updated', this, this._updateCounter);
        
		this._updateCounter();
        this._updateActivityPreview();
        this.setInterval = setInterval(this._setAlarm.bind(this), 60000);
        return this._super(...arguments);
    },

    /**
	 * Set Alarm
     * @private
     */
    _setAlarm: function () {
        var self = this;
		if (!self._list_times.length && !self._activities.length){
			return;
		}
				
        var ut = new Date();
        var h = ut.getUTCHours();
        var m = ut.getUTCMinutes();
		var	utc_time_hour_minute = h + ':' + m;
		var time_matching_index = self._list_times.indexOf(utc_time_hour_minute);
		if ( time_matching_index >= 0){
			//Matching Value.
			var find_activity_item = self._list_times[time_matching_index];
            self._activities.map(function (el) {
				if (el.utc_time_hour_minute == find_activity_item){
					// send notification.

					
	                var message = _.str.sprintf(
                    _t("%s - %s - %s<br/><b>%s - %s</b><br/>Due on %s<br/>Created %s<br/>Assigned to %s"),
	                    _.escape(el.res_model_name),
						_.escape(el.activity_type_name),
						_.escape(el.label_delay),
						
						_.escape(el.summary),
						_.escape(el.user_time_hour_minute),
						
						_.escape(el.date_deadline),
						_.escape(el.user_tz_create_date),
						_.escape(el.user_id_name)											
	                );	

                    self.displayNotification({
                        title: _t("Activity Reminder"),
           				message: message,
                        type: 'info',
                    });
				
/*					Component.env.services['notification'].notify({
                    	message: message,
						title: _t("Activity Reminder"),
                    	type: 'info',
                    });*/
					// send notification.
					
				}
			});					
		}

    },

    /**
     * @override
     */
    destroy: function () {
        clearInterval(this.setInterval);
        this._super(...arguments);
    },
    //--------------------------------------------------
    // Private
    //--------------------------------------------------
    /**
     * Make RPC and get current user's activity details
     * @private
     */
    _getActivityData: function () {
        var self = this;

        return self._rpc({
            model: 'res.users',
            method: 'rt_activity_alarm_systray_get_reminder_activities',
            args: [],
            kwargs: {context: session.user_context},
        }).then(function (data) {
            self._activities = data.list_activities_dic;	
            self._list_times = data.list_times;	
            self.activityCounter = data.list_activities_dic.length || 0;
            self.$('.o_notification_counter').text(self.activityCounter);
            self.$el.toggleClass('o_no_notification', !self.activityCounter);


    var today = moment().startOf('day');
        var dateFormat =  time.getLangDateFormat();
        var datetimeFormat = time.getLangDatetimeFormat();	

    _.each(self._activities, function (activity){
        var toDisplay = '';   
		var date_deadline =  moment(activity.date_deadline); 
	
		   
		var diff = date_deadline.diff(today, 'days', true); // true means no rounding
        if (diff === 0){
            toDisplay = _t("Today");
        } else {
            if (diff < 0){ // overdue
                if (diff === -1){
                    toDisplay = _t("Yesterday");
                } else {
                    toDisplay = _.str.sprintf(_t("%d days overdue"), Math.abs(diff));
                }
            } else { // due
                if (diff === 1){
                    toDisplay = _t("Tomorrow");
                } else {
                    toDisplay = _.str.sprintf(_t("Due in %d days"), Math.abs(diff));
                }
            }
        }
        activity.label_delay = toDisplay;
		activity.date_deadline = moment(activity.date_deadline).format(dateFormat);
		activity.user_tz_create_date = moment(activity.user_tz_create_date).format(datetimeFormat);	
		activity.user_tz_reminder_datetime = moment(activity.user_tz_reminder_datetime).format(datetimeFormat);				
    });


        });
    },
    /**
     * Get particular model view to redirect on click of activity scheduled on that model.
     * @private
     * @param {string} model
     */
    _getActivityModelViewID: function (model) {
        return this._rpc({
            model: model,
            method: 'get_activity_view_id'
        });
    },
    /**
     * Return views to display when coming from systray depending on the model.
     *
     * @private
     * @param {string} model
     * @returns {Array[]} output the list of views to display.
     */
    _getViewsList(model) {
        return [[false, 'kanban'], [false, 'list'], [false, 'form']];
    },
    /**
     * Update(render) activity system tray view on activity updation.
     * @private
     */
    _updateActivityPreview: function () {
        var self = this;
        self._getActivityData().then(function (){
            self._$activitiesPreview.html(QWeb.render('rt_activity_alarm.systray.activity_reminder.previews', {
                widget: self
            }));
        });
    },



    /**
     * update counter based on activity status(created or Done)
     * @private
     * @param {Object} [data] key, value to decide activity created or deleted
     * @param {String} [data.type] notification type
     * @param {Boolean} [data.activity_deleted] when activity deleted
     * @param {Boolean} [data.activity_created] when activity created
     */
    _updateCounter: function (data) {

		if (data) {
            if (data.activity_created || data.activity_deleted || data.rt_activity_alarm_reminder_datetime_updated) {
               this._updateActivityPreview();
            }
        }
        
    },

    //------------------------------------------------------------
    // Handlers
    //------------------------------------------------------------

    /**
     * Redirect to specific action given its xml id or to the activity
     * view of the current model if no xml id is provided
     *
     * @private
     * @param {MouseEvent} ev
     */
    _onActivityActionClick: function (ev) {
		var self=this;
		ev.preventDefault();        
		//ev.stopPropagation();
        this.$('.dropdown-toggle').dropdown('toggle');
        var targetAction = $(ev.currentTarget);
        var actionXmlid = targetAction.data('action_xmlid');
        if (actionXmlid) {
            this.do_action(actionXmlid);
        } else {
            var domain = [['activity_ids.user_id', '=', session.uid]]
            if (targetAction.data('domain')) {
                domain = domain.concat(targetAction.data('domain'))
            }
        	if (targetAction.data('activity_id')){
			var record_domain = [['activity_ids','in',[targetAction.data('activity_id')] ]]
            domain = domain.concat(record_domain)
        	}
            
            this.do_action({
                type: 'ir.actions.act_window',
                name: targetAction.data('model_name'),
                views: [[false, 'activity'], [false, 'kanban'], [false, 'list'], [false, 'form']],
                view_mode: 'activity',
                res_model: targetAction.data('res_model'),
                domain: domain,
            }, {
                clear_breadcrumbs: true,
            });
        }
    },

    /**
     * Redirect to particular model Record view
     * @private
     * @param {MouseEvent} event
     */
    _onOpenSingleModelRecordClick: function (event) {
		var self=this;
		event.preventDefault();

        // fetch the data from the button otherwise fetch the ones from the parent (.o_mail_preview).
        var data = $(event.currentTarget).data();
        var context = {};
/*        if (data.filter === 'my') {
            context['search_default_activities_overdue'] = 1;
            context['search_default_activities_today'] = 1;
        } else {
            context['search_default_activities_' + data.filter] = 1;
        }*/
        // Necessary because activity_ids of mail.activity.mixin has auto_join
        // So, duplicates are faking the count and "Load more" doesn't show up
        context['force_search_count'] = 1;
        
        var domain = [['activity_ids.user_id', '=', session.uid]]
        if (data.domain) {
            domain = domain.concat(data.domain)
        }

        if (data.res_id) {
			var record_domain = [['id','=',data.res_id]]
            domain = domain.concat(record_domain)
        }
        	
        self.do_action({
            type: 'ir.actions.act_window',
            name: data.model_name,
            res_model:  data.res_model,
            views: this._getViewsList(data.res_model),
            search_view_id: [false],
            domain: domain,
            context:context,
        }, {
            clear_breadcrumbs: true,
        });
    },




    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onClickScheduleActivity(ev) {

		var self=this;
		ev.preventDefault();        
        var targetAction = $(ev.currentTarget);
	
    	if (!targetAction.data('activity_id')){
			return;
    	}
	
	
        var action = {
            type: 'ir.actions.act_window',
            name: _t("Schedule Activity"),
            res_model: 'mail.activity',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new',
/*            context: {
                default_res_id: this.res_id,
                default_res_model: this.model,
            },*/
            res_id: targetAction.data('activity_id'),
        };
        self.do_action(action);
    },



    /**
     * @private
     */
    _onActivityMenuShow: function () {
        document.body.classList.add('modal-open');
         this._updateActivityPreview();
    },
    /**
     * @private
     */
    _onActivityMenuHide: function () {
        document.body.classList.remove('modal-open');
    },
});

SystrayMenu.Items.push(rt_activity_alarm_activity_reminder);

return rt_activity_alarm_activity_reminder;

});
