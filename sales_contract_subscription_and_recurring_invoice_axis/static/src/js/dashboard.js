odoo.define('sales_contract_subscription_and_recurring_invoice_axis.MyCustomAction',  function (require) {
"use strict";
var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var rpc = require('web.rpc');
var ActionManager = require('web.ActionManager');
var view_registry = require('web.view_registry');
var Widget = require('web.Widget');
var ajax = require('web.ajax');
var session = require('web.session');
var web_client = require('web.web_client');
var _t = core._t;
var QWeb = core.qweb;

var MyCustomAction = AbstractAction.extend({
    template: 'DashboardView',
    cssLibs: [
        '/sales_contract_subscription_and_recurring_invoice_axis/static/src/css/nv.d3.css'
    ],
    jsLibs: [
        '/sales_contract_subscription_and_recurring_invoice_axis/static/src/js/Chart.js',
    ],
    events: {
        'click .more-new-contract': 'action_new_contract_view',
        'click .more-running-contract': 'action_running_contract_view',
        'click .more-expiry-sson-contract': 'action_expiry_soon_contract_view',
        'click .more-expired-contract':'action_expired_contract_view',
        'click .more-locked-contract': 'action_locked_contract_view',
        'click .more-total-contract': 'action_total_contract_view',   
        'click .total_product': 'action_total_product',   
        'click .total_invoice': 'action_total_invoice',   
    },

    init: function(parent, context) {
        this._super(parent, context);
        var self = this;    
    },

    start: function() {    	
        var self = this;
        self.render_dashboards();
        self.render_graphs();
        return this._super();   
    },

    render_dashboards: function(value) {
        var self = this;     
        var dashboard = QWeb.render('DashboardView', {
            widget: self,
        });

        rpc.query({
                model: 'account.analytic.account',
                method: 'get_count_list',
                args: []
            })
            .then(function (result){
                    self.$el.find('.total-contract').text(result['total_contract'])
                    self.$el.find('.new-contract').text(result['new_contract'])
                    self.$el.find('.running-contract').text(result['running_contract'])
                    self.$el.find('.expiry-soon-contract').text(result['expiry_soon_contract'])
                    self.$el.find('.expired-contract').text(result['expired_contract'])
                    self.$el.find('.locked-contract').text(result['locked_contract'])                 
                    self.$el.find('.total-product').text(result['total_product'])                 
                    self.$el.find('.total-invoice').text(result['total_invoice'])                 
                    self.$el.find('.total-customer').text(result['total_customer'])                 
            });
        
        return dashboard
    },

    action_new_contract_view:function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("New Contract"),
            type: 'ir.actions.act_window',
            res_model: 'account.analytic.account',
            view_mode: 'list,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['state','in',['new']]],
            target: 'current'
        },)
    },
    action_running_contract_view:function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Running Contract"),
            type: 'ir.actions.act_window',
            res_model: 'account.analytic.account',
            view_mode: 'list,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['state','in',['running']]],
            target: 'current'
        },)
    },
    action_expiry_soon_contract_view:function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Expiry Soon Contract"),
            type: 'ir.actions.act_window',
            res_model: 'account.analytic.account',
            view_mode: 'list,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['state','in',['expiry_soon']]],
            target: 'current'
        },)
    },
    action_expired_contract_view:function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Expired Contract"),
            type: 'ir.actions.act_window',
            res_model: 'account.analytic.account',
            view_mode: 'list,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['state','in',['expired']]],
            target: 'current'
        },)
    },
    action_locked_contract_view:function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Locked Contract"),
            type: 'ir.actions.act_window',
            res_model: 'account.analytic.account',
            view_mode: 'list,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['state','in',['locked']]],
            target: 'current'
        },)
    },
    action_total_contract_view:function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Total Contract"),
            type: 'ir.actions.act_window',
            res_model: 'account.analytic.account',
            view_mode: 'list,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            target: 'current'
        },)
    },
    action_total_product:function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Total Contract Product"),
            type: 'ir.actions.act_window',
            res_model: 'product.template',
            view_mode: 'list,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['contract_warranty','=',true]],
            target: 'current'
        },)
    },
    action_total_invoice:function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Total Invoice"),
            type: 'ir.actions.act_window',
            res_model: 'account.move',
            view_mode: 'list,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            target: 'current'
        },)
    },

    
    getRandomColor: function () {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    },

    render_graphs: function(){
        var self = this;
        self.weekly_contract();
        self.monthly_contract();
    },

    weekly_contract: function() {
        var self = this;
        var ctx = this.$el.find('#weekcontract')
        Chart.plugins.register({
          beforeDraw: function(chartInstance) {
            var ctx = chartInstance.chart.ctx;
            ctx.fillStyle = "white";
            ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
          }
        });
        var bg_color_list = []
        for (var i=0;i<=12;i++){
            bg_color_list.push(self.getRandomColor())
        }
        rpc.query({
                model: 'account.analytic.account',
                method: 'get_week_contract',
                
            })
            .then(function (result) {
                var data = result.data;
                var day = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                         "Friday", "Saturday", "Sunday"]
                var week_data = [];
                if (data){
                    for(var i = 0; i < day.length; i++){
                        day[i] == data[day[i]]
                        var day_data = day[i];
                        var day_count = data[day[i]];
                        if(!day_count){
                                day_count = 0;
                        }
                        week_data[i] = day_count

                    }
                }
                              
                

                var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                   
                    labels: day ,
                    datasets: [{
                        label: ' Contract',
                        data: week_data,
                        backgroundColor: bg_color_list,
                        borderColor: bg_color_list,
                        borderWidth: 1,
                        pointBorderColor: 'white',
                        pointBackgroundColor: 'red',
                        pointRadius: 5,
                        pointHoverRadius: 10,
                        pointHitRadius: 30,
                        pointBorderWidth: 2,
                        pointStyle: 'rectRounded'
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                min: 0,
                                max: Math.max.apply(null,week_data),
                              }
                        }]
                    },
                    responsive: true,
                    maintainAspectRatio: true,
                    leged: {
                        display: true,
                        labels: {
                            fontColor: 'black'
                        }
                },
            },
        });

            });
    },

    monthly_contract: function() {
        var self = this;
        var ctx = this.$el.find('#monthlycontract')
        Chart.plugins.register({
          beforeDraw: function(chartInstance) {
            var ctx = chartInstance.chart.ctx;
            ctx.fillStyle = "white";
            ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
          }
        });
        var bg_color_list = []
        for (var i=0;i<=12;i++){
            bg_color_list.push(self.getRandomColor())
        }
        rpc.query({
                model: 'account.analytic.account',
                method: 'get_monthly_contract',
            })
            .then(function (result) {
                var data = result.data
                var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                                'August', 'September', 'October', 'November', 'December']
                var month_data = [];

                if (data){
                    for(var i = 0; i < months.length; i++){
                        months[i] == data[months[i]]
                        var day_data = months[i];
                        var month_count = data[months[i]];
                        if(!month_count){
                                month_count = 0;
                        }
                        month_data[i] = month_count

                    }
                }
                var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                   
                    labels: months,
                    datasets: [{
                        label: ' Contract',
                        data: month_data,
                        backgroundColor: bg_color_list,
                        borderColor: bg_color_list,
                        borderWidth: 1,
                        pointBorderColor: 'white',
                        pointBackgroundColor: 'red',
                        pointRadius: 1,
                        pointHoverRadius: 10,
                        pointHitRadius: 30,
                        pointBorderWidth: 1,
                        pointStyle: 'rectRounded'
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                min: 0,
                                max: Math.max.apply(null,month_data),
                              }
                        }]
                    },
                    responsive: true,
                    maintainAspectRatio: true,
                    leged: {
                        display: true,
                        labels: {
                            fontColor: 'black'
                        }
                    },
                },
            });
        });    
    },
           
});


core.action_registry.add("dashboard", MyCustomAction);
return MyCustomAction
});