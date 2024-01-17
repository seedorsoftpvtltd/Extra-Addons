odoo.define('chatter_message_visibility.form_renderer', function (require) {
"use strict";
var core = require('web.core');
var session = require('web.session')
var _t = core._t;
var rpc = require('web.rpc');
var FormRenderer = require('web.FormRenderer');
var DocumentThread = require('mail.model.DocumentThread');
var BasicModel = require('web.BasicModel');

	BasicModel.include({
		_fetchSpecialActivity: function (record, fieldName) {
			session.user_context.chatter_model = record.model
	    	session.user_context.chatter_res_id = record.res_id
			return this._super.apply(this,arguments);
		},
	});

	FormRenderer.include({
		_renderNode: function (node) {
			var self = this;
			if (node.tag === 'div' && node.attrs.class === 'oe_chatter') {
				this.chatter = false;
				return this._super.apply(this,arguments);
			}
			else{
				return this._super.apply(this,arguments);
			}
		},
	});

	DocumentThread.include({
		_fetchMessages: function (options) {
			var self = this;
			session.user_context.chatter_model = 	this._documentModel
			session.user_context.chatter_res_id = this._documentID
			var self = this;
			return this._fetchMessageIDs().then(function () {
				var messageIDs = self._messageIDs;
				return self._rpc({
					model: 'mail.message',
					method: 'message_format',
					args: [messageIDs],
					context: session.user_context,
				}).then(function (messagesData) {
					self._messages = [];
					_.each(messagesData, function (messageData) {
						self.call('mail_service', 'addMessage', messageData, { silent: true });
					});
				});
			});
		},
	});

	FormRenderer.include({
		events: _.extend({}, FormRenderer.prototype.events, {
			"click input#lognote_chatter": "_onChangeLogNoteChatter",
			"click input#message_chatter": "_onChangeMessageChatter",
			"click input#activity_chatter": "_onChangeActivityChatter",
	    }),

		_hide_tabs : function(){
			var self = this;
			if (!$(self.$el.find('.o_thread_composer')).hasClass("o_hidden")) {
				$(self.$el.find('.o_thread_composer')).toggleClass("o_hidden");
			}
			if ($(self.$el.find('.o_chatter_button_log_note')).hasClass("o_active")) {
				$(self.$el.find('.o_chatter_button_log_note')).toggleClass("o_active")
			}
			if ($(self.$el.find('.o_chatter_button_new_message')).hasClass("o_active")) {
				$(self.$el.find('.o_chatter_button_new_message')).toggleClass("o_active")
			}
			if ($(self.$el.find('.o_chatter_button_schedule_activity')).hasClass("o_active")) {
				$(self.$el.find('.o_chatter_button_schedule_activity')).toggleClass("o_active")
			}
		},

		_onChangeLogNoteChatter : async function(ev){
			var self = this
			self._hide_tabs();
			var checkbox_input = $(ev.currentTarget);
			if(checkbox_input && checkbox_input)
				if($(checkbox_input).prop('checked')){
					self.do_notify(
							_t('Log Notes are visble now!')
					);
					await rpc.query({
						model : 'mail.chatter.visibility',
						method : 'update_chatter_visibility',
						args : [,'show_lognote',true,self.state.res_id,self.state.model]
					})
					await self.chatter._onReloadMailFields({data:{
						"activity": true,
						"thread": true
					}});
					await $(self.$el.find('.o_chatter_button_log_note_hide')).hide();
					await $(self.$el.find('.o_chatter_button_log_note')).show();
				}
			else {
				self.do_notify(
					_t('Log Note are invisble now!')
				);
				await rpc.query({
					model : 'mail.chatter.visibility',
					method : 'update_chatter_visibility',
					args : [,'show_lognote',false,self.state.res_id,self.state.model]
				})
				await self.chatter._onReloadMailFields({data:{
				  "activity": true,
				  "thread": true
				}});
				await $(self.$el.find('.o_chatter_button_log_note')).hide();
				await $(self.$el.find('.o_chatter_button_log_note_hide')).show();

			}
		},

		_onChangeMessageChatter : async function(ev){
		  	var self = this
			self._hide_tabs();
		  	var checkbox_input = $(ev.currentTarget);
		  	if(checkbox_input && checkbox_input)
		  		if($(checkbox_input).prop('checked')){
					self.do_notify(
					_t('Messages are visble now!')
					);
		    		await rpc.query({
						model : 'mail.chatter.visibility',
						method : 'update_chatter_visibility',
						args : [,'show_mailmessage',true,self.state.res_id,self.state.model]
					})
					await self.chatter._onReloadMailFields({data:{
					  "activity": true,
					  "thread": true
					}});

					await $(self.$el.find('.o_chatter_button_new_message_hide')).hide();
					await $(self.$el.find('.o_chatter_button_new_message')).show();
			  	}
		    else {
				self.do_notify(
					_t('Messages are invisble now!')
				);
			    await rpc.query({
			      	model : 'mail.chatter.visibility',
			      	method : 'update_chatter_visibility',
			      	args : [,'show_mailmessage',false,self.state.res_id,self.state.model]
			    })
				await self.chatter._onReloadMailFields({data:{
				  "activity": true,
				  "thread": true
				}});
				await $(self.$el.find('.o_chatter_button_new_message')).hide();
				await $(self.$el.find('.o_chatter_button_new_message_hide')).show();
		  	}
		},

		_onChangeActivityChatter : async function(ev){
			var self = this
			self._hide_tabs();
			var checkbox_input = $(ev.currentTarget);
			if(checkbox_input && checkbox_input)
				if($(checkbox_input).prop('checked')){
					self.do_notify(
							_t('Activities are visble now!')
					);
					await rpc.query({
						model : 'mail.chatter.visibility',
						method : 'update_chatter_visibility',
						args : [,'show_activity',true,self.state.res_id,self.state.model]
					})
					await self.chatter._onReloadMailFields({data:{
					    "activity": true,
		  				"thread": true
					}});
					await $(self.$el.find('.o_chatter_button_schedule_activity')).show();
					await $(self.$el.find('.o_chatter_button_schedule_activity_hide')).hide();
				}
			else {

				self.do_notify(
					_t('Activities are invisble now!')
				);
				await rpc.query({
					model : 'mail.chatter.visibility',
					method : 'update_chatter_visibility',
					args : [,'show_activity',false,self.state.res_id,self.state.model]
				})
				await self.chatter._onReloadMailFields({data:{ "activity": true, "thread": true}});
				await $(self.$el.find('.o_chatter_button_schedule_activity')).hide();
				await $(self.$el.find('.o_chatter_button_schedule_activity_hide')).show();
			}
		},	

		_renderView: function () {
			var self = this;
			if(this.state.model && this.state.res_id) {
				session.user_context.chatter_model = this.state.model
				session.user_context.chatter_res_id = this.state.res_id
			}
			return Promise.all([this._super.apply(this, arguments)]).then(function(){
				if(self.chatter && self.state.model && self.state.res_id) {
					rpc.query({
						model : 'mail.chatter.visibility',
						method : 'get_chatter_visibility_data',
						args : [,self.state.model,self.state.res_id]
					}).then(function(chatter_data){

						var chatter_visibility_div = '<div class="chatter_visisbilty row"></div>';

						var lognote_checkbox = '<div class="form-check btn" style="text-align:center; margin-right: 0px;">'+
											    '<input type="checkbox" class="form-check-input" id="lognote_chatter">'+
											    '<label class="btn-link form-check-label" for="lognote_chatter">Log Note</label>'+
											   '</div>';

						var message_checkbox = '<div class="form-check btn" style="text-align:center; padding-left: 12px; margin-right: 27px;">'+
											    '<input type="checkbox" class="form-check-input" id="message_chatter">'+
											    '<label class="btn-link form-check-label" for="message_chatter">Messages</label>'+
											   '</div>';

						var activity_checkbox = '<div class="form-check btn" style="text-align:center;">'+
											    '<input type="checkbox" class="form-check-input" id="activity_chatter">'+
											    '<label class="btn-link form-check-label" for="activity_chatter">Activity</label>'+
											   '</div>';

						 var msg_hide = '<div type="button" class="btn btn-link o_chatter_button_new_message_hide div_hide" title="Send a message" style="position: relative;" disabled="true" >Send message</div>';
						 var note_hide = '<div type="button" class="btn btn-link o_chatter_button_log_note_hide div_hide" title="Send a message" style="position: relative;" disabled="true" >Log note</div>';
						 var activity_hide = '<div type="button" class="btn btn-link o_chatter_button_schedule_activity_hide div_hide" title="Send a message" style="position: relative;" disabled="true"><i class="fa fa-clock-o" title="Dates"></i>Schedule activity</div>';

						if(chatter_data){
							
							$(self.$el.find('.o_chatter')).wrap('<div class="chatter_box"></div>')
							$(self.$el.find('.o_chatter')).before(chatter_visibility_div)
							self.$el.find('.chatter_visisbilty').append(message_checkbox)
							self.$el.find('.chatter_visisbilty').append(lognote_checkbox)
							self.$el.find('.chatter_visisbilty').append(activity_checkbox)

							var message_hide = $(self.$el.find('.o_chatter_button_new_message_hide'))
							var log_note_hide = $(self.$el.find('.o_chatter_button_log_note_hide'))
							var activity_hide_Schedule = $(self.$el.find('.o_chatter_button_schedule_activity_hide'))
							
							if(message_hide.length == 0 && log_note_hide.length == 0 && activity_hide_Schedule.length == 0){
								$(self.$el.find('.o_chatter_button_schedule_activity')).after(activity_hide)
								$(self.$el.find('.o_chatter_button_new_message')).after(msg_hide)
								$(self.$el.find('.o_chatter_button_log_note')).after(note_hide)
							}

							$(self.$el.find('.o_chatter_button_new_message_hide')).hide();
							$(self.$el.find('.o_chatter_button_schedule_activity_hide')).hide();
							$(self.$el.find('.o_chatter_button_log_note_hide')).hide();

							$(self.$el.find('.o_chatter_button_new_message')).hide();
							$(self.$el.find('.o_chatter_button_schedule_activity')).hide();
							$(self.$el.find('.o_chatter_button_log_note')).hide();

							if(chatter_data.lognote) {
								self.$el.find('.chatter_visisbilty #lognote_chatter').prop('checked',true);
								$(self.$el.find('.o_chatter_button_log_note')).show();
								self.button_note = true;
							}else{
								self.button_note = false;
							$(self.$el.find('.o_chatter_button_log_note_hide')).show();
							}
							if(chatter_data.mail_message) {
								self.$el.find('.chatter_visisbilty #message_chatter').prop('checked',true)
								$(self.$el.find('.o_chatter_button_new_message')).show();
								self.button_message = true;

							}else{
								self.button_message = false;

								$(self.$el.find('.o_chatter_button_new_message_hide')).show();
							}
							if(chatter_data.activity) {
								self.button_activity = true;

								self.$el.find('.chatter_visisbilty #activity_chatter').prop('checked',true)
								$(self.$el.find('.o_chatter_button_schedule_activity')).show();
							}else{
								self.button_activity = false;
									$(self.$el.find('.o_chatter_button_schedule_activity_hide')).show();
							}

						}
						session.user_context.chatter_model = false;
						session.user_context.chatter_res_id = false;
					})
				}
			});
		},
	})
});