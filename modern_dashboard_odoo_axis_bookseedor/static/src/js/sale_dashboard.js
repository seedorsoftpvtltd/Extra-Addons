odoo.define('modern_dashboard_odoo_axis_bookseedor.MyCustomAction',  function (require) {
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
    template: 'SaleDashboardView',
    cssLibs: [
        '/modern_dashboard_odoo_axis_bookseedor/static/src/scss/lib/nv.d3.css'
    ],
    jsLibs: [
        '/modern_dashboard_odoo_axis_bookseedor/static/src/js/lib/d3.min.js',
        '/modern_dashboard_odoo_axis_bookseedor/static/src/js/lib/charts/chart.js',
       
    ],
    events: {
        'click .more-quotation': 'action_quotation',
        'click .more-sale-order': 'action_sales_order',
        'click .more-quotation-sent': 'action_quotation_sent',
        'click .more-cancel':'action_cancel',
        'click .more-customer': 'action_customer',
        'click .more-to-be-invoiced': 'action_to_be_invoiced',
        'click .more-fully-invoiced': 'action_fully_invoiced',
        'change .top_sold_order': 'get_top_sold_order',
        'change .sale_order_cancel': 'get_sale_order_cancel',
        'change .order': 'get_order',
        'change .customer-count': 'get_customer_count',
        'click #sales_filter': 'graph_max_price',
        'click #top_sale_order': 'get_top_sold_order',
        'click #quotation_sale': 'get_order',
        'click #cancel_sale': 'get_sale_order_cancel',
        'change #custom': 'get_top_sold_order',
        'click #color_filter': 'graph_sale',
        'click #color_filter1': 'graph_max_price',
        'click #color_filter2': 'graph',
        'click #color_filter3': 'graph_recent_sale',
        'click #color_filter4': 'render_s_team_graph',
        'click #color_filter5': 'render_r_sale_graph',
        'click #last_sale_order_pdf': function(){this.last_sale_order_pdf("bar")},
        'click #top_recent_customer_pdf': function(){this.top_recent_customer_pdf("pie")},
        'click #product_price_pdf': function(){this.product_price_pdf("line")},
        'click #sale_team_report_pdf': function(){this.sale_team_report_pdf("pie")},
        'click #sale_order_report_pdf': function(){this.sale_order_report_pdf("pie")},
        'click #count_wise_customer_pdf': function(){this.count_wise_customer_pdf("pie")},
       
    },

    
    init: function(parent, context) {
        this._super(parent, context);
        var employee_data = [];
        var self = this;
    },

    willStart: function() {
        var self = this;
            return self.fetch_data();
    },

    start: function() {
    	
        var self = this;
      
        self.get_top_sold_order();
        self.get_sale_order_cancel();
        self.get_order();
        self.get_customer_count();
        self.render_graphs();
        self.render_dashboards();
        return this._super();
        
    },

    fetch_data: function() {
        
        var self = this;
        var abcd = self._rpc({
                model: 'sale.order',
                method: 'get_value',
            }, []).then(function(result){
                self.employee_data = result; 
            })
        
        return abcd

    },

    reload: function () {
            window.location.href = this.href;
    },

 

    render_dashboards: function(value) {
        var self = this;     
        var sale_dashboard = QWeb.render('SaleDashboardView', {
            widget: self,
        });

        rpc.query({
                model: 'sale.order',
                method: 'get_count_list',
                args: []
            })
            .then(function (result){
                    self.$el.find('.total-quotation').text(result['quotation_count'])
                    self.$el.find('.total-sale').text(result['sale_count'])
                    self.$el.find('.total-customer').text(result['partner_count'])
                    self.$el.find('.quotation-sent').text(result['quotation_sent_count'])
                    self.$el.find('.cancel').text(result['cancel_count'])
                    self.$el.find('.count_customer').text(result['count_c'])
                    self.$el.find('.to-be_invoice').text(result['fully_invoice'])
                    self.$el.find('.table').text(result['sale_tables'])                  
            });
        
        return sale_dashboard
    },

    action_quotation:function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Quotation"),
            type: 'ir.actions.act_window',
            res_model: 'sale.order',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_all_quotation':true,                   
                    },
            domain: [['state','in',['draft']]],
            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });


    },

    
    action_sales_order:function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Sales Orders"),
            type: 'ir.actions.act_window',
            res_model: 'sale.order',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_sale_order':true,                   
                    },
            domain: [['state','in',['sale']]],
            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });


    },
    
    action_quotation_sent:function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Quotation Sent"),
            type: 'ir.actions.act_window',
            res_model: 'sale.order',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_quotation_sent':true,                   
                    },
            domain: [['state','in',['sent']]],
            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });


    },

    action_cancel:function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Cancel"),
            type: 'ir.actions.act_window',
            res_model: 'sale.order',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_quotation_cancel':true,                   
                    },
            domain: [['state','in',['cancel']]],
            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });


    },
    action_customer:function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Customer"),
            type: 'ir.actions.act_window',
            res_model: 'sale.order',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['state','in',['cancel']]],
            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });


    },
    action_to_be_invoiced:function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("To be Invoiced"),
            type: 'ir.actions.act_window',
            res_model: 'sale.order',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['state','in',['invoiced']]],
            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });


    },

    action_fully_invoiced:function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Fully  Invoiced"),
            type: 'ir.actions.act_window',
            res_model: 'account.move',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['state','in',['no']]],
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
    
    get_top_sold_order : function(value){
        var option = this.$el.find('#top_sale_order').val();
            var self = this;
            rpc.query({
                model: 'sale.order',
                method: 'get_sale_table',
                args : [option],
            }).then(function (result) {
                if(result){
                    var contents = self.$el.find('.top-sold');
                    contents.empty();
                    var res = result['sale_tables']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].order_reference, res[i].partner_name,res[i].amount,res[i].date_order,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.top-sold').DataTable( {
                            lengthChange : false,
                            info: false,
                            "destroy": true,
                            "responsive": false,
                            pagingType: 'simple',
                            "pageLength": 10,
                            language: {
                                paginate: {
                                    next: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-right" /></button>',
                                    previous: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-left" /></button>'
                                }
                            },
                            searching: true,
                            data: dataSet,
                            columns: [
                                { title: "Order Reference" },
                                { title: "Customer Name" },
                                { title: "Total" },
                                { title: "Creation Order" }
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#exportcsv');
                    var exp_xls = self.$el.find('#exportxls');
                    exp_csv.click(function(){        
                        var html = document.getElementById("top_sold").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#top_sold tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
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
                        var table_html = $('#top_sold')[0].outerHTML;
                        table_html = table_html.replace(/<tfoot[\s\S.]*tfoot>/gmi, '');
                        var css_html = '<style>td {border: 0.5pt solid #c0c0c0} .tRight { text-align:right} .tLeft { text-align:left} </style>';
                        a.href = data_type + ',' + encodeURIComponent('<html><head>' + css_html + '</' + 'head><body>' + table_html + '</body></html>');
                        a.download = 'exported_table_' + postfix + '.xls';
                        a.click();
                    });
                }
            });
        },

    get_sale_order_cancel : function(value){
            var self = this;
            var option = this.$el.find('#cancel_sale').val();
            rpc.query({
                model: 'sale.order',
                method: 'get_cancel_sale_table',
                args : [option]
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.sale-cancel');
                    contents.empty();
                    var res = result['sale_cancel']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].order_reference, res[i].partner_name,res[i].date_order,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.sale-cancel').DataTable( {
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
                                { title: "Order Reference" },
                                { title: "Customer Name" },
                                { title: "Creation Order" }
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#cancelsalecsv');
                    var exp_xls = self.$el.find('#cancelsalexls');
                    exp_csv.click(function(){
                        var html = document.querySelector("table").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#cancelsaletable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), filename);
                    });
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
                        var table_html = $('#cancelsaletable')[0].outerHTML;
                        table_html = table_html.replace(/<tfoot[\s\S.]*tfoot>/gmi, '');
                        var css_html = '<style>td {border: 0.5pt solid #c0c0c0} .tRight { text-align:right} .tLeft { text-align:left} </style>';
                        a.href = data_type + ',' + encodeURIComponent('<html><head>' + css_html + '</' + 'head><body>' + table_html + '</body></html>');
                        a.download = 'exported_table_' + postfix + '.xls';
                        a.click();
                    });
                }
            });
        },


    get_customer_count : function(value){
            var self = this;
            rpc.query({
                model: 'sale.order',
                method: 'get_sale_customer',
                args : []
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.customer');
                    contents.empty();
                    var res = result['count_customer']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].customer_name,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.customer').DataTable( {
                            lengthChange : false,
                            info: false,
                            "destroy": true,
                            "responsive": false,
                            pagingType: 'simple',
                            "pageLength": 10,
                            language: {
                                paginate: {
                                    next: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-right" /></button>',
                                    previous: '<button type="button" class="btn btn-box-tool"><i class="fa fa-angle-left" /></button>'
                                }
                            },
                            searching: true,
                            data: dataSet,
                            columns: [
                                { title: "Customer Name" },
        
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#customercsv');
                    var exp_xls = self.$el.find('#customerxls');
                    exp_csv.click(function(){
                        var html = document.querySelector("table").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#customertable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
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
                        var table_html = $('#customertable')[0].outerHTML;
                        table_html = table_html.replace(/<tfoot[\s\S.]*tfoot>/gmi, '');
                        var css_html = '<style>td {border: 0.5pt solid #c0c0c0} .tRight { text-align:right} .tLeft { text-align:left} </style>';
                        a.href = data_type + ',' + encodeURIComponent('<html><head>' + css_html + '</' + 'head><body>' + table_html + '</body></html>');
                        a.download = 'exported_table_' + postfix + '.xls';
                        a.click();
                    });
                }
            });
        },

    get_order : function(value){
            var self = this;
            var option = this.$el.find('#quotation_sale').val();
            rpc.query({
                model: 'sale.order',
                method: 'get_quotation_table',
                args : [option]
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.sale');
                    contents.empty();
                    var res = result['order']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].order_reference, res[i].partner_name,res[i].date_order,res[i].delievery_date,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.sale').DataTable( {
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
                                { title: "Order Reference" },
                                { title: "Customer Name" },
                                { title: "Creation Order" },
                                { title: "Delivery Date" }
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#quotationcsv');
                    var exp_xls = self.$el.find('#quotationxls');
                    exp_csv.click(function(){
                        var html = document.querySelector("table").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#quotationtable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
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
                        var table_html = $('#quotationtable')[0].outerHTML;
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
            self.graph_max_price();
            self.graph_recent_sale();
            self.graph_sale();
            self.graph_top_salesperson();
            self.render_s_team_graph();
            self.render_r_sale_graph();     
    },
    getRandomColor: function () {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
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

  
    graph: function() {
        var self = this
        var color = this.$el.find('#color_filter2').val();
        if (color == 'cool'){
            $('.count_wise').addClass('cool_color');
        }
        else {
            $('.count_wise').addClass('warm_color');
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
        var get_data=[];
        for (var i = 0;i < self.employee_data.payroll_label.length; i++) {
            var dict = {};
            var key  = self.employee_data.payroll_label[i];
            var val = self.employee_data.payroll_dataset[i];
            dict['Customer'] =  key;
            dict['Total'] =  val;
            get_data[i] = dict;
        }

        var chart = new Chart(ctx, {
            type: 'bar',
            data: {    
                labels: self.employee_data.payroll_label,
                datasets: [{
                    label: 'Sale Order',
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
                }],
                dataPoints: get_data
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
        var csv_file = self.$el.find('#count_customer_csv');
        csv_file.click(function(){
            self.exportcsv({ filename: "chart-data.csv", chart: chart })
        });
    },

    graph_max_price: function() {
        var self = this;
        var color = this.$el.find('#color_filter1').val();
        if (color == 'cool'){
            $('.high_price').addClass('cool_color');
        }
        else {
            $('.high_price').addClass('warm_color');
        }
        
        var option = this.$el.find('#sales_filter').val();
        var ctx = this.$el.find('#highprice')
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
                model: 'sale.order',
                method: 'get_value_price',
                args: [option],
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
                        label: 'Sale Order',
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
                    dataPoints: get_data,

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
                    legend: {
                        display: true,
                        labels: {
                            fontColor: 'black'
                        }
                },
            },
            });
        var csv_file = self.$el.find('#downloadCSV');
        csv_file.click(function(){
            self.exportcsv({ filename: "chart-data.csv", chart: chart })
        });
        
        });
    },

    graph_recent_sale: function() {
        var self = this
        var color = this.$el.find('#color_filter3').val();
        if (color == 'cool'){
            $('.price_product').addClass('cool_color');
        }
        else {
            $('.price_product').addClass('warm_color');
        }
        var ctx = this.$el.find('#sale_order_generated')
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
                model: 'sale.order',
                method: 'get_recent_sale_order',
                

            })
            .then(function (result) {
                var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                   
                    labels: result.payroll_label,
                    datasets: [{
                        label: 'Product Price',
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
                            fontColor: 'red'
                        }
                },
            },
        });

            });
    },


    graph_sale: function() {
        var self = this
        var color = this.$el.find('#color_filter').val();
        if (color == 'cool'){
            $('.recent_customer').addClass('cool_color');
        }
        else {
            $('.recent_customer').addClass('warm_color');
        }
        
        var piectx = this.$el.find('#top_recent_customer')
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
                model: 'sale.order',
                method: 'get_customer_detail',
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
                                label: 'Customer'
                            }],
                            labels:result.payroll_label,
                        },
                        options: {
                            responsive: true
                        }
                    });
            });

            },


    graph_top_salesperson: function() {
        var self = this
        var piectx = this.$el.find('#top_salesperson')
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
                model: 'sale.order',
                method: 'get_salesperson',
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
                                label: 'Saleperson'
                            }],
                            labels:result.payroll_label,
                        },
                        options: {
                            responsive: true
                        }
                    });
            });

            },


    render_s_team_graph: function() {
        var self = this
        var color = this.$el.find('#color_filter4').val();
        if (color == 'cool'){
            $('.sale_team').addClass('cool_color');
        }
        else {
            $('.sale_team').addClass('warm_color');
        }
        var piectx = this.$el.find('#sale_team_data')
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
                model: 'sale.order',
                method: 'get_sale_team_info',
            })
            .then(function (result) {
                
                    bg_color_list = []
                    for (var i=0;i<=result.st_dataset.length;i++){
                        bg_color_list.push(self.getRandomColor())
                    }
                    var pieChart = new Chart(piectx, {
                        type: 'doughnut',
                        data: {
                            datasets: [{
                                data: result.st_dataset,
                                backgroundColor: bg_color_list,
                                label: 'Sale Team'
                            }],
                            labels:result.st_label,
                        },
                        options: {
                            responsive: true
                        }
                    });
            });

            },


    render_r_sale_graph: function() {
        var self = this
        var color = this.$el.find('#color_filter5').val();
        
        if (color == 'cool'){
            $('.rent_order').addClass('cool_color');
        }
        else {
            $('.rent_order').addClass('warm_color');
        }
        var piectx = this.$el.find('#sale_order_data')
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
                model: 'sale.order',
                method: 'get_r_sale_info',
            })
            .then(function (result) {
                
                    bg_color_list = []
                    for (var i=0;i<=result.r_dataset.length;i++){
                        bg_color_list.push(self.getRandomColor())
                    }
                    var pieChart = new Chart(piectx, {
                        type: 'doughnut',
                        data: {
                            datasets: [{
                                data: result.r_dataset,
                                backgroundColor: bg_color_list,
                                label: 'Recent Sale Order'
                            }],
                            labels:result.r_label,
                        },
                        options: {
                            responsive: true
                        }
                    });
            });

            },
            last_sale_order_pdf: function(chart) {
        if (chart == 'bar'){
            var canvas = document.querySelector('#highprice');
        }
        else if (chart == 'pie') {
            var canvas = document.querySelector('#attendanceChart');
        }

        //creates image
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('report.pdf');
    },

    top_recent_customer_pdf: function(chart) {
        if (chart == 'pie'){
            var canvas = document.querySelector('#top_recent_customer');
        }
      
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('recent_customer_report.pdf');
    },

    product_price_pdf: function(chart) {
        if (chart == 'line'){
            var canvas = document.querySelector('#sale_order_generated');
        }
      
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var
        doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('product_price_report.pdf');
    },
    
    sale_team_report_pdf: function(chart) {
        if (chart == 'pie'){
            var canvas = document.querySelector('#sale_team_data');
        }
      
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('sale_team_report.pdf');
    },

    sale_order_report_pdf: function(chart) {
        if (chart == 'pie'){
            var canvas = document.querySelector('#sale_order_data');
        }
      
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('sale_order_report.pdf');
    },

    count_wise_customer_pdf: function(chart) {
        if (chart == 'pie'){
            var canvas = document.querySelector('#Chart');
        }
      
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('count_wise_customer.pdf');
    },
    
          
});


core.action_registry.add("sale_dashboard", MyCustomAction);
return MyCustomAction
});