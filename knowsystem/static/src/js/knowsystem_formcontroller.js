odoo.define('knowsystem.knowsystem_formcontroller', function (require) {
"use strict";

    var core = require('web.core');
    var session = require('web.session');
    var FormController = require('web.FormController');
    var Dialog = require('web.Dialog');
    var dialogs = require('web.view_dialogs');
    var Pager = require('web.Pager');

    var qweb = core.qweb;
    var _t = core._t;

    var KnowSystemFormController = FormController.extend({
        events: _.extend({}, FormController.prototype.events, {
            "click .hide_chatter": "_onKnowSystemChatter",
        }),
        init: function (parent, model, renderer, params) {
            // Re write to save number of views
            this._super.apply(this, arguments);
            if (this.modelName == 'knowsystem.article') {this.articleController = true;};
        },
        renderButtons: function ($node) {
            // Re write to add custom buttons to
            var self = this;
            $.when(this._super.apply(this, arguments)).then(function () {
                if (self.modelName == 'knowsystem.article') {
                    $(".o_cp_left").addClass("know_left_control");
                    $(".o_cp_right").addClass("know_right_control");
                    self._renderKnowSystemButtons();
                };
            });
        },
        _update: function() {
            // Re-write to update likes when articles are switched. Also update views counter
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                var articleID = self.model.localData[self.handle];
                self._rpc({
                    model: "knowsystem.article",
                    method: 'return_complementary_data',
                    args: [[articleID.data.id]],
                    context: {},
                }).then(function (cdata) {
                    self._updateLikes(cdata);
                    self._updateArchive(cdata);
                    self._updateFavourite(cdata);
                    self._updatePublish(cdata);
                }); 
                self._rpc({
                    model: "knowsystem.article",
                    method: 'update_number_of_views',
                    args: [[articleID.data.id]],
                    context: {},
                })
            });
        },
        _renderKnowSystemButtons: function() {
            var self = this;
            if (this.modelName == 'knowsystem.article') {
                var articleID = self.model.localData[self.handle];
                self._rpc({
                    model: "knowsystem.article",
                    method: 'return_complementary_data',
                    args: [[articleID.data.id]],
                    context: {},
                }).then(function (cdata) {
                    var extraButtons = qweb.render("KnowSystemFormButtons", {widget: self, cdata: cdata});
                    self.$buttons.find(".knowsystem_buttons").append(extraButtons);
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_create_from_template',
                        self._onKnowSystemCreateFromTemplate.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_edit_website',
                        self._onKnowSystemEditWebsite.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_make_template',
                        self._onKnowSystemMakeTemplate.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_article_revisions',
                        self._onKnowSystemRevisions.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_article_info',
                        self._onKnowSystemInfo.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_print',
                        self._onKnowSystemPrint.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_chatter',
                        self._onKnowSystemChatter.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_article_like',
                        self._onArticleLike.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_article_dislike',
                        self._onArticleDisLike.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_article_archive',
                        self._onArticleArchive.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_article_publish',
                        self._onArticlePublish.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_duplicate',
                        self._onDuplicateRecord.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_delete',
                        self._onDeleteRecord.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_mark_favourite',
                        self._onMarkFavourite.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_add_to_tour',
                        self._onAddToTour.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.form_knowsystem_restrict_access',
                        self._onOpenRights.bind(self)
                    );
                    self.$buttons.on(
                        'click',
                        '.open_misc_actions',
                        self._onOpenMiscActions.bind(self)
                    );
                    $(document).on("click", function (event) {self._onClose(event);});
                });
            };
        },
        _onKnowSystemEditWebsite: function(event) {
            var self = this;
            var articleID = this.model.localData[this.handle];
            this._rpc({
                model: "knowsystem.article",
                method: 'edit_website',
                args: [[articleID.data.id]],
                context: {},
            }).then(function (res) {
                self.do_action(res);
            });
        },
        _onKnowSystemCreateFromTemplate: function(event) {
            var self = this;
            this._rpc({
                model: "knowsystem.article",
                method: 'select_template',
                args: [[]],
                context: {},
            }).then(function (res) {
                self.do_action(res);
            });
        },
        _onKnowSystemMakeTemplate: function(event) {
            var self = this;
            var articleID = this.model.localData[this.handle];
            this._rpc({
                model: "knowsystem.article",
                method: 'action_make_template',
                args: [[articleID.data.id]],
                context: {},
            }).then(function (res) {
                self.do_action(res);
            });
        },
        _onKnowSystemRevisions: function(event) {
            // The method to return revisions list
            var self = this;
            var articleID = this.model.localData[this.handle];
            this._rpc({
                model: "knowsystem.article",
                method: 'get_revisions',
                args: [[articleID.data.id]],
                context: {},
            }).then(function (revisions) {
                var $content = qweb.render("KnowSystemRevisions", {revisions: revisions,});
                var dialog = new RevisionsDialog(self, {
                    title: _t("Revisions"),
                    buttons: [
                        {text: _t("Back"), classes: "btn-primary o_save_button", close: true}
                    ],
                    $content: $content,
                    size: 'large',
                    fullscreen: true,
                });
                dialog.open();
            });
        },
        _onKnowSystemInfo: function(event) {
            // The method to open stats of the article and misc info
            var self = this;
            var article = this.model.localData[this.handle],
                articleID = article.data.id;
            this._rpc({
                model: "knowsystem.article",
                method: 'get_info_formview_id',
                args: [[articleID]],
                context: {},
            }).then(function (view_id) {
                new dialogs.FormViewDialog(self, {
                    res_model: "knowsystem.article",
                    res_id: articleID,
                    context: {},
                    title: _t("Info"),
                    view_id: view_id,
                    shouldSaveLocally: false,
                    readonly: true,
                }).open();
            });
        },
        _onOpenRights: function(event) {
            // The method to open user groups
            var self = this;
            var article = this.model.localData[this.handle],
                articleID = article.data.id;
            this._rpc({
                model: "knowsystem.article",
                method: 'get_rights_formview_id',
                args: [[articleID]],
                context: {},
            }).then(function (view_id) {
                new dialogs.FormViewDialog(self, {
                    res_model: "knowsystem.article",
                    res_id: articleID,
                    context: {},
                    title: _t("Info"),
                    view_id: view_id,
                    shouldSaveLocally: false,
                    readonly: false,
                }).open();
            });
        },
        _onKnowSystemPrint: function(event) {
            // The method to open stats of the article and misc info
            var self = this;
            var article = this.model.localData[this.handle],
                articleID = article.data.id;
            this._rpc({
                model: "knowsystem.article",
                method: "save_as_pdf",
                args: [[articleID]],
                context: {},
            }).then(function (action_id) {
                self.do_action(action_id);
            });
        },
        _onKnowSystemChatter: function(event) {
            // The method to opend discussion channel of this article
            var chatterDiv = this.$el.find(".knowsystem_chatter")
            if (chatterDiv.hasClass("knowsystem_hidden")) {
                chatterDiv.removeClass("knowsystem_hidden");
            }
            else {
                chatterDiv.addClass("knowsystem_hidden");
            }
        },
        _onArticleLike: function(event) {
            // The method to mark the article as liked
            var self = this;
            var article = this.model.localData[this.handle],
                articleID = article.data.id;
            this._rpc({
                model: "knowsystem.article",
                method: 'like_the_article',
                args: [[articleID]],
                context: {},
            }).then(function (cdata) {
                self._updateLikes(cdata);
            });
        },
        _onArticleDisLike: function(event) {
            // The method to mark the article disliked
            var self = this;
            var article = this.model.localData[this.handle],
                articleID = article.data.id;
            this._rpc({
                model: "knowsystem.article",
                method: 'dislike_the_article',
                args: [[articleID]],
                context: {},
            }).then(function (cdata) {
                self._updateLikes(cdata);
            });
        },
        _updateLikes: function(cdata) {
            // The method to update interfaces based on new likes data
            this.$buttons.find('#knowdislike').removeClass("done_article_like");
            this.$buttons.find('#knowlike').removeClass("done_article_like");
            if (cdata.user_like) {this.$buttons.find('#knowlike').addClass("done_article_like");}
            if (cdata.user_dislike) {this.$buttons.find('#knowdislike').addClass("done_article_like");};
            var likesCounters = this.$buttons.find('#knowlike_counter');
            var dislikesCounter = this.$buttons.find('#knowdislike_counter');
            var likeCounter = this.$buttons.find('#knowlike_counter');
            var dislikeCounter = this.$buttons.find('#knowdislike_counter');
            if (likeCounter.length != 0 && dislikeCounter.length != 0) {
                likeCounter[0].innerHTML = cdata.likes_counter;
                dislikeCounter[0].innerHTML  = cdata.dislikes_counter;
            };
        },
        _onArticleArchive: function(event) {
            // The method to archive / restore the article
            event.stopPropagation();
            var self = this;
            var article = this.model.localData[this.handle],
                articleID = article.data.id;
            this._rpc({
                model: "knowsystem.article",
                method: 'archive_article',
                args: [[articleID]],
                context: {},
            }).then(function (cdata) {
                self._updateArchive(cdata);
            });
        },
        _updateArchive : function(cdata) {
            // The method to update 'active' value in the interface
            this.$buttons.find('#article_archive').removeClass("knowsystem_hidden");
            this.$buttons.find('#article_restore').removeClass("knowsystem_hidden");
            if (cdata.active) {this.$buttons.find('#article_restore').addClass("knowsystem_hidden");}
            else {this.$buttons.find('#article_archive').addClass("knowsystem_hidden");};
        },
        _onArticlePublish: function(event) {
            // The method to publish / unpublish the article
            event.stopPropagation();
            var self = this;
            var article = this.model.localData[this.handle],
                articleID = article.data.id;
            this._rpc({
                model: "knowsystem.article",
                method: 'publish_article',
                args: [[articleID]],
                context: {},
            }).then(function (cdata) {
                self._updatePublish(cdata);
            });
        },
        _updatePublish: function(cdata) {
            // The method to update 'active' value in the interface
            this.$buttons.find('#article_publish').removeClass("knowsystem_hidden");
            this.$buttons.find('#article_unpublish').removeClass("knowsystem_hidden");
            if (cdata.website_published) {
                this.$buttons.find('#article_publish').addClass("knowsystem_hidden");
            }
            else {
                this.$buttons.find('#article_unpublish').addClass("knowsystem_hidden");
            };
        },
        _onMarkFavourite: function(event) {
            // The method to add / remove articles from favourites
            var self = this;
            var article = this.model.localData[this.handle],
                articleID = article.data.id;
            this._rpc({
                model: "knowsystem.article",
                method: 'mark_as_favourite',
                args: [[articleID]],
                context: {},
            }).then(function (cdata) {
                self._updateFavourite(cdata);
            });
        },
        _updateFavourite: function(cdata) {
            // The method to update 'favourite' in the interface
            if (cdata.favourite) {
                this.$buttons.find('#knowfavorbutton').removeClass("fa-star-o");
                this.$buttons.find('#knowfavorbutton').addClass("fa-star");
            }
            else {
                this.$buttons.find('#knowfavorbutton').removeClass("fa-star");
                this.$buttons.find('#knowfavorbutton').addClass("fa-star-o");
            };
        },
        _onAddToTour: function(event) {
            // The method to open tour selection wizard
            var self = this;
            var article = this.model.localData[this.handle],
                articleID = article.data.id;
            this._rpc({
                model: "knowsystem.article",
                method: 'return_add_to_tour_wizard',
                args: [[articleID]],
                context: {},
            }).then(function (view_id) {
                var onSaved = function(record) {
                    var tourId = record.data.tour_id.res_id;
                    self._rpc({
                        model: "knowsystem.tour",
                        method: 'return_form_view',
                        args: [[tourId]],
                        context: {},
                    }).then(function (action) {
                        self.do_action(action);
                    });
                };
                new dialogs.FormViewDialog(self, {
                    res_model: "add.to.tour",
                    context: {'default_articles': articleID},
                    title: _t("Add to tour"),
                    view_id: view_id,
                    readonly: false,
                    shouldSaveLocally: false,
                    on_saved: onSaved,
                }).open();
            });
        },
        _onOpenMiscActions: function(event) {
            // The method to show the list of hidden actions
            event.stopPropagation();
            var self = this;
            var thisButton = self.$buttons.find('.open_misc_actions');
            var miscButtons = self.$buttons.find('.knowsystem_misc_actions');
            if (miscButtons.hasClass("knowsystem_hidden")) {
                miscButtons.removeClass("knowsystem_hidden");
                thisButton.addClass("highlight_button");
            }
            else {
                miscButtons.addClass("knowsystem_hidden");
                thisButton.removeClass("highlight_button");
            };
        },
        _onClose: function () {
            // The method to hide dropdown elements under any click outside
            var self = this;
            var thisButton = self.$buttons.find('.open_misc_actions');
            var miscButtons = self.$buttons.find('.knowsystem_misc_actions');
            miscButtons.addClass("knowsystem_hidden");
            thisButton.removeClass("highlight_button");
        },
        _enableButtons: function () {
            // Re-write to the case of create & duplicate
            this._super.apply(this, arguments);
            var self = this;
            if (this.modelName == 'knowsystem.article') {
                var articleID = self.model.localData[self.handle];
                self._rpc({
                    model: "knowsystem.article",
                    method: 'return_complementary_data',
                    args: [[articleID.data.id]],
                    context: {},
                }).then(function (cdata) {
                    self._updateLikes(cdata);
                    self._updateArchive(cdata);
                    self._updateFavourite(cdata);
                });
            };
        },
    });
    var RevisionsDialog = Dialog.extend({
        events: _.extend({}, Dialog.prototype.events, {
            'click .open_revision': '_onOpenRevision',
        }),
        _onOpenRevision: function(event) {
            var self = this;
            var articleID = parseInt($(event.target).data('id'));
            this._rpc({
                model: "knowsystem.article.revision",
                method: 'open_revision',
                args: [[articleID]],
                context: {},
            }).then(function (res) {
                self.do_action(res);
            });
        },
    });

    return  KnowSystemFormController;

});
