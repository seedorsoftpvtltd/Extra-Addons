odoo.define('knowsystem.knowsystem_kanbanrecord', function (require) {
"use strict";

    var KanbanRecord = require('web.KanbanRecord');

    var KnowSystemKanbanRecord = KanbanRecord.extend({
        events: _.extend({}, KanbanRecord.prototype.events, {
            'click .article_select': '_articleSelect',
        }),
        _updateSelect: function (event, selected) {
            // The method to pass selection to the controller
            this.trigger_up('select_record', {
                originalEvent: event,
                resID: this.id,
                selected: selected,
            });
        },
        _updateRecordView: function (select) {
            // Mark the article selected / disselected in the interface
            var kanbanCard = this.$el;
            var checkBox = this.$el.find(".article_select");
            if (select) {
                checkBox.removeClass("fa-square-o");
                checkBox.addClass("fa-check-square-o");
                kanbanCard.addClass("knowkanabanselected");
            }
            else {
                checkBox.removeClass("fa-check-square-o");
                checkBox.addClass("fa-square-o");
                kanbanCard.removeClass("knowkanabanselected");
            };
        },
        _articleSelect: function (event) {
            // The method to add to / remove from selection
            event.preventDefault();
            event.stopPropagation();
            var checkBox = this.$el.find(".article_select");
            if (checkBox.hasClass("fa-square-o")) {
                this._updateRecordView(true)
                this._updateSelect(event, true);
            }
            else {
                this._updateRecordView(false);
                this._updateSelect(event, false);
            }
        },
    });

    return KnowSystemKanbanRecord;

});