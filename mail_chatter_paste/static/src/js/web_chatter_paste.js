/* Copyright 2017 Onestein
* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

odoo.define('web_chatter_paste', function (require) {
"use strict";
    var core = require('web.core');
    var composer = require('mail.composer.Basic');


    composer.include({
        start: function() {
            var self = this;
            var res = this._super.apply(this, arguments);
			
			this.$('.o_composer_text_field').on('paste', function(e) {
                if (!e.originalEvent.clipboardData.items) return;
                var items = e.originalEvent.clipboardData.items;
				var files = e.originalEvent.clipboardData.files;
				
                for (var i = 0; i < items.length; i++) 
					{
					var item = items[i];
                    if (item.type != 'image/png') continue;
                    var reader = new FileReader();
                    reader.onload = function() {
                        self.add_as_attachment(reader.result, _.uniqueId('pasted_file') + '.png');
						}
                    reader.readAsDataURL(item.getAsFile());
					}
				});
            return res;
        },
        add_as_attachment: function(data, filename, cb) {
            //Fetch mimetype and base64
            var mimetype = data.substring(5, data.indexOf(';'));
            var base64_data = data.substr(data.indexOf(',') + 1, data.length);

            //Change and submit form
            this.prepare_form();
            this.$('form.o_form_binary_form input.filename').val(filename);
            this.$('form.o_form_binary_form input.content').val(base64_data);
            this.$('form.o_form_binary_form input.mimetype').val(mimetype);

            this.$('form.o_form_binary_form').submit();
            this.reverse_form();

            var attachments = this.get('attachment_ids');
            //this.$attachment_button.prop('disabled', true);
            attachments.push({
                'id': 0,
                'name': _.uniqueId('attachment_name'),
                'filename': filename,
                'url': filename,
                'upload': true,
                'mimetype': '',
				});
			},
        prepare_form: function() {
            //Change action
            this.$('form.o_form_binary_form').attr('action', '/web_chatter_paste/upload_attachment');

            //Remove ufile
            this.$('form.o_form_binary_form input.o_form_input_file').remove();

            //Add hidden input content
            var $content = $('<input type="hidden" name="content" class="content" />');
            this.$('form.o_form_binary_form').append($content);

            //Add hidden input filename
            var $filename = $('<input type="hidden" name="filename" class="filename" />');
            this.$('form.o_form_binary_form').append($filename);

            //Add hidden input filename
            var $mimetype = $('<input type="hidden" name="mimetype" class="mimetype" />');
            this.$('form.o_form_binary_form').append($mimetype);
			},
        reverse_form: function() {
            //Change action
            this.$('form.o_form_binary_form').attr('action', '/web/binary/upload_attachment');

            //Remove new input
            this.$('form.o_form_binary_form input.content').remove();
            this.$('form.o_form_binary_form input.filename').remove();
            this.$('form.o_form_binary_form input.mimetype').remove();

            //Restore old input
            var $ufile = $('<input class="o_form_input_file" name="ufile" type="file" />');
            this.$('form.o_form_binary_form').append($ufile);
			},
		_preprocessMessage: function () {
            var selectTor = $(".o_thread_message.o_thread_selected_message");
            var value = _.escape(this.$input.val()).trim();
            value = value.replace(/(\r|\n){2,}/g, '<br/><br/>');
            value = value.replace(/(\r|\n)/g, '<br/>');

            value = value.replace(/ /g, '&nbsp;').replace(/([^>])&nbsp;([^<])/g, '$1 $2');
            var commands = this.options.commandsEnabled ?
                            this._mentionManager.getListenerSelection('/') :
                            [];

            var msg_quotes = [];
			var quoteAttach = [];

			if(selectTor.length > 0)
				{
				var msgHTML = selectTor.find(".o_thread_message_content").clone();
				$(msgHTML).find(".user-quote-messages").remove();
				$(msgHTML).find(".o_attachment").remove();

				_.each(selectTor.find(".o_attachment"), function(singleHTML, index) {
					quoteAttach.push({
						'id': $(singleHTML).find(".o_image_box").attr("attachment-id"),
						'filename': $(singleHTML).attr("title"),
						'name': $(singleHTML).attr("title"),
						'mimetype': $(singleHTML).find(".o_image_box").attr("attachment-mime-type")
						});
					});

				msg_quotes = [{
					'name': selectTor.find(".o_thread_message_core > .o_mail_info .o_thread_author").text().trim(),
					'quote_date': selectTor.find(".o_thread_message_core > .o_mail_info .o_mail_timestamp").attr("title"),
					'quote_msg': $(msgHTML).html().trim(),
					'quote_msg_id': selectTor.attr('data-message-id'),
					'q_attachments': quoteAttach,
					'hour': selectTor.find(".o_thread_message_core > .o_mail_info .o_mail_timestamp").html(),
					}];
				}

            return $.when({
                content: this._mentionManager.generateLinks(value),
                msg_quotes: msg_quotes,
                attachment_ids: _.pluck(this.get('attachment_ids'), 'id'),
                partner_ids: _.uniq(_.pluck(this._mentionManager.getListenerSelection('@'), 'id')),
                canned_response_ids: _.uniq(_.pluck(this._mentionManager.getListenerSelections()[':'], 'id')),
                command: commands.length > 0 ? commands[0].name : undefined,
                });
            },
        });


 
});
