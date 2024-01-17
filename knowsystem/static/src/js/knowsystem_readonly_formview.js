odoo.define('knowsystem.knowsystem_readonly_formview', function (require) {
"use strict";

    var KnowSystemReadonlyFormController = require('knowsystem.knowsystem_readonly_formcontroller');
    var config = require('web.config');
    var core = require('web.core');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var _lt = core._lt;

    var KnowSystemReadonlyFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: KnowSystemReadonlyFormController,
        }),
    });

    view_registry.add('knowsystem_readonly_form', KnowSystemReadonlyFormView);

    return KnowSystemReadonlyFormView;

});