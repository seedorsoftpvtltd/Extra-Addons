odoo.define('modern_dashboard_odoo_axis_bookseedor.CrmDashboard',  function (require) {
"use strict";
var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var rpc = require('web.rpc');
var ActionManager = require('web.ActionManager');
var view_registry = require('web.view_registry');
var Widget = require('web.Widget');
var AbstractAction = require('web.AbstractAction');
var ajax = require('web.ajax');
var session = require('web.session');
var web_client = require('web.web_client');

var _t = core._t;
var QWeb = core.qweb;

var MyCustomCrm = AbstractAction.extend({
    template: 'CrmDashboardView',
    cssLibs: [
        '/modern_dashboard_odoo_axis_bookseedor/static/src/scss/lib/nv.d3.css'
    ],
    jsLibs: [
        '/modern_dashboard_odoo_axis_bookseedor/static/src/js/lib/d3.min.js',
        '/modern_dashboard_odoo_axis_bookseedor/static/src/js/lib/charts/chart.js',
       
    ],
    events: {
        'click .more-my-pipeline': 'action_my_pipeline',
        'click .more-overdue-opportunity': 'action_overdue_opportunity',
        'click .more-open-opportunity': 'action_open_opportunity',
        'click .more-won-count': 'action_won_count',
        'click .more-loss-count': 'action_loss_count',
        'change .top_leads': 'get_top_leads',
        'change .custommer_list': 'get_top_customer',
        'change .won_data': 'get_won_data',
        'change .activity_type_list': 'get_activity_data',
        'change .loss_data': 'get_loss_data',
        'click #color_filter_crm': 'graph',
        'click #color_filter_crm1': 'graph_won',
        'click #color_filter_crm3': 'graph_loss',
        'click #color_filter_crm4': 'render_won_list_customer',
        'click #color_filter_crm5': 'render_loss_list_customer',
        'click #color_filter_crm6': 'render_team_sale',
        'click #total_expected_pdf': function(){this.total_expected_pdf("bar")},
        'click #customer_won_pdf': function(){this.customer_won_pdf("pie")},
        'click #customer_loss_pdf': function(){this.customer_loss_pdf("line")},
        'click #sale_team_pdf': function(){this.sale_team_pdf("pie")},
        'click #won_list_customer_pdf': function(){this.won_list_customer_pdf("pie")},
        'click #loss_list_customer_pdf': function(){this.loss_list_customer_pdf("pie")},
    
    },

    init: function (parent,context,result) {
        this._super(parent,context);
        
    },

    willStart: function() {
        var self = this;
            return self.fetch_data();
    },

    start: function() {
        var self = this;
        self.get_top_leads();
        self.get_won_data();
        self.get_activity_data();
        self.get_loss_data();
        self.render_dashboards();
        self.render_graphs();
        self.get_top_customer();
        return this._super();
    },

    fetch_data: function() {
        var self = this;
        var crm_dashboard =  this._rpc({
                model: 'crm.lead',
                method: 'get_crm_lead',
        }).then(function(result) {
            self.employee_data = result;

        });
        return crm_dashboard
    },

    reload: function () {
            window.location.href = this.href;
    },
    

    render_dashboards: function() {
        var self = this;     
        var crm_dashboard = QWeb.render('CrmDashboardView', {
            widget: self,
        });
        rpc.query({
                model: 'crm.lead',
                method: 'get_crm_list',
                args: []
            })
            .then(function (result){
            		self.$el.find('.won-count').text(result['total_won'])
            		self.$el.find('.loss-count').text(result['total_loss'])
            		self.$el.find('.my-pipeline').text(result['my_pipeline'])
            		self.$el.find('.overdue-opportunities').text(result['overdue_opportunities'])
            		self.$el.find('.open-opportunities').text(result['open_opportunities'])
                    self.$el.find('.total-revenue').text(result['total_revenue'])
                    self.$el.find('.total-lead').text(result['total_leads'])
                  
                
            });
        
        return crm_dashboard
    },

    action_my_pipeline: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("My Pipeline"),
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'kanban'],[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_assigned_to_me':true,                   
                    },
            search_view_id: self.crm_search_view_id,
            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });


    },
    action_overdue_opportunity: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Overdue Opportunity"),
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'kanban'],[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_overdue_opportunities':true,                   
                    },
            search_view_id: self.crm_search_view_id,
            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });


    },
    action_open_opportunity: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Open Oppoertunity"),
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'kanban'],[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_open_opportunities':true,                   
                    },
          
            domain: [['type','=', 'opportunity'],['probability','<',100]],
            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });


    },

    action_won_count: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Won Count"),
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'kanban'],[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_won_count':true,                   
                    },
           
            domain: [['active','=', 1],['probability','=',100]],
            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });


    },

    action_loss_count: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Loss Count"),
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'kanban'],[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_lost_count':true,                   
                    },
            
            domain: [['active','=', 0],['probability','=',0]],

            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });
    },

    export_csv : function(csv, filename){
        var csvFile;
        var downloadLink;
        csvFile = new Blob([csv], {type: "text/csv"});
        downloadLink = document.createElement("a");
        downloadLink.download = filename;
        downloadLink.href = window.URL.createObjectURL(csvFile);
        downloadLink.style.display = "none";
        document.body.appendChild(downloadLink);
        downloadLink.click();
    },

    get_top_leads : function(value){
            var self = this;

            rpc.query({
                model: 'crm.lead',
                method: 'get_crm_table',
                args : []
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.top_leads_list');
                    contents.empty();
                    var res = result['crm_tables']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].lead_name, res[i].planned_revenue,res[i].probability,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.top_leads_list').DataTable( {
                            lengthChange : false,
                            info: false,
                            "destroy": true,
                            "responsive": false,
                            pagingType: 'simple',
                            "pageLength": 8,
                            language: {
                                paginate: {
                                    next: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-right" /></button>',
                                    previous: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-left" /></button>'
                                }
                            },
                            searching: true,
                            data: dataSet,
                            columns: [
                                { title: "Leads/Opportunity Name" },
                                { title: "Planned Revenue" },
                                { title: "Probability" }
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#topleadcsv');
                    exp_csv.click(function(){        
                        var html = document.getElementById("topleadtable").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#topleadtable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
                    var exp_xls = self.$el.find('#topleadxls');
                    exp_xls.click(function(){
                        var dt = new Date();
                        var day = dt.getDate();
                        var month = dt.getMonth() + 1;
                        var year = dt.getFullYear();
                        var hour = dt.getHours();
                        var mins = dt.getMinutes();
                        var postfix = day + "." + month + "." + year + "_" + hour + "." + mins;
                        var a = document.createElement('a');
                        var data_type = 'data:application/vnd.ms-excel;charset=utf-8';
                        var table_html = $('#topleadtable')[0].outerHTML;
                        table_html = table_html.replace(/<tfoot[\s\S.]*tfoot>/gmi, '');
                        var css_html = '<style>td {border: 0.5pt solid #c0c0c0} .tRight { text-align:right} .tLeft { text-align:left} </style>';
                        a.href = data_type + ',' + encodeURIComponent('<html><head>' + css_html + '</' + 'head><body>' + table_html + '</body></html>');
                        a.download = 'exported_table_' + postfix + '.xls';
                        a.click();
                    });
                }
            });
        },

    get_top_customer : function(value){
            var self = this;

            rpc.query({
                model: 'crm.lead',
                method: 'get_crm_table',
                args : []
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.top_customer');
                    contents.empty();
                    var res = result['calculate']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].partner_name,,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.top_customer').DataTable( {
                            lengthChange : false,
                            info: false,
                            "destroy": true,
                            "responsive": false,
                            pagingType: 'simple',
                            "pageLength": 8,
                            language: {
                                paginate: {
                                    next: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-right" /></button>',
                                    previous: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-left" /></button>'
                                }
                            },
                            searching: true,
                            data: dataSet,
                            columns: [
                                { title: "Partner Name" },
                               
                            ]
                        });
                    }
                }
            });
        },

    get_activity_data : function(value){
            var self = this;

            rpc.query({
                model: 'crm.lead',
                method: 'get_crm_table',
                args : []
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.activity_type');
                    contents.empty();
                    var res = result['calculate_type']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].activity_name,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.activity_type').DataTable( {
                            lengthChange : false,
                            info: false,
                            "destroy": true,
                            "responsive": false,
                            pagingType: 'simple',
                            "pageLength": 8,
                            language: {
                                paginate: {
                                    next: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-right" /></button>',
                                    previous: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-left" /></button>'
                                }
                            },
                            searching: true,
                            data: dataSet,
                            columns: [
                                { title: "Activity Name" },
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#activitycsv');
                    exp_csv.click(function(){        
                        var html = document.getElementById("activitytable").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#activitytable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
                    var exp_xls = self.$el.find('#activityxls');
                    exp_xls.click(function(){
                        var dt = new Date();
                        var day = dt.getDate();
                        var month = dt.getMonth() + 1;
                        var year = dt.getFullYear();
                        var hour = dt.getHours();
                        var mins = dt.getMinutes();
                        var postfix = day + "." + month + "." + year + "_" + hour + "." + mins;
                        var a = document.createElement('a');
                        var data_type = 'data:application/vnd.ms-excel;charset=utf-8';
                        var table_html = $('#activitytable')[0].outerHTML;
                        table_html = table_html.replace(/<tfoot[\s\S.]*tfoot>/gmi, '');
                        var css_html = '<style>td {border: 0.5pt solid #c0c0c0} .tRight { text-align:right} .tLeft { text-align:left} </style>';
                        a.href = data_type + ',' + encodeURIComponent('<html><head>' + css_html + '</' + 'head><body>' + table_html + '</body></html>');
                        a.download = 'exported_table_' + postfix + '.xls';
                        a.click();
                    });
                }
            });
        },

    get_won_data : function(value){
            var self = this;
            rpc.query({
                model: 'crm.lead',
                method: 'get_crm_table',
                args : []
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.won_count');
                    contents.empty();
                    var res = result['calculate_won']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].lead_name,res[i].probability,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.won_count').DataTable( {
                            lengthChange : false,
                            info: false,
                            "destroy": true,
                            "responsive": false,
                            pagingType: 'simple',
                            "pageLength": 8,
                            language: {
                                paginate: {
                                    next: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-right" /></button>',
                                    previous: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-left" /></button>'
                                }
                            },
                            searching: true,
                            data: dataSet,
                            columns: [
                                { title: "Leads/Opportunity Name" },
                                { title: "Probability" }
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#woncountcsv');
                    exp_csv.click(function(){        
                        var html = document.getElementById("top_sold").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#woncounttable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
                    var exp_xls = self.$el.find('#woncountxls');
                    exp_xls.click(function(){
                        var dt = new Date();
                        var day = dt.getDate();
                        var month = dt.getMonth() + 1;
                        var year = dt.getFullYear();
                        var hour = dt.getHours();
                        var mins = dt.getMinutes();
                        var postfix = day + "." + month + "." + year + "_" + hour + "." + mins;
                        var a = document.createElement('a');
                        var data_type = 'data:application/vnd.ms-excel;charset=utf-8';
                        var table_html = $('#woncounttable')[0].outerHTML;
                        table_html = table_html.replace(/<tfoot[\s\S.]*tfoot>/gmi, '');
                        var css_html = '<style>td {border: 0.5pt solid #c0c0c0} .tRight { text-align:right} .tLeft { text-align:left} </style>';
                        a.href = data_type + ',' + encodeURIComponent('<html><head>' + css_html + '</' + 'head><body>' + table_html + '</body></html>');
                        a.download = 'exported_table_' + postfix + '.xls';
                        a.click();
                    });

                }
            });
        },

    get_loss_data : function(value){
            var self = this;
            rpc.query({
                model: 'crm.lead',
                method: 'get_crm_table',
                args : []
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.loss_count');
                    contents.empty();
                    var res = result['calculate_loss']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].lead_name,res[i].probability,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.loss_count').DataTable( {
                            lengthChange : false,
                            info: false,
                            "destroy": true,
                            "responsive": false,
                            pagingType: 'simple',
                            "pageLength": 8,
                            language: {
                                paginate: {
                                    next: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-right" /></button>',
                                    previous: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-left" /></button>'
                                }
                            },
                            searching: true,
                            data: dataSet,
                            columns: [
                                { title: "Leads/Opportunity Name" },
                                { title: "Probability" }
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#losscountcsv');
                    exp_csv.click(function(){        
                        var html = document.getElementById("top_sold").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#losscounttable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
                    var exp_xls = self.$el.find('#losscountxls');
                    exp_xls.click(function(){
                       var dt = new Date();
                        var day = dt.getDate();
                        var month = dt.getMonth() + 1;
                        var year = dt.getFullYear();
                        var hour = dt.getHours();
                        var mins = dt.getMinutes();
                        var postfix = day + "." + month + "." + year + "_" + hour + "." + mins;
                        var a = document.createElement('a');
                        var data_type = 'data:application/vnd.ms-excel;charset=utf-8';
                        var table_html = $('#losscounttable')[0].outerHTML;
                        table_html = table_html.replace(/<tfoot[\s\S.]*tfoot>/gmi, '');
                        var css_html = '<style>td {border: 0.5pt solid #c0c0c0} .tRight { text-align:right} .tLeft { text-align:left} </style>';
                        a.href = data_type + ',' + encodeURIComponent('<html><head>' + css_html + '</' + 'head><body>' + table_html + '</body></html>');
                        a.download = 'exported_table_' + postfix + '.xls';
                        a.click();
                    });
                }
            });
        },



    render_graphs: function(){
        var self = this;
            self.graph();
            self.render_team_sale();
            self.render_won_list_customer();  
            self.render_loss_list_customer(); 
            self.graph_won();  
            self.graph_loss();  
            self.render_r_customer();


    },
    convertcharttocsv: function (args) {
        var result, ctr, keys, columnDelimiter, lineDelimiter, data;
          data = args.data || null;
          if (data == null || !data.length) {
            return null;
          }
          columnDelimiter = args.columnDelimiter || ',';
          lineDelimiter = args.lineDelimiter || '\n';
          keys = Object.keys(data[0]);
          result = '';
          result += keys.join(columnDelimiter);
          result += lineDelimiter;
          data.forEach(function(item) {
            ctr = 0;
            keys.forEach(function(key) {
              if (ctr > 0) result += columnDelimiter;
              result += item[key];
              ctr++;
            });
            result += lineDelimiter;
          });
          return result;
    },
    exportcsv: function (args) {
        var self = this;
        var data, filename, link;
          var csv = "";
          for(var i = 0; i < args.chart.config.data.dataPoints.length; i++){
            csv = self.convertcharttocsv({
              data: args.chart.config.data.dataPoints
            });
          }
          if (csv == null) {
            return;
        }
        filename = args.filename || 'chart-data.csv';
        if (!csv.match(/^data:text\/csv/i)) {
            csv = 'data:teCustomerxt/csv;charset=utf-8,' + csv;
          }
          data = encodeURI(csv);
          link = document.createElement('a');
          link.setAttribute('href', data);
          link.setAttribute('download', filename);
          document.body.appendChild(link); // Required for FF
            link.click(); 
            document.body.removeChild(link);  
    },

    getRandomColor: function () {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    },



    
    
    graph_won: function() {
        var self = this
        var color = this.$el.find('#color_filter_crm1').val();
        
        if (color == 'cool'){
            $('.customer_won_d').addClass('cool_color');
        }
        else {
            $('.customer_won_d').addClass('warm_color');
        }
        var ctx = this.$el.find('#customer')
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
                model: 'crm.lead',
                method: 'get_probability',
            })
            .then(function (result) {
                var get_data=[];
                for (var i = 0;i < result.payroll_label.length; i++) {
                    var dict = {};
                    var key  = result.payroll_label[i];
                    var val = result.payroll_dataset[i];
                    dict['Customer'] =  key;
                    dict['Total'] =  val;
                    get_data[i] = dict;
                }
                var chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    //labels: ["January","February", "March", "April", "May", "June", "July", "August", "September",
                    // "October", "November", "December"],
                    labels: result.payroll_label,
                    datasets: [{
                        label: 'Probability',
                        data: result.payroll_dataset,
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
                    }],
                    dataPoints: get_data
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                min: 0,
                                max: Math.max.apply(null,result.payroll_dataset),
                                //min: 1000,
                                //max: 100000,
                                stepSize: result.
                                payroll_dataset.reduce((pv,cv)=>{return pv + (parseFloat(cv)||0)},0)
                                /result.payroll_dataset.length
                              }
                        }]
                    },
                    responsive: true,
                    maintainAspectRatio: true,
                    legend: {
                        display: true,
                        labels: {
                            fontColor: 'black'
                        }
                },
            },
        });
        var csv_file = self.$el.find('#topcustomcsv');
        csv_file.click(function(){
            self.exportcsv({ filename: "chart-data.csv", chart: chart })
        });
            });

    
    },


    graph_loss: function() {
        var self = this
        var color = this.$el.find('#color_filter_crm3').val();
        
        if (color == 'cool'){
            $('.customer_loss_i').addClass('cool_color');
        }
        else {
            $('.customer_loss_i').addClass('warm_color');
        }
        var ctx = this.$el.find('#customer_loss')
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
                model: 'crm.lead',
                method: 'get_probability_loss',
                

            })
            .then(function (result) {
                var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    //labels: ["January","February", "March", "April", "May", "June", "July", "August", "September",
                    // "October", "November", "December"],
                    labels: result.payroll_label,
                    datasets: [{
                        label: 'Probability',
                        data: result.payroll_dataset,
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
                                max: Math.max.apply(null,result.payroll_dataset),
                                //min: 1000,
                                //max: 100000,
                                stepSize: result.
                                payroll_dataset.reduce((pv,cv)=>{return pv + (parseFloat(cv)||0)},0)
                                /result.payroll_dataset.length
                              }
                        }]
                    },
                    responsive: true,
                    maintainAspectRatio: true,
                    legend: {
                        display: true,
                        labels: {
                            fontColor: 'black'
                        }
                },
            },
        });

            });

    
    },





    graph: function() {
        var self = this
        var color = this.$el.find('#color_filter_crm').val();
        
        if (color == 'cool'){
            $('.expected_revenue').addClass('cool_color');
        }
        else {
            $('.expected_revenue').addClass('warm_color');
        }
        var ctx = this.$el.find('#Chart')
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
        

        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                //labels: ["January","February", "March", "April", "May", "June", "July", "August", "September",
                // "October", "November", "December"],
                labels: self.employee_data.payroll_label,
                datasets: [{
                    label: 'Expected Revenue',
                    data: self.employee_data.payroll_dataset,
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
                            max: Math.max.apply(null,self.employee_data.payroll_dataset),
                            //min: 1000,
                            //max: 100000,
                            stepSize: self.employee_data.
                            payroll_dataset.reduce((pv,cv)=>{return pv + (parseFloat(cv)||0)},0)
                            /self.employee_data.payroll_dataset.length
                          }
                    }]
                },
                responsive: true,
                maintainAspectRatio: true,
                legend: {
                    display: true,
                    labels: {
                        fontColor: 'black'
                    }
                },
            },
        });
       

    },


    render_team_sale: function() {
        var self = this
        var color = this.$el.find('#color_filter_crm6').val();
        
        if (color == 'cool'){
            $('.sale_team_i').addClass('cool_color');
        }
        else {
            $('.sale_team_i').addClass('warm_color');
        }
        var piectx = this.$el.find('#sale_team')
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
                model: 'crm.lead',
                method: 'get_crm_team_sale',
            })
            .then(function (result) {
                
                    bg_color_list = []
                    for (var i=0;i<=result.payroll_dataset.length;i++){
                        bg_color_list.push(self.getRandomColor())
                    }
                    var pieChart = new Chart(piectx, {
                        type: 'doughnut',
                        data: {
                            datasets: [{
                                data: result.payroll_dataset,
                                backgroundColor: bg_color_list,
                                label: 'Attendance Pie'
                            }],
                            labels:result.payroll_label,
                        },
                        options: {
                            responsive: true
                        }
                    });
            });

            },







    render_won_list_customer: function() {
        var self = this
        var color = this.$el.find('#color_filter_crm4').val();
        
        if (color == 'cool'){
            $('.customer_won_list').addClass('cool_color');
        }
        else {
            $('.customer_won_list').addClass('warm_color');
        }
        var piectx = this.$el.find('#won_list')
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
                model: 'crm.lead',
                method: 'get_won_list',
            })
            .then(function (result) {
                
                    bg_color_list = []
                    for (var i=0;i<=result.payroll_dataset.length;i++){
                        bg_color_list.push(self.getRandomColor())
                    }
                    var pieChart = new Chart(piectx, {
                        type: 'doughnut',
                        data: {
                            datasets: [{
                                data: result.payroll_dataset,
                                backgroundColor: bg_color_list,
                                label: 'Attendance Pie'
                            }],
                            labels:result.payroll_label,
                        },
                        options: {
                            responsive: true
                        }
                    });
            });

            },


    render_r_customer: function() {
        var self = this
        var color = this.$el.find('#color_filter5').val();
        
        if (color == 'cool'){
            $('.rent_order').addClass('cool_color');
        }
        else {
            $('.rent_order').addClass('warm_color');
        }
        var piectx = this.$el.find('#r_customer')
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
                model: 'crm.lead',
                method: 'get_recent_customer',
            })
            .then(function (result) {
                
                    bg_color_list = []
                    for (var i=0;i<=result.payroll_dataset.length;i++){
                        bg_color_list.push(self.getRandomColor())
                    }
                    var pieChart = new Chart(piectx, {
                        type: 'doughnut',
                        data: {
                            datasets: [{
                                data: result.payroll_dataset,
                                backgroundColor: bg_color_list,
                                label: 'Attendance Pie'
                            }],
                            labels:result.payroll_label,
                        },
                        options: {
                            responsive: true
                        }
                    });
            });

            },


   render_loss_list_customer: function() {
        var self = this
        var color = this.$el.find('#color_filter_crm5').val();
        if (color == 'cool'){
            $('.customer_loss_list').addClass('cool_color');
        }
        else {
            $('.customer_loss_list').addClass('warm_color');
        }
        var piectx = this.$el.find('#loss_list')
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
                model: 'crm.lead',
                method: 'get_loss_list',
            })
            .then(function (result) {
                
                    bg_color_list = []
                    for (var i=0;i<=result.payroll_dataset.length;i++){
                        bg_color_list.push(self.getRandomColor())
                    }
                    var pieChart = new Chart(piectx, {
                        type: 'doughnut',
                        data: {
                            datasets: [{
                                data: result.payroll_dataset,
                                backgroundColor: bg_color_list,
                                label: 'Attendance Pie'
                            }],
                            labels:result.payroll_label,
                        },
                        options: {
                            responsive: true
                        }
                    });
            });

            },

   total_expected_pdf: function(chart) {
        if (chart == 'bar'){
            var canvas = document.querySelector('#Chart');
        }
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('total_revenue.pdf');
    },

    customer_won_pdf: function(chart) {
        var canvas = document.querySelector('#customer');
    
      
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('customer_won.pdf');
    },

    customer_loss_pdf: function(chart) {
        
        var canvas = document.querySelector('#customer_loss');
        
      
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('customer_loss.pdf');
    },
    
    sale_team_pdf: function(chart) {
        var canvas = document.querySelector('#sale_team');
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('sale_team.pdf');
    },

    won_list_customer_pdf: function(chart) {
        var canvas = document.querySelector('#won_list');
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('won_list_customer.pdf');
    },

    loss_list_customer_pdf: function(chart) {
        var canvas = document.querySelector('#loss_list');
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('loss_list_customer.pdf');
    },

   
        
             
});


core.action_registry.add("crm_dashboard_action", MyCustomCrm);
return MyCustomCrm
});