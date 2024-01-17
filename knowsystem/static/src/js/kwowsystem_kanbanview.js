odoo.define('knowsystem.kwowsystem_kanbanview', function (require) {
"use strict";

    var KnowSystemKanbanController = require('knowsystem.kwowsystem_kanbancontroller');
    var KnowSystemKanbanModel = require('knowsystem.kwowsystem_kanbanmodel');
    var KnowSystemKanbanRenderer = require('knowsystem.knowsystem_kanbanrender');
    var config = require('web.config');
    var core = require('web.core');
    var KanbanView = require('web.KanbanView');
    var view_registry = require('web.view_registry');

    var _lt = core._lt;

    var KnowSystemKanbanView = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Controller: KnowSystemKanbanController,
            Model: KnowSystemKanbanModel,
            Renderer: KnowSystemKanbanRenderer,
        }),
        display_name: _lt('Knowledge Base'),
        groupable: false,
    });

    view_registry.add('knowsystem_kanban', KnowSystemKanbanView);

    return KnowSystemKanbanView;

});