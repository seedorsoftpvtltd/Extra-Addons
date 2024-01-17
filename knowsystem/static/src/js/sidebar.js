odoo.define('knowsystem.Sidebar', function (require) {
"use strict";

    var core = require('web.core');
    var Sidebar = require('web.Sidebar');
    var dialogs = require('web.view_dialogs');
    var rpc = require('web.rpc');

    var qweb = core.qweb;
    var _t = core._t;

    Sidebar.include({
        _redraw: function () {
            var self = this;
            var resModel = this.options.env.model;
            var viewType = this.options.viewType;
            if (resModel == 'knowsystem.article'
                || resModel == 'knowsystem.article.revision'
                && viewType === "form") {
                // remove the actions sidebar for articles form view
                this.$el.html("");
            }
            else {
                this._super.apply(this, arguments);
                // Render knowsystem quick link
                // viewType === "form" &&
                if (resModel) {
                    rpc.query({
                        model: "knowsystem.section",
                        method: "check_option",
                        args: [[], "form"],
                    }).then(function (need) {
                        if (need) {
                            $('#quick_knowsystem').remove();
                            var quickLink = qweb.render("KnowSystemQuickLink", {widget: self});
                            self.$el.after(quickLink);
                            $("#quick_knowsystem").on("click", function () {
                                self._openKnowSystem();
                            });
                        };
                    });
                };
            };
        },
        _openKnowSystem: function () {
            // The method to open knowsystem (wizard?)
            var self = this;
            var resModel = this.options.env.model;
            var resID = parseInt(this.options.env.activeIds[0]);
            self._rpc({
                model: "knowsystem.section",
                method: "return_article_search",
                args: [[], resModel, resID],
                context: this.options.env.context,
            }).then(function (res) {
                var context = res.context;
                context.default_no_selection = true;
                new dialogs.FormViewDialog(self, {
                    res_model: "article.search",
                    title: _t("Articles quick search"),
                    context: context,
                    view_id: res.view_id,
                    readonly: false,
                    shouldSaveLocally: false,
                    buttons: [{
                        text: (_t("Close")),
                        classes: "btn-secondary o_form_button_cancel",
                        close: true,
                    }],
                }).open();
            });
        },
    });

});