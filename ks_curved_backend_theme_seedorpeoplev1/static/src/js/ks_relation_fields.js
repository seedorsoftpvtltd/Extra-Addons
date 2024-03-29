odoo.define("ks_curved_backend_theme_seedorpeoplev1.ksRelationField", function (require) {
  "use srtict";

  var RelationalFields = require("web.relational_fields");
  var config = require("web.config");

  RelationalFields.FieldStatus.include({
    _setState: function () {
      this._super.apply(this, arguments);
      if (config.device.isMobile) {
        this.status_information.map((value) => {
          value.fold = true;
        });
      }
    },
  });

  return RelationalFields;
});
