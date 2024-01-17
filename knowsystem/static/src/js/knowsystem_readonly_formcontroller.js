odoo.define('knowsystem.knowsystem_readonly_formcontroller', function (require) {
"use strict";

    var core = require('web.core');
    var session = require('web.session');
    var FormController = require('web.FormController');

    var qweb = core.qweb;
    var _t = core._t;

    var KnowSystemReadonlyFormController = FormController.extend({
        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
            this.activeActions = false;
        },
    });
    return  KnowSystemReadonlyFormController;

});