odoo.define('modern_dashboard_odoo_axis_affinity.AccountDashboard',  function (require) {
"use strict";
var AbstractAction = require('web.AbstractAction');
var ActionManager = require('web.ActionManager');
var view_registry = require('web.view_registry');
var Widget = require('web.Widget');
var AbstractAction = require('web.AbstractAction');
var ajax = require('web.ajax');
var core = require('web.core');
var rpc = require('web.rpc');
var session = require('web.session');
var web_client = require('web.web_client');
var _t = core._t;
var QWeb = core.qweb;

var MyAccountDashboard = AbstractAction.extend({
    template: 'AccountDashboardView',
    cssLibs: [
        '/modern_dashboard_odoo_axis_affinity/static/src/scss/lib/nv.d3.css'
    ],
    jsLibs: [
        '/modern_dashboard_odoo_axis_affinity/static/src/js/lib/d3.min.js',
        '/modern_dashboard_odoo_axis_affinity/static/src/js/lib/charts/chart.js',
       
    ],
    events: {
        'click .more-open-invoice': 'action_open_invoice',
        'click .more-cancel-invoice': 'action_cancel_invoice',
        'click .more-cutomer-payment': 'action_customer_payment',
        'click .more-vendor-payment': 'action_vendor_payment',
        'change .custommer_payment_list': 'action_customer_payment_data',
        'change .vendor_payment_list': 'action_vendor_payment_data',
        'change .customer_record': 'action_customer_record',
        'change .vendor_record': 'action_vendor_record',
        'change .journal_record': 'action_journal_record',
        'change .revenue_customer_data': 'action_revenue_customer_data',
        'change .invoice_order_list': 'action_invoice_order_list',
        'click  #order_details': 'action_invoice_order_list',
        'click  #cust_payment': 'graph_customer_payment',
        'click  #vender_payment': 'graph_supplier_payment',
        'click  #cash_bank_detail': 'graph_bank_cash_info',
         'click #color_filter2': 'graph_customer_payment',
        'click #color_filter3': 'graph_supplier_payment',
        'click #color_filter4': 'graph_journal_list',
        'click #color_filter6': 'render_r_customer',
        'click #color_filter8': 'graph_bank_cash_info',
        'click #customer_payment_pdf': function(){this.customer_payment_pdf("bar")},
        'click #vendor_payment_pdf': function(){this.vendor_payment_pdf("line")},
        'click #journal_list_pdf': function(){this.journal_list_pdf("pie")},
        'click #recent_customer_pdf': function(){this.recent_customer_pdf("pie")},
        'click #cash_bank_pdf': function(){this.cash_bank_pdf("pie")},

       
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
        self.action_customer_payment_data();
        self.action_vendor_payment_data();
        self.action_customer_record();
        self.action_vendor_record();
        self.action_journal_record();
        self.action_revenue_customer_data();
        self.action_invoice_order_list();
        self.render_graphs();
        return this._super();
    },

    fetch_data: function() {
        var self = this;
        var account_dashboard =  this._rpc({
                model: 'account.move',
                method: 'get_account_list',
        }).then(function(result) {
            self.render_dashboards();
            self.href = window.location.href;

        });
        return account_dashboard
    },

    reload: function () {
            window.location.href = this.href;
    },
    

    render_dashboards: function() {
        var self = this;     
        var account_dashboard = QWeb.render('AccountDashboardView', {
            widget: self,
        });
        rpc.query({
                model: 'account.move',
                method: 'get_account_move_list',
                args: []
            })
            .then(function (result){
            		self.$el.find('.total-posted').text(result['total_posted'])
            		self.$el.find('.total-cancel').text(result['total_cancel'])
            		self.$el.find('.total-customer-payment').text(result['total_customer_payment'])
            		self.$el.find('.total-vendor-payment').text(result['total_vendor_payment'])
                    self.$el.find('.total-profit').text(result['total_profit']) 

            });
        
        return account_dashboard
    },


    action_open_invoice: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Open Invoice"),
            type: 'ir.actions.act_window',
            res_model: 'account.move',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_open_invoice':true,                   
                    },
            
            domain: [['state','in',['posted']]],

            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });


    },

    action_cancel_invoice: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Cancel Invoice"),
            type: 'ir.actions.act_window',
            res_model: 'account.move',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_closse_invoice':true,                   
                    },
            
            domain: [['state','in',['cancel']]],

            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });


    },


    action_customer_payment: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Customer Payment"),
            type: 'ir.actions.act_window',
            res_model: 'account.move',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_lost_count':true,                   
                    },
            
            domain: [['state','in',['posted']]],

            target: 'current'
        }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });


    },



    action_vendor_payment: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
        this.do_action({
            name: _t("Vendor Payment"),
            type: 'ir.actions.act_window',
            res_model: 'account.move',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {                        
                        'search_default_lost_count':true,                   
                    },
            
            domain: [['state','in',['reconciled']]],

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
    
    action_customer_payment_data : function(value){
            var self = this;

            rpc.query({
                model: 'account.move',
                method: 'get_account_table',
                args : []
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.customer_payment_data');
                    contents.empty();
                    var res = result['customer_payment_data']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].invoice,res[i].partner_name,res[i].amount,res[i].payment_date,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.customer_payment_data').DataTable( {
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
                                { title: "Invoice Name" },
                                { title: "Customer Name" },
                                { title: "Amount" },
                                { title: "Payment Date" },
        
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#custpaymentcsv');
                    exp_csv.click(function(){        
                        var html = document.getElementById("custpaymenttable").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#custpaymenttable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
                    var exp_xls = self.$el.find('#custpaymentxls');
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
                        var table_html = $('#custpaymenttable')[0].outerHTML;
                        table_html = table_html.replace(/<tfoot[\s\S.]*tfoot>/gmi, '');
                        var css_html = '<style>td {border: 0.5pt solid #c0c0c0} .tRight { text-align:right} .tLeft { text-align:left} </style>';
                        a.href = data_type + ',' + encodeURIComponent('<html><head>' + css_html + '</' + 'head><body>' + table_html + '</body></html>');
                        a.download = 'exported_table_' + postfix + '.xls';
                        a.click();
                    });
                }
            });
        },

    action_vendor_payment_data : function(value){
            var self = this;

            rpc.query({
                model: 'account.move',
                method: 'get_account_table',
                args : []
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.vendor_payment_data');
                    contents.empty();
                    var res = result['vendor_payment_data']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].invoice,res[i].partner_name,res[i].amount,res[i].payment_date,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.vendor_payment_data').DataTable( {
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
                                { title: "Invoice Name" },
                                { title: "Customer Name" },
                                { title: "Amount" },
                                { title: "Payment Date" },
        
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#venderpaycsv');
                    exp_csv.click(function(){        
                        var html = document.getElementById("venderpaytable").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#venderpaytable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
                    var exp_xls = self.$el.find('#venderpayxls');
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
                        var table_html = $('#venderpaytable')[0].outerHTML;
                        table_html = table_html.replace(/<tfoot[\s\S.]*tfoot>/gmi, '');
                        var css_html = '<style>td {border: 0.5pt solid #c0c0c0} .tRight { text-align:right} .tLeft { text-align:left} </style>';
                        a.href = data_type + ',' + encodeURIComponent('<html><head>' + css_html + '</' + 'head><body>' + table_html + '</body></html>');
                        a.download = 'exported_table_' + postfix + '.xls';
                        a.click();
                    });
                }
            });
        },


    action_customer_record : function(value){
            var self = this;

            rpc.query({
                model: 'account.move',
                method: 'get_account_table',
                args : []
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.customer_record_data');
                    contents.empty();
                    var res = result['customer_list_data']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].customer_name,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.customer_record_data').DataTable( {
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
                              
                                { title: "Customer Name" }, 
        
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#custrecordcsv');
                    exp_csv.click(function(){        
                        var html = document.getElementById("custrecordtable").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#custrecordtable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
                    var exp_xls = self.$el.find('#custrecordxls');
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
                        var table_html = $('#custrecordtable')[0].outerHTML;
                        table_html = table_html.replace(/<tfoot[\s\S.]*tfoot>/gmi, '');
                        var css_html = '<style>td {border: 0.5pt solid #c0c0c0} .tRight { text-align:right} .tLeft { text-align:left} </style>';
                        a.href = data_type + ',' + encodeURIComponent('<html><head>' + css_html + '</' + 'head><body>' + table_html + '</body></html>');
                        a.download = 'exported_table_' + postfix + '.xls';
                        a.click();
                    });
                }
            });
        },

    action_vendor_record : function(value){
            var self = this;

            rpc.query({
                model: 'account.move',
                method: 'get_account_table',
                args : []
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.vendor_record_data');
                    contents.empty();
                    var res = result['vendor_list_data']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].customer_name,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.vendor_record_data').DataTable( {
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

                                { title: "Customer Name" },

        
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#vendercsv');
                    exp_csv.click(function(){        
                        var html = document.getElementById("vendertable").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#vendertable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
                    var exp_xls = self.$el.find('#venderxls');
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
                        var table_html = $('#vendertable')[0].outerHTML;
                        table_html = table_html.replace(/<tfoot[\s\S.]*tfoot>/gmi, '');
                        var css_html = '<style>td {border: 0.5pt solid #c0c0c0} .tRight { text-align:right} .tLeft { text-align:left} </style>';
                        a.href = data_type + ',' + encodeURIComponent('<html><head>' + css_html + '</' + 'head><body>' + table_html + '</body></html>');
                        a.download = 'exported_table_' + postfix + '.xls';
                        a.click();
                    });
                }
            });
        },



    action_journal_record : function(value){
            var self = this;

            rpc.query({
                model: 'account.move',
                method: 'get_account_table',
                args : []
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.journal_record_data');
                    contents.empty();
                    var res = result['journal_list_data']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].journal_name,res[i].types,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.journal_record_data').DataTable( {
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

                                { title: "Journal Name" },
                                { title: "Journal Type" },

        
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#journacsv');
                    exp_csv.click(function(){        
                        var html = document.getElementById("journaltable").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#journaltable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
                    var exp_xls = self.$el.find('#journalxls');
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
                        var table_html = $('#journaltable')[0].outerHTML;
                        table_html = table_html.replace(/<tfoot[\s\S.]*tfoot>/gmi, '');
                        var css_html = '<style>td {border: 0.5pt solid #c0c0c0} .tRight { text-align:right} .tLeft { text-align:left} </style>';
                        a.href = data_type + ',' + encodeURIComponent('<html><head>' + css_html + '</' + 'head><body>' + table_html + '</body></html>');
                        a.download = 'exported_table_' + postfix + '.xls';
                        a.click();
                    });
                }
            });
        },


    action_revenue_customer_data : function(value){
            var self = this;

            rpc.query({
                model: 'account.move',
                method: 'get_account_table',
                args : []
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.revenue_customer_record');
                    contents.empty();
                    var res = result['total_revenue_customer']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                        dataSet.push([res[i].partner_name,res[i].amount,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.revenue_customer_record').DataTable( {
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

                                { title: "Partner Name" },
                                { title: "Amount" },

        
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#revenuerecordcsv');
                    exp_csv.click(function(){        
                        var html = document.getElementById("revenuetable").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#revenuetable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
                    var exp_xls = self.$el.find('#revenuerecordxls');
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
                        var table_html = $('#revenuetable')[0].outerHTML;
                        table_html = table_html.replace(/<tfoot[\s\S.]*tfoot>/gmi, '');
                        var css_html = '<style>td {border: 0.5pt solid #c0c0c0} .tRight { text-align:right} .tLeft { text-align:left} </style>';
                        a.href = data_type + ',' + encodeURIComponent('<html><head>' + css_html + '</' + 'head><body>' + table_html + '</body></html>');
                        a.download = 'exported_table_' + postfix + '.xls';
                        a.click();
                    });
                }
            });
        },


    action_invoice_order_list: function(value){
            var self = this;
            var option = this.$el.find('#order_details').val();
            rpc.query({
                model: 'account.move',
                method: 'get_invoice_order_table',
                args : [option]
            }, {async: false}).then(function (result) {
                if(result){
                    var contents = self.$el.find('.invoice_order_data');
                    contents.empty();
                    var res = result['total_invoice_order']
                    var dataSet = []
                    for(var i=0;i<res.length;i++){
                         dataSet.push([res[i].amount,res[i].origin,res[i].invoice_date,res[i].name,res[i].payment,'<span class="label label-success">' + '</span>'])
                    }
                    if(dataSet.length > 0){
                        $('.invoice_order_data').DataTable( {
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

                                { title: "Amount" },
                                { title: "Invoice Origin" },
                                { title: "Invoice Date" },
                                { title: "Partner Name" },
                                { title: "Payment" },

        
                            ]
                        });
                    }
                    var exp_csv = self.$el.find('#ordercsv');
                    exp_csv.click(function(){        
                        var html = document.getElementById("ordertable").outerHTML;
                        var csv = [];
                        var rows = document.querySelectorAll("#ordertable tr");
                        for (var i = 0; i < rows.length; i++) {
                            var row = [], cols = rows[i].querySelectorAll("td, th");
                            for (var j = 0; j < cols.length; j++) 
                                row.push(cols[j].innerText);
                            csv.push(row.join(","));        
                        }
                        self.export_csv(csv.join("\n"), "table.csv");
                    });
                    var exp_xls = self.$el.find('#orderxls');
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
                        var table_html = $('#ordertable')[0].outerHTML;
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
            self.graph_customer_payment();
            self.graph_customer_invoice();
            self.graph_journal_list();
            self.graph_supplier_payment();
            self.render_r_customer();
            self.graph_bank_cash_info();
        
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


    render_r_customer: function() {
        var self = this
        var color = this.$el.find('#color_filter6').val();
        
        if (color == 'cool'){
            $('.recent_customer_i').addClass('cool_color');
        }
        else {
            $('.recent_customer_i').addClass('warm_color');
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
                model: 'account.move',
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


    graph_customer_payment: function() {
        var self = this;
        var color = this.$el.find('#color_filter2').val();
        
        if (color == 'cool'){
            $('.customer_payment_i').addClass('cool_color');
        }
        else {
            $('.customer_payment_i').addClass('warm_color');
        }
        var option = this.$el.find('#cust_payment').val();
        var ctx = this.$el.find('#customer_payment')
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
                model: 'account.move',
                method: 'get_customer_payment',
                args: [option]

            })
            .then(function (result) {
                var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                   
                    labels: result.payroll_label,
                    datasets: [{
                        label: 'Customer Payment',
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

  


    graph_bank_cash_info: function() {
        var self = this;
        var color = this.$el.find('#color_filter8').val();
        
        if (color == 'cool'){
            $('.cash_balance').addClass('cool_color');
        }
        else {
            $('.cash_balance').addClass('warm_color');
        }
        var option = this.$el.find('#cash_bank_detail').val();
        var ctx = this.$el.find('#cash_bank')
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
                model: 'account.move',
                method: 'get_bank_cash_info',
                args: [option]

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
                        label: 'Balance',
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
        var csv_file = self.$el.find('#cashbankcsv');
        csv_file.click(function(){
            self.exportcsv({ filename: "chart-data.csv", chart: chart })
        });
     });

    
    },



    graph_supplier_payment: function() {
        var self = this;
        var color = this.$el.find('#color_filter3').val();
        
        if (color == 'cool'){
            $('.vendor_payment_i').addClass('cool_color');
        }
        else {
            $('.vendor_payment_i').addClass('warm_color');
        }
        var option = this.$el.find('#vender_payment').val();
        var ctx = this.$el.find('#supplier_invoice')
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
                model: 'account.move',
                method: 'get_supplier_payment',
                args: [option]
            })
            .then(function (result) {
                var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                   
                    labels: result.payroll_label,
                    datasets: [{
                        label: 'Vendor Payment',
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



    graph_customer_invoice: function() {
        var self = this
        var ctx = this.$el.find('#customer_invoice')
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
                model: 'account.move',
                method: 'get_customer_invoice',
                

            })
            .then(function (result) {
                var myChart = new Chart(ctx, {
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


    graph_journal_list: function() {
        var self = this
        var color = this.$el.find('#color_filter4').val();
        
        if (color == 'cool'){
            $('.journal_list').addClass('cool_color');
        }
        else {
            $('.journal_list').addClass('warm_color');
        }
        var piectx = this.$el.find('#journal_record')
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
                model: 'account.move',
                method: 'get_journal_list',
            })
            .then(function (result) {
                
                    bg_color_list = []
                    for (var i=0;i<=result.payroll_dataset.length;i++){
                        bg_color_list.push(self.getRandomColor())
                    }
                    var pieChart = new Chart(piectx, {
                        type: 'radar',
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
            customer_payment_pdf: function(chart) {
        var canvas = document.querySelector('#customer_payment');
    
      
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('customer_payment_data.pdf');
    },

    vendor_payment_pdf: function(chart) {
        
        var canvas = document.querySelector('#supplier_invoice');
        
      
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('vendor_payment_data.pdf');
    },
    
    journal_list_pdf: function(chart) {
        var canvas = document.querySelector('#journal_record');
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('journal_list_data.pdf');
    },

    recent_customer_pdf: function(chart) {
        var canvas = document.querySelector('#r_customer');
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('recent_customer_data.pdf');
    },

    cash_bank_pdf: function(chart) {
        var canvas = document.querySelector('#cash_bank');
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('cash_bank_data.pdf');
    },



    



             
});
 

core.action_registry.add("account_dashboard_action", MyAccountDashboard);
return MyAccountDashboard
});