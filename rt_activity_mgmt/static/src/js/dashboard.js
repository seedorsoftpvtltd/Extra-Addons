odoo.define("rt_activity_mgmt.activity_kanban_dashboard_renderer", function (require) {
    "use strict";


    /**
     * This file defines the activity Dashboard view (alongside its renderer, model
     * and controller). This Dashboard is added to the top of list and kanban activity
     * views, it extends both views with essentially the same code except for
     * _onDashboardActionClicked function so we can apply filters without changing our
     * current view.
     */

    var core = require("web.core");
    var KanbanRenderer = require("web.KanbanRenderer");
    var KanbanView = require("web.KanbanView");

    var view_registry = require("web.view_registry");

    var QWeb = core.qweb;

    //--------------------------------------------------------------------------
    // List View
    //--------------------------------------------------------------------------

    var ActivityKanbanDashboardRenderer = KanbanRenderer.extend({

		/**
         * @private
         */
        async _rt_activity_mgmt_get_dashboard_data() {
	            var self = this;
	             await self._rpc({
                    model: "mail.activity",
                    method: "rt_activity_mgmt_retrieve_dashboard",
                    args: [self.state.domain],
                }).then(function (result) {
                    var activity_dashboard = QWeb.render("rt_activity_mgmt.activity_dashboard", {
                        values: result,
                    });
                    self.$el.prepend(activity_dashboard);
                });
		},
        /**
         * @override
         * @private
         * @returns {Promise}
         */
        _renderView: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
				self._rt_activity_mgmt_get_dashboard_data();
            });
        },
    });

    var ActivityKanbanDashboardView = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Renderer: ActivityKanbanDashboardRenderer,
        }),
    });



    view_registry.add("rt_activity_mgmt_activity_kanban_dashboard", ActivityKanbanDashboardView);

    return {
        ActivityKanbanDashboardRenderer: ActivitykanbanDashboardRenderer,
    };
});