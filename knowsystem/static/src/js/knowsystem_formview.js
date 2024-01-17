odoo.define('knowsystem.knowsystem_formview', function (require) {
"use strict";

    var KnowSystemFormController = require('knowsystem.knowsystem_formcontroller');
    var KnowSystemFormRenderer = require('knowsystem.knowsystem_formrenderer');
    var config = require('web.config');
    var core = require('web.core');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var _lt = core._lt;

    var KnowSystemFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: KnowSystemFormController,
            Renderer: KnowSystemFormRenderer,
        }),
    });

    view_registry.add('knowsystem_form', KnowSystemFormView);

    return KnowSystemFormView;

});