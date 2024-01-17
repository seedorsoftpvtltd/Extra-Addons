odoo.define('documentation_builder.docu_kwowsystem_kanbancontroller', function (require) {
"use strict";

    var core = require('web.core');
    var KnowSystemKanbanController = require('knowsystem.kwowsystem_kanbancontroller');
    var dialogs = require('web.view_dialogs');

    var _t = core._t;

    KnowSystemKanbanController.include({
        events: _.extend({}, KnowSystemKanbanController.prototype.events, {
        	"click .documentation_articles_add": "_onAddToDocumentation",
        }),
        _onAddToDocumentation: function(event) {
            // The method to open adding to documentaiton wizard
            event.stopPropagation();
            var self = this;
            this._rpc({
                model: "documentation.section",
                method: 'return_add_to_documentation_wizard',
                args: [this.selectedRecords],
                context: {},
            }).then(function (view_id) {
                var onSaved = function(record) {
                    var docuID = record.data.section_id.res_id;
                    self._rpc({
                        model: "documentation.section",
                        method: 'return_form_view',
                        args: [[docuID]],
                        context: {},
                    }).then(function (action) {
                        self.do_action(action);
                    });
                };
                new dialogs.FormViewDialog(self, {
                    res_model: "add.to.documentation",
                    context: {'default_articles': self.selectedRecords.join()},
                    title: _t("Add to Documentation"),
                    view_id: view_id,
                    readonly: false,
                    shouldSaveLocally: false,
                    on_saved: onSaved,
                }).open();
            });
        },
    });

});