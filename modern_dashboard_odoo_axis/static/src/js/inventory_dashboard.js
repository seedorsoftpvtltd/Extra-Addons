odoo.define('modern_dashboard_odoo_axis.InventoryDashboard',  function (require) {
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

var InventoryDashboardACtion = AbstractAction.extend({
    template: 'InventoryDashboardView',
    cssLibs: [
        '/modern_dashboard_odoo_axis/static/src/scss/lib/nv.d3.css'
    ],
    jsLibs: [
        '/modern_dashboard_odoo_axis/static/src/js/lib/d3.min.js',
        '/modern_dashboard_odoo_axis/static/src/js/lib/charts/chart.js',
       
    ],
    events: {
    	'click .more-assigned-count': 'action_assigned_count',
        'click .more-delivery-order': 'action_delivery_order',
        'click .more-waiting-count': 'action_waiting_count',
        'change .delivery_record': 'get_delivery_record',
        'change .sell_product_record': 'get_sell_product_record',
        'change .lots_data': 'action_get_lots_data',
        'click #delivery_filter': 'render_delivery_order',
        'click #product_moves': 'render_product_moves',
        'click #stock_moves': 'render_stock_moves',
        'click #internal_transfer': 'render_internal_transfer',
         'click #color_filter7': 'render_selling_product',
        'click #color_filter1': 'render_delivery_order',
        'click #color_filter9': 'render_product_moves',
        'click #color_filter8': 'render_stock_moves',
        'click #color_filter4': 'render_operation_types',
        'click #color_filter6': 'render_inventory_report',
          'click #internal_transfer_info': function(){this.internal_transfer_info("bar")},
        'click #reserved_stock_info': function(){this.reserved_stock_info("pie")},
        'click #open_outward_data_pdf': function(){this.open_outward_data_pdf("line")},
        'click #in_outward_data_pdf': function(){this.in_outward_data_pdf("pie")},
        'click #operation_type_pdf': function(){this.operation_type_pdf("pie")},
        'click #product_moves_pdf': function(){this.product_moves_pdf("pie")},
        'click #stock_move_data_pdf': function(){this.stock_move_data_pdf("pie")},
        'click #stock_move_data_pdf': function(){this.stock_move_data_pdf("pie")},
        'click #stock_move_data_pdf': function(){this.stock_move_data_pdf("pie")},
        'click #inventory_dashboard_pdf': function(){this.inventory_dashboard_pdf("pie")},
    },

     init: function (parent,context,result) {
        this._super(parent,context);
        var inventory_data = [];
        self.inventory_data = result[0]
        
    },

    willStart: function() {
        var self = this;
            return self.fetch_data();
    },

    start: function() {
        var self = this;
        self.get_delivery_record();
        self.get_sell_product_record();
        self.action_get_lots_data();
        self.render_graphs();
        return this._super();
    },

    fetch_data: function() {
        var self = this;
        var inventory_dashboard =  this._rpc({
                model: 'stock.picking',
                method: 'get_stock_list',
        }).then(function(result) {
            self.render_dashboards();
            self.href = window.location.href;

        });
        return inventory_dashboard
    },
    reload: function () {
            window.location.href = this.href;
    },
    

    render_dashboards: function() {
        var self = this;     
        var inventory_dashboard = QWeb.render('InventoryDashboardView', {
            widget: self,
        });
        rpc.query({
                model: 'stock.picking',
                method: 'get_stock_picking_list',
                args: []
            })
            .then(function (result){
            		self.$el.find('.assigned').text(result['total_assigned'])
            		self.$el.find('.done').text(result['total_done'])
            		self.$el.find('.waiting').text(result['total_waiting'])
            		self.$el.find('.lot-serial').text(result['total_lot_serial'])
            		self.$el.find('.total-reordering').text(result['total_reordering_rules'])
                    self.$el.find('.total-internal').text(result['total_internal_transfer'])   
                
            });
        
        return inventory_dashboard
    },

    action_assigned_count: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Assigned Count"),
            type: 'ir.actions.act_window',
            res_model: 'stock.picking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_assigned_count':true,                   
                    },
            
            domain: [['state','in',['assigned']]],

            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });


    },
    action_delivery_order: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Delivery Orders"),
            type: 'ir.actions.act_window',
            res_model: 'stock.picking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_delievery_orders':true,                   
                    },
            
            domain: [['state','in',['done']]],

            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });


    },

    action_waiting_count: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Waiting Count"),
            type: 'ir.actions.act_window',
            res_model: 'stock.picking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_waiting_count':true,                   
                    },
            
            domain: [['state','in',['confirmed']]],

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
    
    get_delivery_record : function(value){
            var self = this;

            rpc.query({
                model: 'stock.picking',
                method: 'get_inventory_table',
                args : []
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.delivery_data');
                    contents.empty();
                    var res = result['abcd']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].stock_name,res[i].origin,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.delivery_data').DataTable( {
                            lengthChange : false,
                            info: false,
                            "destroy": true,
                            "responsive": false,
                            pagingType: 'simple',
                            "pageLength": 4,
                            language: {
                                paginate: {
                                    next: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-right" /></button>',
                                    previous:'<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-left" /></button>'
                                }
                            },
                            searching: true,
                            data: dataSet,
                            columns: [
                                { title: "Stock Name" },
                                 { title: "Scheduled Date" },
        
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#deliverydataxls');
                    exp_csv.click(function(){        
                        var html = document.getElementById("deliverydatatable").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#deliverydatatable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
                    var exp_xls = self.$el.find('#deliverydataxls');
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
                        var table_html = $('#deliverydatatable')[0].outerHTML;
                        table_html = table_html.replace(/<tfoot[\s\S.]*tfoot>/gmi, '');
                        var css_html = '<style>td {border: 0.5pt solid #c0c0c0} .tRight { text-align:right} .tLeft { text-align:left} </style>';
                        a.href = data_type + ',' + encodeURIComponent('<html><head>' + css_html + '</' + 'head><body>' + table_html + '</body></html>');
                        a.download = 'exported_table_' + postfix + '.xls';
                        a.click();
                    });
                }
            });
        },


    get_sell_product_record : function(value){
            var self = this;

            rpc.query({
                model: 'stock.picking',
                method: 'get_inventory_table',
                args : []
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.sell_data');
                    contents.empty();
                    var res = result['calculate_price']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].product_name,res[i].list_price,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.sell_data').DataTable( {
                            lengthChange : false,
                            info: false,
                            "destroy": true,
                            "responsive": false,
                            pagingType: 'simple',
                            "pageLength": 9,
                            language: {
                                paginate: {
                                    next: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-right" /></button>',
                                    previous: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-left" /></button>'
                                }
                            },
                            searching: true,
                            data: dataSet,
                            columns: [
                                { title: "Product Name" },
                                 { title: "Product Price" },
        
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#selldatacsv');
                    exp_csv.click(function(){        
                        var html = document.getElementById("selldatatable").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#selldatatable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
                    var exp_xls = self.$el.find('#selldataxls');
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
                        var table_html = $('#selldatatable')[0].outerHTML;
                        table_html = table_html.replace(/<tfoot[\s\S.]*tfoot>/gmi, '');
                        var css_html = '<style>td {border: 0.5pt solid #c0c0c0} .tRight { text-align:right} .tLeft { text-align:left} </style>';
                        a.href = data_type + ',' + encodeURIComponent('<html><head>' + css_html + '</' + 'head><body>' + table_html + '</body></html>');
                        a.download = 'exported_table_' + postfix + '.xls';
                        a.click();
                    });
                }
            });
        },





    action_get_lots_data : function(value){
            var self = this;

            rpc.query({
                model: 'stock.picking',
                method: 'get_inventory_table',
                args : []
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.lots_record_list');
                    contents.empty();
                    var res = result['calculate_lot']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].lot_number,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.lots_record_list').DataTable( {
                            lengthChange : false,
                            info: false,
                            "destroy": true,
                            "responsive": false,
                            pagingType: 'simple',
                            "pageLength": 4,
                            language: {
                                paginate: {
                                    next: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-right" /></button>',
                                    previous: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-left" /></button>'
                                }
                            },
                            searching: true,
                            data: dataSet,
                            columns: [
                                { title: "Lots/Serials Number" },
                                ,
        
                            ]
                        });
                    }
                }
            });
        },



    render_graphs: function(){
        var self = this;
            self.render_product_moves();
            self.render_selling_product();
            self.render_internal_transfer();
            self.render_inventory_report();
            self.render_operation_types();
            self.render_delivery_order();
            self.render_product_outward();
            self.render_product_inward();  
            self.render_stock_moves(); 
            self.render_reserved_stock();
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



    render_product_outward: function() {
        var self = this
        var piectx = this.$el.find('#open_outward_data')
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
                model: 'stock.picking',
                method: 'get_open_outwards',
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


    render_product_inward: function() {
        var self = this
        var piectx = this.$el.find('#in_outward_data')
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
                model: 'stock.picking',
                method: 'get_open_inwards',
            })
            .then(function (result) {
                
                    bg_color_list = []
                    for (var i=0;i<=result.payroll_dataset.length;i++){
                        bg_color_list.push(self.getRandomColor())
                    }
                    var pieChart = new Chart(piectx, {
                        type: 'pie',
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

    render_stock_moves: function() {
        var self = this;
        var option = this.$el.find('#stock_moves').val();
        var piectx = this.$el.find('#stock_move_data')
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
                model: 'stock.picking',
                method: 'get_stock_moves',
                args:[option]
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


    render_internal_transfer: function() {
        var self = this;
        var option = this.$el.find('#internal_transfer').val();
        var piectx = this.$el.find('#internal_transfer_data')
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
                model: 'stock.picking',
                method: 'get_internal_transfer',
                args:[option]
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

    render_reserved_stock: function() {
        var self = this
        var ctx = this.$el.find('#reserved_stock_data')
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
                model: 'stock.picking',
                method: 'get_reserved_stock',   

            })
            .then(function (result) {
                var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: result.payroll_label,
                    datasets: [{
                        label: 'Reserved',
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
                            fontColor: 'blue'
                        }
                },
            },
        });

            });

    
    },


 


     render_inventory_report: function() {
        var self = this;
        var ctx = this.$el.find('#inventory_report_data')
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
                model: 'stock.picking',
                method: 'get_inventory_report',   

            })
            .then(function (result) {
                var get_data =[];
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
                    labels: result.payroll_label,
                    datasets: [{
                        label: 'Report',
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
        var csv_file = self.$el.find('#reportcsv');
        csv_file.click(function(){
            self.exportcsv({ filename: "chart-data.csv", chart: chart })
        });

            });

    
    },



    render_selling_product: function() {
        var self = this
        var color = this.$el.find('#color_filter7').val();
        if (color == 'cool'){
            $('.sell_product').addClass('cool_color');
        }
        else {
            $('.sell_product').addClass('warm_color');
        }
        var ctx = this.$el.find('#selling_product_data')
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
                model: 'stock.picking',
                method: 'get_selling_product',   

            })
            .then(function (result) {
                var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: result.payroll_label,
                    datasets: [{
                        label: 'Product',
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


    render_product_moves: function() {
        var self = this;
        var color = this.$el.find('#color_filter9').val();
        if (color == 'cool'){
            $('.product_m').addClass('cool_color');
        }
        else {
            $('.product_m').addClass('warm_color');
        }
        var option = this.$el.find('#product_moves').val();
        var ctx = this.$el.find('#product_move_data')
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
                model: 'stock.picking',
                method: 'get_product_moves',   
                args:[option]
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
                    labels: result.payroll_label,
                    datasets: [{
                        label: 'Done',
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
        var csv_file = self.$el.find('#productcsv');
        csv_file.click(function(){
            self.exportcsv({ filename: "chart-data.csv", chart: chart })
        });

            });

    
    },

    






    render_operation_types: function() {
        var self = this
        var color = this.$el.find('#color_filter4').val();
        if (color == 'cool'){
            $('.operation_type_i').addClass('cool_color');
        }
        else {
            $('.operation_type_i').addClass('warm_color');
        }
        var piectx = this.$el.find('#operation_type')
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
                model: 'stock.picking',
                method: 'get_operations_type',
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



    render_delivery_order: function() {
        var self = this;
        var color = this.$el.find('#color_filter1').val();
        
        if (color == 'cool'){
            $('.delivery_order_info').addClass('cool_color');
        }
        else {
            $('.delivery_order_info').addClass('warm_color');
        }
        var option = this.$el.find('#delivery_filter').val();
        var piectx = this.$el.find('#delivery_order')
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
                model: 'stock.picking',
                method: 'get_delivery_order',
                args:[option]
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
            internal_transfer_info: function(chart) {
        var canvas = document.querySelector('#internal_transfer_data');        
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('internal_transfer_info.pdf');
    },

    product_moves_pdf: function(chart) {
        var canvas = document.querySelector('#product_move_data');        
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('product_move.pdf');
    },

    stock_move_data_pdf: function(chart) {
        var canvas = document.querySelector('#stock_move_data');        
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('stock_move.pdf');
    },

    reserved_stock_info: function(chart) {
        var canvas = document.querySelector('#reserved_stock_data');
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('reserved_stock_data.pdf');
    },

    open_outward_data_pdf: function(chart) {
        var canvas = document.querySelector('#open_outward_data');
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('product_price_report.pdf');
    },
    
    in_outward_data_pdf: function(chart) {
        var canvas = document.querySelector('#in_outward_data');
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('in_outward_data_pdf.pdf');
    },

    operation_type_pdf: function(chart) {
        var canvas = document.querySelector('#operation_type');
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('operation_type.pdf');
    },

    inventory_dashboard_pdf: function(chart) {
        var canvas = document.querySelector('#inventory_report_data');
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('inventory_dashboard.pdf');
    },



   

             
});


core.action_registry.add("inventory_dashboard_action", InventoryDashboardACtion);
return InventoryDashboardACtion
});