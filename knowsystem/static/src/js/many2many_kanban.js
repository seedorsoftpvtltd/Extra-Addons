odoo.define('knowsystem.many2many_kanban', function (require) {
"use strict";

    var session = require('web.session');
    var registry = require('web.field_registry');
    var core = require('web.core');
    var relationalFields = require('web.relational_fields');

    var qweb = core.qweb;
    var _t = core._t;

    var knowSystemKanban = relationalFields.FieldMany2Many.extend({
        events: _.extend({}, relationalFields.FieldMany2Many.prototype.events, {
            'click .article_select': '_articleSelect',
        }),
        _articleSelect: function (event) {
            // The method to add to selection
            event.preventDefault();
            event.stopPropagation();
            var articleId = parseInt(event.currentTarget.id);
            this.trigger_up('field_changed', {
                dataPointID: this.dataPointID,
                changes: _.object(["selected_article_ids"], [{
                    operation: 'ADD_M2M',
                    ids: [{"id": articleId}],
                }])
            });
        },
        _onOpenRecord: function (event) {
            // Re-write to update views counter
            this._super.apply(this, arguments);
            var articleID = parseInt(event.target.id);
            this._rpc({
                model: "knowsystem.article",
                method: 'update_number_of_views',
                args: [[articleID]],
                context: {},
            })
        },
    });

    registry.add('many2many_knowsystem_kanban', knowSystemKanban);
});
