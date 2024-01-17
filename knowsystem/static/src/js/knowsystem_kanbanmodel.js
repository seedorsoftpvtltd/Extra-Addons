odoo.define('knowsystem.kwowsystem_kanbanmodel', function (require) {
"use strict";

    var KanbanModel = require('web.KanbanModel');
    var core = require('web.core');

    var _t = core._t;

    var KnowSystemKanbanModel = KanbanModel.extend({
        reload: function (id, options) {
            // Re-write to explicitly retrieve searchDomain from element, when no options.domain is received
            options = options || {};
            var element = this.localData[id];
            var searchDomain = options.domain || element.searchDomain || [];
            element.searchDomain = options.searchDomain = searchDomain;
            if (options.knowSystemDomain !== undefined) {
                options.domain = searchDomain.concat(options.knowSystemDomain);
            };
            return this._super.apply(this, arguments)
        },
    });

    return KnowSystemKanbanModel;

});
