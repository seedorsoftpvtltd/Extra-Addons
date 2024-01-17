
odoo.define('multi_container_for_warehouse.set_limitaiton', function (require) {

"use strict";
var FieldChar = require('web.basic_fields').FieldChar;
var fieldRegistry = require('web.field_registry');

var MonkTextOnly = FieldChar.extend({

});

fieldRegistry.add('monk_text_only', MonkTextOnly);
return MonkTextOnly;

});
