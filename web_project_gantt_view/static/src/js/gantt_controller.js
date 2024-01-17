odoo.define('web_project_gantt_view.GanttController', function (require) {
    "use strict";

    var AbstractController = require('web.AbstractController');
    var core = require('web.core');
    var config = require('web.config');
    var Dialog = require('web.Dialog');
    var dialogs = require('web.view_dialogs');
    var time = require('web.time');
    var session = require('web.session');

    var _t = core._t;
    var qweb = core.qweb;

    var n_direction = false;

    var GanttController = AbstractController.extend({
        events: {
            'click .gantt_task_row .gantt_task_cell': '_onCreateClick',            
            'click .o_gantt_scale_button': '_onScaleClick',
            'click .o_gantt_new_button': '_onNewClick',
            'click .o_gantt_today_button': '_onTodayClick',
            'click .o_gantt_left_button': '_onPreviousClick',
            'click .o_gantt_right_button': '_onNextClick',
            'click .o_gantt_sort_button': '_onSortClick',        
            'click .o_gantt_export_pdf': '_onExportPDFClick',
            'click .o_gantt_export_png': '_onExportPNGClick',
        },
        custom_events: _.extend({}, AbstractController.prototype.custom_events, {
            task_update: '_onTaskUpdate',
            task_display: '_onTaskDisplay',
            task_create: '_onTaskCreate',
            crate_link: '_onCreateLink',
            delete_link: '_onDeleteLink',
        }),

        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);     
            this.set('title', params.displayName);   
            this.context = params.context;
            this.displayName = params.displayName;
            this.dateStartField = params.dateStartField;
            this.dateStopField = params.dateStopField;
            this.linkModel = params.linkModel;
        },

        getTitle: function () {
            return this.get('title');
        },

        renderButtons: function ($node) {
            var self = this;
            this.$buttons = $(qweb.render("WebGanttView.buttons", {'isMobile': config.device.isMobile}));
            if ($node) {
                this.$buttons.appendTo($node);
            }
        },  

        _onScaleClick: function(event){
            var self = this;
            self.$buttons.find('.o_gantt_scale_dropdown_button').text($(this).text());
            self.$buttons.find('.o_gantt_scale_button').removeClass('active');
            var scale = $(event.target).data('value');
            self._updateButtons(scale);
            return self._setScale($(event.target).data('value'));
        },
        
        _updateButtons: function(scale){
            var self = this;
            if (!self.$buttons) {
                return;
            }
            self.$buttons.find('.o_gantt_scale_button[data-value="' + scale + '"]').addClass('active');
        },

        _onTodayClick: function(){
            var self = this;
            self.model.setFocusDate(moment(new Date()));
            return self.reload();
        },

        _onPreviousClick: function(){
            var self = this;
            var state = self.model.get();
            self._setFocusDate(state.focus_date.subtract(1, state.scale));
        },
        _onNextClick: function(){
            var self = this;
            var state = self.model.get();
            self._setFocusDate(state.focus_date.add(1, state.scale));
        },

        _setScale: function (scale) {
            var self = this;
            this.model.setScale(scale);
            self.set('title', self.displayName + ' (' + self.model.get().date_display + ')');
            this.reload();
        },

        _onCreateClick: function (event) {
            if (this.activeActions.create) {
                
                var context = _.clone(this.context);
                var id = event.target.parentElement.attributes.task_id.value;
                var task = gantt.getTask(id);
                var classDate = _.find(event.target.classList, function (e) {
                    return e.indexOf("date_") > -1;
                });
                
                var startDate = moment(new Date(parseInt(classDate.split("_")[1], 10))).utc();
                var endDate;
                switch (this.model.get().scale) {
                    case "day":
                        endDate = startDate.clone().add(4, "hour");
                        break;
                    case "week":
                        endDate = startDate.clone().add(2, "day");
                        break;
                    case "month":
                        endDate = startDate.clone().add(4, "day");
                        break;
                    case "year":
                        endDate = startDate.clone().add(2, "month");
                        break;
                }
                
                var get_create = function (item) {
                    if (item.create) {
                        context["default_"+item.create[0]] = item.create[1][0];
                    }
                    if (item.parent) {
                        var parent = gantt.getTask(item.parent);
                        get_create(parent);
                    }
                };
                get_create(task);

                context["default_"+this.dateStartField] = startDate.format("YYYY-MM-DD HH:mm:ss");
                if (this.dateStopField) {
                    context["default_"+this.dateStopField] = endDate.format("YYYY-MM-DD HH:mm:ss");
                } 
                else {
                    context["default_"+this.model.mapping.date_delay] = gantt.calculateDuration(startDate, endDate);
                }

                context.id = 0;

                new dialogs.FormViewDialog(this, {
                    res_model: this.modelName,
                    context: context,
                    on_saved: this.reload.bind(this),
                }).open();  
            }
        },

        _onTaskUpdate: function (event) {
            var taskObj = event.data.task;
            var success = event.data.success;
            var fail = event.data.fail;
            var fields = this.model.fields;
            
            if (fields[this.dateStopField] === undefined) {
                    Dialog.alert(this, _t('You have no date_stop field defined!'));
                return fail();
            }

            if (fields[this.dateStartField].readonly || fields[this.dateStopField].readonly) {
                Dialog.alert(this, _t('You are trying to write on a read-only field!'));
                return fail();
            }

            var start = taskObj.start_date;
            var end = taskObj.end_date;
            
            var data = {};
            data[this.dateStartField] = time.auto_date_to_str(start, fields[this.dateStartField].type);
            if (this.dateStopField) {
                var field_type = fields[this.dateStopField].type;
                if (field_type === 'date') {
                    end.setTime(end.getTime() - 86400000);
                    data[this.dateStopField] = time.auto_date_to_str(end, field_type);
                    end.setTime(end.getTime() + 86400000);
                } else {
                    data[this.dateStopField] = time.auto_date_to_str(end, field_type);
                }
            } 
            
            var taskId = parseInt(taskObj.id.split("gantt_task_").slice(1)[0], 10);

            this._rpc({
                model: this.model.modelName,
                method: 'write',
                args: [taskId, data],
            })
            .then(success, fail);
        },

        _onTaskCreate: function () {
            if (this.activeActions.create) {
                var startDate = moment(new Date()).utc();
                this._createTask(0, startDate);
            }
        },
        
        _onCreateLink: function (item) {
            var linkObj = item.data.link;
            var success = item.data.success;
            var fail = item.data.fail;

            var linkSourceId = parseInt(linkObj.source.split("gantt_task_").slice(1)[0], 10);
            var linkTargetId = parseInt(linkObj.target.split("gantt_task_").slice(1)[0], 10);
            var linkType = linkObj.type || 0;

            var args = [{
                'task_id' : linkSourceId,
                'target_task_id' : linkTargetId,
                'link_type' : linkType,
            }];
            
            return this._rpc({
                model: this.linkModel,
                method: 'create',
                args: args,
            }).then(success, fail);
        },

        _onDeleteLink: function (item) {
            var linkObj = item.data.link;
            var success = item.data.success;
            var fail = item.data.fail;

            var Id = parseInt(linkObj.id.split("gantt_link_").slice(1)[0], 10);
            
            return this._rpc({
                model: this.linkModel,
                method: 'unlink',
                args: [Id],
            }).then(success, fail);
        },

        _onTaskDisplay: function (event) {
            var readonly = !this.activeActions.edit;
            this._displayTask(event.data, readonly);
        },

        _displayTask: function (task, readonly) {
            var taskId = _.isString(task.id) ? parseInt(_.last(task.id.split("_")), 10) : task.id;
            readonly = readonly ? readonly : false;
            new dialogs.FormViewDialog(this, {
                res_model: this.modelName,
                res_id: taskId,
                context: session.user_context,
                on_saved: this.reload.bind(this),
                readonly: readonly
            }).open();  
        },
    
        _setFocusDate: function (focusDate) {
            var self = this;
            this.model.setFocusDate(focusDate);
            self.set('title', self.displayName + ' (' + self.model.get().date_display + ')');
            this.reload();
        },

        _onNewClick: function (event) {
            var context = _.clone(this.context);
            var startDate = moment(new Date()).utc();
            var endDate;
            switch (this.model.get().scale) {
                case "day":
                    endDate = startDate.clone().add(4, "hour");
                    break;
                case "week":
                    endDate = startDate.clone().add(2, "day");
                    break;
                case "month":
                    endDate = startDate.clone().add(4, "day");
                    break;
                case "year":
                    endDate = startDate.clone().add(2, "month");
                    break;
            }
            
            context["default_"+ this.dateStartField] = startDate.format("YYYY-MM-DD HH:mm:ss");
            if (this.dateStopField) {
                context["default_"+ this.dateStopField] = endDate.format("YYYY-MM-DD HH:mm:ss");
            } 

            new dialogs.FormViewDialog(this, {
                res_model: this.modelName,
                context: context,
                on_saved: this.reload.bind(this),
            }).open();
        },
        
        _onSortClick: _.debounce(function(event){
            event.preventDefault();        
            if (n_direction){
                gantt.sort("id",false);
            } 
            else {
                gantt.sort("id",true);
            }
            n_direction = !n_direction;
        }, 200, true),

        _onExportPNGClick: _.debounce(function(event){
            event.preventDefault();
            gantt.exportToPNG();   
        }, 200, true),

        _onExportPDFClick: _.debounce(function(event){
            event.preventDefault();   
            gantt.exportToPDF();        
        }, 200, true),
    });
    return GanttController;
});
