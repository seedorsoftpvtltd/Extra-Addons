odoo.define('modern_dashboard_odoo_axis_affinity.dashboard_view',  function (require) {
"use strict";
	
	var AbstractAction = require('web.AbstractAction');
	var core = require('web.core');
	var rpc = require('web.rpc');
	var ajax = require('web.ajax');
	var _t = core._t;
	var QWeb = core.qweb;
	
	var CustomDashboard = AbstractAction.extend({
		hasControlPanel: false,
		jsLibs: [
	        '/modern_dashboard_odoo_axis_affinity/static/src/js/lib/gridstack.all.js',

	    ],
 		events: {
			'click .dashboard_add_view': '_onAddItemclick',
        	'click .dashboard_edit_layout': '_onEditClickEvent',
        	'click .dashboard_saved_layout': '_onSaveClickEvent',
        	'click .dashboard_cancel_layout': '_onCancelClickEvent',

		},
		init: function(parent, context) {
	        this._super(parent, context);
	        var self = this;
	        this.all_data = {};
	        this.grid = {};
	        this.gridaxies = {};
	    },
	    willStart: function() {
	        var self = this;
	       	return self.fetch_data();
	    },
	    fetch_data: function() {
	        var self = this;
	        var items = self._rpc({
                model: 'ax_general.dashboard',
                method: 'search_read',
                args: [],
            }).then(function(result){
                self.all_data = result;
                for (var i = 0; i<result.length; i++){
                	self.all_data.axies_value = result[i].grid_axies
                }
            })
	        return items

	    },
	    start: function() {
        	var self = this;
        	self.render_dashboard();
        },
        on_attach_callback: function() {
            var self = this;
            if(self.fetch_data()){
            	self.render_dashboard();
            	if(self.all_data){
            		self._saveLayout();
            	}
            }
        },
        render_dashboard: function(value) {
	        var self = this;
	        var options = {
                float: false,
                animate: true,
                disableDrag: true,
	            disableResize: true,
	        }
	        var main_body_layout = $(QWeb.render('DashboardMainBody',{widget: self}));   
	        self.$el.empty();
	        self.$el.append(main_body_layout);
	        var gridstacklayout = main_body_layout.find('.grid-stack');
	        gridstacklayout.gridstack(options);
            self.grid =  gridstacklayout.data('gridstack');
	        var Values = self.all_data
	        self.RenderDashboardItems(Values);	
	    },

	    RenderDashboardItems: function(Values){
	        var self = this;
	        var content_view ;
	        if(self.all_data.axies_value){
	        	self.gridaxies = JSON.parse(self.all_data.axies_value);
	        }
	        for (var i = 0; i < Values.length; i++){
	            if(self.grid){
		            if(Values){
		                var content_view = QWeb.render('DashboardItemLayout',{
		                	'item':Values[i],
		                });
		                if (Values[i].id in self.gridaxies) {
                            self.grid.addWidget($(content_view), self.gridaxies[Values[i].id].x, self.gridaxies[Values[i].id].y, self.gridaxies[Values[i].id].width, self.gridaxies[Values[i].id].height, false, 6, null, 2, 2, Values[i].id);
                        } 
                        else {
		                	self.grid.addWidget($(content_view), 0, 0, 8, 2, true, 6, null, 2, 2, Values[i].id);
		                }
		            }
		        }
	        }
	    },
	    
    	_onAddItemclick:function(event){
	        var self = this;
	        event.stopPropagation();
	        event.preventDefault();
	        this.do_action({
	            type: 'ir.actions.act_window',
	            res_model: 'ax_general.dashboard',
	            view_mode: 'form',
	            view_type: 'form',
	            views: [[false, 'form']],
	            target: 'current'
	        });
	    },

	    _onEditClickEvent: function() {
	        var self = this;
	        $('.dashboard_save_layout').removeClass('d-none');
	        $('.dashboard_add_view').addClass('d-none');
	        self._EditLayoutMode();
	    },

	    _EditLayoutMode: function() {
	        var self = this;
	        $('.dashboard_edit_layout').addClass('d-none');
	        self.grid.enable();
	    },

	    _onSaveClickEvent: function() {
	    	var self = this;
	        $('.dashboard_edit_layout').removeClass('d-none');
	        $('.dashboard_save_layout').addClass('d-none');
	        $('.dashboard_add_view').removeClass('d-none');
	        if (self.all_data){
	        	self._saveLayout();
	        }
	        if(self.grid){
			   	$('.grid-stack').data('gridstack').disable();
			}     
	    },

	    _saveLayout: function(){
	    	var self = this;
            if (self.grid){
                var node = self.grid.grid.nodes;
            }
            var grid_data = {};
            if (node){
	            for (var i = 0; i < node.length; i++) {
	                grid_data[node[i].id] = {
	                    'x': node[i].x,
	                    'y': node[i].y,
	     				'width': node[i].width,
	                    'height': node[i].height
	                }
	            }
        	}
        	var keys = Object.keys(grid_data);
			var id = keys[keys.length-1];
        	self.all_data.axies_value = JSON.stringify(grid_data);
     		ajax.jsonRpc('/dashboard/get_data', 'call', {
     				'id':id,
                	'axies_value' : JSON.stringify(grid_data),
                }).then(function (data) {
            });
	    },

	    _onCancelClickEvent: function(){
	    	var self = this;
	    	if(self.grid){
			   	$('.grid-stack').data('gridstack').disable();
			}
	    	$('.dashboard_add_view').removeClass('d-none');
	    	$('.dashboard_edit_layout').removeClass('d-none');
	    	$('.dashboard_save_layout').addClass('d-none');
	    },

	});
	core.action_registry.add("custom_dashboard", CustomDashboard);
	return CustomDashboard
});