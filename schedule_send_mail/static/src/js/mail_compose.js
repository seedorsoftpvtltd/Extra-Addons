odoo.define('schedule_send_mail.mail_compose', function (require) {
"use strict";
	var BasicComposer = require('mail.composer.Basic');
	var Activity = require('mail.Activity');
	var emojis = require('mail.emojis');
	var MentionManager = require('mail.composer.MentionManager');
	var DocumentViewer = require('mail.DocumentViewer');
	var mailUtils = require('mail.utils');
	var Thread = require('mail.model.Thread');
	var session = require('web.session');
	var core = require('web.core');
	var QWeb = core.qweb;
	var _t = core._t;


	BasicComposer.include({
		init: function (parent, options) {
			this._super(parent, options);
			self.$(".show_date").hide();
			self.$(".send_scheduler").hide();		 
			this.options = _.defaults(this.options || {}, {
				sendScheduler: _t("Schedule Send"),
			});
		},

		start: function () {
		var self = this;
		this._super();
		this.$date = this.$('.o_composer_button_send_scheduler_date');
		this.$date.val(this.options.defaultBody);
		self.$(".show_date").hide();
		self.$(".send_scheduler").hide();
		this.$('.send_schedule_checkbox').click(function(){
			if($(this).prop("checked") == true){
			  $(".show_date").show();
			  $(".send_scheduler").show();
			  $(".o_composer_button_send").attr("disabled", true);
			}
			else if($(this).prop("checked") == false){
				$(".show_date").hide();
				$(".send_scheduler").hide();
				$(".o_composer_button_send").attr("disabled", false);
			}
		});
 
		this.$(".o_composer_button_send_scheduler").click(function(){
		var recipientDoneDef = $.Deferred();
		// any operation on the full-composer will reload the record, so
		// warn the user that any unsaved changes on the record will be lost.
		self.trigger_up('discard_record_changes', {
			proceed: function () {
				if (self.options.isLog) {
					recipientDoneDef.resolve([]);
				} else {
					var checkedSuggestedPartners = self._getCheckedSuggestedPartners();
					self._checkSuggestedPartners(checkedSuggestedPartners)
						.then(recipientDoneDef.resolve.bind(recipientDoneDef));
				}
			},
		});

		recipientDoneDef.then(function (partnerIDs) {
			var context = {
				default_parent_id: self.id,
				default_body: mailUtils.getTextToHTML(self.$input.val()),
				default_attachment_ids: _.pluck(self.get('attachment_ids'), 'id'),
				default_partner_ids: partnerIDs,
				default_is_log: self.options.isLog,
				mail_post_autofollow: true,
			};

			if (self.context.default_model && self.context.default_res_id) {
				context.default_model = self.context.default_model;
				context.default_res_id = self.context.default_res_id;
				context.default_body = mailUtils.getTextToHTML(self.$input.val());
				context.default_attachment_ids = _.pluck(self.get('attachment_ids'), 'id');
				context.default_date = self.$date.val();
			}
			var resModel = self.context.default_model
			var resID = self.context.default_res_id
			self._rpc({
					  model: 'mail.activity',
					  method: 'generate_scheduler',
					  args: [resID],
					  kwargs: context,
			})
			  .then(function (messageID) {
						if(messageID == "date not entered"){
							self.do_notify(_t("Sending Error"), _t("Please Select Validate Date First"));
							self._mentionManager.resetSelections();
							self.$input.val('');
							self.set('attachment_ids', []);
							self.$('.o_composer_button_send_scheduler').val('');
						 	self.$('.o_composer_input textarea').val('');
						 	self.$('.o_composer_button_send_scheduler_date').val('');
						 	self.$(".send_schedule_checkbox").prop("checked", true);
							self.destroy();
							self.trigger_up('reload');
						}else if(messageID == "date not valid"){
							self.do_notify(_t("Sending Error"), _t("Schedule date not valid , Please select validate date'"));
							self._mentionManager.resetSelections();
							self.$input.val('');
							self.set('attachment_ids', []);
							self.$('.o_composer_button_send_scheduler').val('');
						 	self.$('.o_composer_input textarea').val('');
						 	self.$('.o_composer_button_send_scheduler_date').val('');
						 	self.$(".send_schedule_checkbox").prop("checked", true);
							self.destroy();
							self.trigger_up('reload');
						}else if(messageID== true){
							var attachments = self.get('attachment_ids');
							self.do_notify(_t("Success Message"), _t("Your message Register in Schedule Send."));
						 	self.$('.o_composer_button_send_scheduler').val('');
						 	self.$('.o_composer_input textarea').val('');
						 	self.$('.o_composer_button_send_scheduler_date').val('');
						 	self.$('input.o_input_file').val('');
						 	self.trigger_up('reload');
						 	self.$('input.o_input_file').val('');
						 	self._mentionManager.resetSelections();
						 	self.set('attachment_ids', []);
						 	self.destroy();
						  }else{
							  self.do_notify(_t("Sending Error"), _t("Your message Not Register , Please contact to Administrator"));
							  self._mentionManager.resetSelections();
								self.$input.val('');
								self.set('attachment_ids', []);
								self.$('.o_composer_button_send_scheduler').val('');
							 	self.$('.o_composer_input textarea').val('');
							 	self.$('.o_composer_button_send_scheduler_date').val('');
							 	self.$(".send_schedule_checkbox").prop("checked", true);
								self.destroy();
								self.trigger_up('reload');
						  }
					})
				});
			});
		},
	});

});