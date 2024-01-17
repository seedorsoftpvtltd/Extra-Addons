odoo.define('knowsystem.composer_html', function (require) {
"use strict";

    var session = require('web.session');
    var registry = require('web.field_registry');
    var core = require('web.core');
    var FieldHtml = require('web_editor.field.html');
    var dialogs = require('web.view_dialogs');
    var rpc = require('web.rpc');
    
    var qweb = core.qweb;
    var _t = core._t;

    var KnowSystemComposerHtml = FieldHtml.extend({
        events: {"click .open_knowsystem": "_onOpenKnowSystem",},
        _renderEdit: function () {
            // Rewrite to render quick parts
            var self = this;
            this._super.apply(this, arguments);
            rpc.query({
                model: "knowsystem.section",
                method: "check_option",
                args: [[], "composer"],
            }).then(function (need) {
                if (need) {
                    var quickKnowSystem = qweb.render("ComposerQuickLink", {});
                    self.$('.note-toolbar').append(quickKnowSystem);
                };
            });
        },
        _onOpenKnowSystem: function (event) {
            var self = this;
            var resModel = this.record.data['model'];
            var resID = parseInt(this.record.data['res_id'])
            self._rpc({
                model: "knowsystem.section",
                method: "return_article_search",
                args: [[], resModel, resID],
                context:  this.record.context,
            }).then(function (res) {
                var context = res.context;
                context.default_no_selection = false;
                var dialog = new dialogs.FormViewDialog(self, {
                    res_model: "article.search",
                    title: _t("Articles quick search"),
                    context: context,
                    view_id: res.view_id,
                    readonly: false,
                    shouldSaveLocally: false,
                    buttons: [
                        {
                            text: (_t("Update Body")),
                            classes: "btn-primary",
                            click: function () {
                                dialog._save().then(
                                    self._onApplyArticleAction(dialog, "add_to_body"),
                                );
                            },
                        },
                        {
                            text: (_t("Share URL")),
                            classes: "btn-primary",
                            click: function () {
                                dialog._save().then(
                                    self._onApplyArticleAction(dialog, "share_url"),
                                );
                            },
                        },
                        {
                            text: (_t("Attach PDF")),
                            classes: "btn-primary",
                            click: function () {
                                dialog._save().then(
                                    self._onApplyArticleAction(dialog, "add_pdf"),
                                );
                            },
                        },
                        {
                            text: (_t("Close")),
                            classes: "btn-secondary o_form_button_cancel",
                            close: true,
                        },
                    ],
                });
                dialog.open();
            });
        },
        _onApplyArticleAction: function(dialog, action) {
            var record = dialog.form_view.model.get(dialog.form_view.handle);
            var articles = record.data.selected_article_ids.data;
            var articleIDS = [];
            _.each(articles, function (art) {
                articleIDS.push(parseInt(art.res_id));
            });
            var self = this;
            self._rpc({
                model: 'knowsystem.article',
                method: 'proceed_article_action',
                args: [articleIDS, action],
            }).then(function(article) {
                if (article) {
                    if (article.descr && article.descr.length !== 0) {
                        self.$content = self.$('.note-editable:first');
                        self.$content.append(article.descr);
                    };
                    if (article.url && article.url.length !== 0) {
                        self.$content = self.$('.note-editable:first');
                        self.$content.append(article.url);
                    };
                    if (article.attachment_ids) {
                        self._onAttachmentChange({'data': article.attachment_ids});
                    };
                };
                dialog.close();
            });
        },
    });

    registry.add('know_system_composer', KnowSystemComposerHtml);
    return KnowSystemComposerHtml
});
