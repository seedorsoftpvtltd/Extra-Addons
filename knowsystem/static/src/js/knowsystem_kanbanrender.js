odoo.define('knowsystem.knowsystem_kanbanrender', function (require) {
"use strict";

    var KnowSystemKanbanRecord = require('knowsystem.knowsystem_kanbanrecord');

    var KanbanRenderer = require('web.KanbanRenderer');

    var KnowSystemKanbanRenderer = KanbanRenderer.extend({
        config: _.extend({}, KanbanRenderer.prototype.config, {
            KanbanRecord: KnowSystemKanbanRecord,
        }),
        updateSelection: function (selectedRecords) {
            // To keep selected articles when switching between pages and filters
            _.each(this.widgets, function (widget) {
                if (typeof widget._updateRecordView === 'function') {
                    var selected = _.contains(selectedRecords, widget.id);
                    widget._updateRecordView(selected);
                }
                else {
                    _.each(widget.records, function (widg) {
                        var selected = _.contains(selectedRecords, widg.id);
                        widg._updateRecordView(selected);
                    });
                }
            });
        },

    });

    return KnowSystemKanbanRenderer;

});
