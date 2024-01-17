odoo.define('knowsystem.knowsystem_formrenderer', function (require) {
"use strict";

    var FormRenderer = require('web.FormRenderer');

    var KnowSystemFormRenderer = FormRenderer.extend({
        displayTranslationAlert: function () {
            // re-write to replace translation alerts
        },
    });

    return KnowSystemFormRenderer;

});
