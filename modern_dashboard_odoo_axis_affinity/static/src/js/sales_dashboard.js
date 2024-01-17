odoo.define('pos_sales_dachboard.sale_dashboard_screens', function (require) {
"use strict";

	var screens = require('point_of_sale.screens');
    var models = require('point_of_sale.models');
    var gui = require('point_of_sale.gui');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var PopupWidget = require('point_of_sale.popups');
    
    var _t = core._t;
    var QWeb = core.qweb;

    screens.ProductScreenWidget.include({
        start: function(){
            var self = this;
            self._super();
            if(self.pos.config.pos_dashboard){
                $('.sales-dashboard').show();
                $('#sales_dashboard').click(function() {
                    self.gui.show_screen('pos_dashboard_graph_view');
                });
            }
            else{
              $('.sales-dashboard').hide();
            }
            if(self.pos.config.print_audit_report){
                $('.print_audit_report').show();
                $('.print_audit_report').click(function() {
                    self.gui.show_popup('report_popup');
                });
            }
            else{
                $('.print_audit_report').hide();
            }
            $('.main_slider-ul > li.main-header-li').click(function() {
                $(this).parent().find('ul.content-list-ul').slideToggle();
                $(this).find('i').toggleClass('fa fa-angle-down fa fa-angle-right');
            });
            if(self.pos.config.today_sale_report && self.pos.user.access_today_sale_report){
                $('.today_sale_report').click(function() {
                    var str_payment = '';
                    var params = {
                        model: 'pos.session',
                        method: 'get_session_report',
                        args: [],
                    }
                    rpc.query(params, {async: false}).then(function(result){
                        if(result['error']){
                            self.pos.db.notification('danger',result['error']);
                        }
                        if(result['payment_lst']){
                            var temp = [] ;
                            for(var i=0;i<result['payment_lst'].length;i++){
                                if(result['payment_lst'][i].session_name){
                                    if(jQuery.inArray(result['payment_lst'][i].session_name,temp) != -1){
                                        str_payment+="<tr><td style='font-size: 16px;padding: 8px;'>"+result['payment_lst'][i].journals+"</td>" +
                                        "<td style='font-size: 16px;padding: 8px;'>"+self.format_currency(result['payment_lst'][i].total.toFixed(2))+"</td>" +
                                    "</tr>";
                                    }else{
                                        str_payment+="<tr><td style='font-size:14px;padding: 8px;' colspan='2'>"+result['payment_lst'][i].session_name+"</td></tr>"+
                                        "<td style='font-size: 16px;padding: 8px;'>"+result['payment_lst'][i].journals+"</td>" +
                                        "<td style='font-size: 16px;padding: 8px;'>"+self.format_currency(result['payment_lst'][i].total.toFixed(2))+"</td>" +
                                    "</tr>";
                                    temp.push(result['payment_lst'][i].session_name);
                                    }
                                }
                            }
                        }
                        self.gui.show_popup('pos_today_sale',{result:result,str_payment:str_payment});
                    }).catch(function(){
                        self.pos.db.notification('danger',"Connection lost");
                    });
                });
            }
            else{
                $('.today_sale_report').hide();
            }
            if(self.pos.config.x_report && self.pos.user.access_x_report){
                $('.x-report').click(function() {
                    var pos_session_id = [self.pos.pos_session.id];
                    self.pos.chrome.do_action('pos_sales_dashboard.pos_x_report',{additional_context:{
                        active_ids:pos_session_id,
                    }}).fail(function(){
                        self.pos.db.notification('danger',"Connection lost");
                    });
                });  
            }
        },
    });

    var POSDashboardGraphScreenWidget = screens.ScreenWidget.extend({
        template: 'POSDashboardGraphScreenWidget',
        init: function(parent, options){
            this._super(parent, options);
            var self = this;
            this.pie_chart_journal = function(){
                var order = this.pos.get_order();
                var data = order.get_graph_data_journal();
                var dps = [];
                // for(var i=0;i<data.length;i++){
                //     dps.push({label: data[i].name, y: data[i].sum});
                // }
                var chart = new CanvasJS.Chart("chartContainer_journal",
                {
                    zoomEnabled:true,
                    theme: "theme2",
                    data: [{
                        type: "pie",
                        showInLegend: true,
                        toolTipContent: "{y} - #percent %",
                        yValueFormatString: "",
                        legendText: "{indexLabel}",
                        dataPoints: dps
                    }]
                });
                chart.render();
            };
            this.pie_chart_top_product = function(){
                var order = this.pos.get_order();
                var data = order.get_top_product_result();
                var dps = [];
                if(data && data[0]){
                    for(var i=0;i<data.length;i++){
                        dps.push({label: data[i].name, y: data[i].sum});
                    }
                }
                var chart = new CanvasJS.Chart("chartContainer_top_product",
                {
                    zoomEnabled:true,
                    theme: "theme2",
                    data: [{
                        type: "pie",
                        showInLegend: true,
                        toolTipContent: "{y} - #percent %",
                        yValueFormatString: "",
                        legendText: "{indexLabel}",
                        dataPoints: dps
                    }]
                });
                chart.render();
            };
            this.pie_chart_customer = function(){
                var order = this.pos.get_order();
                var data = order.get_customer_summary();
                var dps = [];
                if(data){
                    dps.push({label: "New Customer", y: data.new_client_sale});
                    dps.push({label: "Existing Customer", y: data.existing_client_sale});
                    dps.push({label: "Without Customer", y: data.without_client_sale});
                }
                var chart = new CanvasJS.Chart("chartContainer_based_customer",
                {
                    zoomEnabled:true,
                    theme: "theme2",
                    data: [{
                        type: "pie",
                        showInLegend: true,
                        toolTipContent: "{y} - #percent %",
                        yValueFormatString: "",
                        legendText: "{indexLabel}",
                        dataPoints: dps
                    }]
                });
                chart.render();
            };
            this.bar_chart_hourly = function(){
                var order = this.pos.get_order();
                var data = order.get_hourly_summary();
                var dps = [];
                var dps2 = [];
                if(data && data[0]){
                    for(var i=0;i<data.length;i++){
                        dps.push({label: "("+data[i].date_order_hour[0] + "-" + data[i].date_order_hour[1	]+")", y: data[i].price_total});
                        dps2.push({y: data[i].price_total});
                    }
                }
                var symbol = 'Amount-#######.00';
                var chart = new CanvasJS.Chart("chartContainer_hourly_sale",{
                    width: data && data.length > 10 ? 1200 : 0,
                    dataPointMaxWidth:25,
                    zoomEnabled:true,
                    animationEnabled: true,
                    theme: "theme3",
                    title: {
                        text: "Today Hourly Sales"
                    },
                    axisY: {
                        suffix: "",
                        title:"Amount",
                    },
                     axisX:{
                          title:"Hours",
                          labelAngle: 45,
                          interval:1
                    },
                    legend :{
                        verticalAlign: 'bottom',
                        horizontalAlign: "center"
                    },
                    data: [{
                        type: "column",
                        dataPoints: dps,
                        color:"#008080",
                    },{
                        type: "column",
                        dataPoints: dps2,
                        color:"#008080",
                    }]
                });
                chart.render();
            };
            this.bar_chart_monthly = function(){
                var order = this.pos.get_order();
                var data = order.get_month_summary();
                var dps = [];
                if(data && data[0]){
                    for(var i=0;i<data.length;i++){
                        dps.push({label: data[i].date_order_day +'/'+data[i].date_order_month, y: data[i].price_total});
                    }
                    var symbol = 'Amount-#######.00';
                    var chart = new CanvasJS.Chart("chartContainer_monthly_sale",{
                        width: data && data.length > 10 ? 1200 : 0,
                        dataPointMaxWidth:25,
                        zoomEnabled:true,
                        animationEnabled: true,
                        theme: "theme3",
                        title: {
                            text: "This Month Sales"
                        },axisY: {
                            suffix: "",
                            title:"Amount",
                        },axisX:{
                              title:"Days",
                              interval:1
                        },legend :{
                            verticalAlign: 'bottom',
                            horizontalAlign: "center"
                        },data: [{
                            type: "column",
                            indexLabel:'{y}',
                            xValueType: "dateTime",
                            indexLabelOrientation: "vertical",
                            dataPoints: dps
                        }]
                    });
                    chart.render();
                }
            };
            this.bar_chart_six_month = function(){
                var order = this.pos.get_order();
                var data = order.get_six_month_summary();
                var dps = [];
                if(data && data[0]){
                    for(var i=0;i<data.length;i++){
                        dps.push({x: data[i].date_order_month, y: data[i].price_total});
                    }
                    var symbol = 'Amount-#######.00';
                    var chart = new CanvasJS.Chart("chartContainer_six_month_sale",{
                        width: data && data.length > 10 ? 1200 : 0,
                        dataPointMaxWidth:25,
                        zoomEnabled:true,
                        animationEnabled: true,
                        theme: "theme3",
                        title: {
                            text: "Last 12 Month Sales"
                        },axisY: {
                            suffix: "",
                            title:"Amount",
                        },axisX:{
                              title:"Months",
                              interval:1
                        },legend :{
                            verticalAlign: 'bottom',
                            horizontalAlign: "center"
                        },data: [{
                            type: "column",
                            indexLabel:'{y}',
                            indexLabelOrientation: "vertical",
                            dataPoints: dps
                        }]
                    });
                    chart.render();
                }
            };
            this.bar_chart_active_session_wise_sale = function(){
                var order = this.pos.get_order();
                var data = order.get_active_session_sales();
                var dps = [];
                if(data && data[0]){
                    _.each(data,function(session){
                        dps.push({label: session.pos_session_id[0].display_name, y: session.sum});
                    })
                }
                var chart = new CanvasJS.Chart("chartContainer_session_wise_sale",{
                    width: data && data.length > 10 ? 1200 : 0,
                    dataPointMaxWidth:25,
                    zoomEnabled:true,
                    animationEnabled: true,
                    theme: "theme3",
                    title: {
                        text: "Today's Active Session(s) Sale"
                    },axisY: {
                        suffix: "",
                        title:"Amount",
                    },axisX:{
                        title:"Sessions",
                        interval:3
                    },legend :{
                        verticalAlign: 'bottom',
                        horizontalAlign: "center"
                    },data: [{
                        type: "column",
                        indexLabel:'{y}',
                        indexLabelOrientation: "vertical",
                        dataPoints: dps
                    }]
                });
                chart.render();
            };
            this.bar_chart_closed_session_wise_sale = function(){
                var order = this.pos.get_order();
                var data = order.get_closed_session_sales();
                var dps = [];
                if(data && data[0]){
                    _.each(data,function(session){
                        dps.push({label: session.pos_session_id[0].display_name, y: session.sum});
                    })
                }
                var chart = new CanvasJS.Chart("chartContainer_closed_session_wise_sale",{
                    width: data && data.length > 10 ? 1200 : 0,
                    dataPointMaxWidth:25,
                    zoomEnabled:true,
                    animationEnabled: true,
                    theme: "theme3",
                    title: {
                        text: "Today's Closed Session(s) Sale"
                    },axisY: {
                        suffix: "",
                        title:"Amount",
                    },axisX:{
                        title:"Sessions",
                        interval:3
                    },legend :{
                        verticalAlign: 'bottom',
                        horizontalAlign: "center"
                    },data: [{
                        type: "column",
                        indexLabel:'{y}',
                        indexLabelOrientation: "vertical",
                        dataPoints: dps
                    }]
                });
                chart.render();
            };
        },
        get_graph_information: function(){
            var from = $('#start_date_journal').val() ? $('#start_date_journal').val() + " 00:00:00" : false;
            var to   = $('#end_date_journal').val() ? $('#end_date_journal').val() + " 23:59:59" : false;
            this.graph_data_journal(from,to);
        },
        get_top_product_graph_information: function(){
            var from = $('#start_date_top_product').val() ? $('#start_date_top_product').val() + " 00:00:00" : false;
            var to   = $('#end_date_top_product').val() ? $('#end_date_top_product').val() + " 23:59:59" : false;
            this.graph_data_top_product(from,to);
        },
        get_sales_by_user_information: function(){
            var from = $('#start_date_sales_by_user').val() ? $('#start_date_sales_by_user').val() + " 00:00:00" : false;
            var to   = $('#end_date_sales_by_user').val() ? $('#end_date_sales_by_user').val() + " 23:59:59" : false;
            this.sales_by_user(from,to)
        },
        render_journal_list: function(journal_data){
        	console.log('-------------journal_data-------------',journal_data)
            var contents = this.$el[0].querySelector('.journal-list-contents');
            contents.innerHTML = "";
            for(var i = 0, len = Math.min(journal_data.length,1000); i < len; i++){
                var journal = journal_data[i];
                var journal_html = QWeb.render('JornalLine',{widget: this, journal:journal_data[i]});
                var journalline = document.createElement('tbody');
                journalline.innerHTML = journal_html;
                journalline = journalline.childNodes[1];
                contents.appendChild(journalline);
            }
        },
        render_top_product_list: function(top_product_list){
            var contents = this.$el[0].querySelector('.top-product-list-contents');
            contents.innerHTML = "";
            for(var i = 0, len = Math.min(top_product_list.length,1000); i < len; i++){
                var top_product = top_product_list[i];
                var top_product_html = QWeb.render('TopProductLine',{widget: this, top_product:top_product_list[i]});
                var top_product_line = document.createElement('tbody');
                top_product_line.innerHTML = top_product_html;
                top_product_line = top_product_line.childNodes[1];
                contents.appendChild(top_product_line);
            }
        },
        graph_data_journal: function(from, to){
            var self = this;
            rpc.query({
                model: 'pos.order',
                method: 'graph_date_on_canvas',
                args: [from, to]
            },{async:false}).then(
                function(result) {
                    var order = self.pos.get_order();
                    if(result){
                        self.render_journal_list(result)
                        if(result.length > 0){
                            order.set_graph_data_journal(result);
                        }else{
                            order.set_graph_data_journal(0);
                        }
                    }else{
                        order.set_graph_data_journal(0);
                    }
                    self.pie_chart_journal();
                }).catch(function(error) {
                if (error.code === -32098) {
                    alert("Server closed...");
                    event.preventDefault();
                }
            });
        },
        graph_data_top_product: function(from, to){
            var self = this;
            rpc.query({
                model: 'pos.order',
                method: 'graph_best_product',
                args: [from, to]
            },{async:false}).then(
                function(result) {
                    var order = self.pos.get_order();
                    if(result){
                        self.render_top_product_list(result)
                        if(result.length > 0){
                            order.set_top_product_result(result);
                        }else{
                            order.set_top_product_result(0);
                        }
                    }else{
                        order.set_top_product_result(0);
                    }
                    self.pie_chart_top_product();
                }).catch(function(error, event) {
                if (error.code === -32098) {
                    alert("Server closed...");
                    event.preventDefault();
                }
            });
        },
        sales_by_user: function(from, to){
            var self = this;
            rpc.query({
                model: 'pos.order',
                method: 'orders_by_salesperson',
                args: [from,to]
            },{async:false}).then(function(result) {
                if(result){
                    self.render_user_wise_sales(result)
                }
            });
        },
        sales_from_session: function(){
            var self = this;
            rpc.query({
                model: 'pos.order',
                method: 'session_details_on_canvas',
            },{async:false}).then(function(result) {
                if(result){
                    if(result){
                        if(result.active_session && result.active_session[0]){
                            self.pos.get_order().set_active_session_sales(result.active_session);
                        }
                        if(result.close_session && result.close_session[0]){
                            self.pos.get_order().set_closed_session_sales(result.close_session)
                        }
                    }
                }
            });
        },
        render_user_wise_sales: function(sales_users){
            var contents = this.$el[0].querySelector('.user-wise-sales-list-contents');
            contents.innerHTML = "";
            for(var i = 0, len = Math.min(sales_users.length,1000); i < len; i++){
                var user_data = sales_users[i];
                var user_sales_html = QWeb.render('UserSalesLine',{widget: this, user_sales:sales_users[i]});
                var user_sales_line = document.createElement('tbody');
                user_sales_line.innerHTML = user_sales_html;
                user_sales_line = user_sales_line.childNodes[1];
                contents.appendChild(user_sales_line);
            }
        },
        show: function(){
            var self = this;
            this._super();
            this.$('.back').click(function(){
                self.gui.show_screen('products');
            });
            
            var today = moment().locale('en').format("YYYY-MM-DD");
            $("#start_date_journal").val(today);
            $("#end_date_journal").val(today);
            $("#start_date_top_product").val(today);
            $("#end_date_top_product").val(today);
            $("#start_date_sales_by_user").val(today);
            $("#end_date_sales_by_user").val(today);
            var start_date = false;
            var end_date = false;
            var active_chart = $('span.selected_chart').attr('id');
            $("#start_date_journal").datepicker({
                dateFormat: 'yy-mm-dd',
                autoclose: true,
                closeText: 'Close',
                showButtonPanel: true,
                onSelect: function(dateText, inst) {
                    start_date = dateText;
                    var active_chart = $('span.selected_chart').attr('id');
                    self.graph_data_journal(start_date, end_date);
                },
            });
            $("#end_date_journal").datepicker({
                dateFormat: 'yy-mm-dd',
                autoclose: true,
                closeText: 'Close',
                showButtonPanel: true,
                onSelect: function(dateText, inst) {
                    end_date = dateText;
                    var active_chart = $('span.selected_chart').attr('id');
                    self.graph_data_journal(start_date, end_date);
                },
            });
            $("#start_date_top_product").datepicker({
                dateFormat: 'yy-mm-dd',
                autoclose: true,
                closeText: 'Close',
                showButtonPanel: true,
                onSelect: function(dateText, inst) {
                    start_date = dateText;
                    var active_chart = $('span.selected_chart').attr('id');
                    self.graph_data_top_product(start_date, end_date);
                },
            });
            $("#end_date_top_product").datepicker({
                dateFormat: 'yy-mm-dd',
                autoclose: true,
                closeText: 'Close',
                showButtonPanel: true,
                onSelect: function(dateText, inst) {
                    end_date = dateText;
                    var active_chart = $('span.selected_chart').attr('id');
                    self.graph_data_top_product(start_date, end_date);
                },
            });
            $("#start_date_sales_by_user").datepicker({
                dateFormat: 'yy-mm-dd',
                autoclose: true,
                closeText: 'Close',
                showButtonPanel: true,
                onSelect: function(dateText, inst) {
                    start_date = dateText;
                    self.sales_by_user(start_date,end_date)
                },
            });
            $("#end_date_sales_by_user").datepicker({
                dateFormat: 'yy-mm-dd',
                autoclose: true,
                closeText: 'Close',
                showButtonPanel: true,
                onSelect: function(dateText, inst) {
                    end_date = dateText;
                    self.sales_by_user(start_date,end_date)
                },
            });
            rpc.query({
                model: 'pos.order',
                method: 'get_dashboard_data',
                args: []
            },{async:false}).then(function(result) {
                self.pos.dashboard_data = result;
                if(result){
                    $('#total_active_session').text(result['active_sessions'])
                    $('#total_closed_session').text(result['closed_sessions'])
                    $('#total_sale_count').text(result['total_orders']);
                    $('#total_sale_amount').text(self.chrome.format_currency(result['total_sales']));
                    var order = self.pos.get_order();
                    order.set_hourly_summary(result['sales_based_on_hours']);
                    order.set_month_summary(result['current_month']);
                    order.set_six_month_summary(result['last_6_month_res']);
                    order.set_customer_summary(result['client_based_sale']);
                    self.get_graph_information();
                    self.get_top_product_graph_information();
                    self.get_sales_by_user_information();
                    self.pie_chart_journal();
                    self.pie_chart_top_product();
                    self.bar_chart_hourly();
                    self.bar_chart_monthly();
                    self.bar_chart_six_month();
                    self.pie_chart_customer();
                    self.sales_from_session();
//        			self.bar_chart_active_session_wise_sale();
//        			self.bar_chart_closed_session_wise_sale();
                }
            });
        },
    });
    gui.define_screen({name:'pos_dashboard_graph_view', widget: POSDashboardGraphScreenWidget});
    
    // today sale report
    var TodayPosReportPopup = PopupWidget.extend({
        template: 'TodayPosReportPopup',
        show: function(options){
            this.str_main = options.str_main || "";
            this.str_payment = options.str_payment || "";
            options = options || {};
            this._super(options);
            this.session_total = options.result['session_total'] || [];
            this.payment_lst = options.result['payment_lst'] || [];
            this.all_cat = options.result['all_cat'] || [];
            this.renderElement();
            $(".tabs-menu a").click(function(event) {
                event.preventDefault();
                $(this).parent().addClass("current");
                $(this).parent().siblings().removeClass("current");
                var tab = $(this).attr("href");
                $(".tab-content").not(tab).css("display", "none");
                $(tab).fadeIn();
            });
        },
        renderElement: function() {
            var self = this;
            this._super();
        },
    });
    gui.define_popup({name:'pos_today_sale', widget: TodayPosReportPopup});

    // print audit report
    var ReportPopupWidget = PopupWidget.extend({
        template: 'ReportPopupWidget',
        events: _.extend({}, PopupWidget.prototype.events, {
            'click .report_pdf.session': 'session_report_pdf',
            'click .report_thermal.session': 'session_report_thermal',
            'click .report_pdf.location': 'location_report_pdf',
            'click .report_thermal.location': 'location_report_thermal',
            'click .tablinks':'tablinks',
        }),
        show: function(options){
            options = options || {};
            this._super(options);
            this.enable_thermal_print = this.pos.config.iface_print_via_proxy || false;
            this.renderElement();
        },
        tablinks: function(event){
            var cityName = $(event.currentTarget).attr('value');
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tabcontent");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
            document.getElementById(cityName).style.display = "block";
            event.currentTarget.className += " active";
        },
        session_report_pdf: function(e){
            var self = this;
            var session_id = $(e.currentTarget).data('id');
            console.log("====== ====== =========", session_id)
            self.pos.chrome.do_action('pos_sales_dashboard.report_pos_inventory_session_pdf_front',{additional_context:{
                active_ids:[session_id],
            }}).catch(function(){
                alert("Connection lost");
            });
        },
        session_report_thermal: function(e){
            var self = this;
            var session_id = $(e.currentTarget).data('id');
            var report_name = "pos_sales_dashboard.front_inventory_session_thermal_report_template";
            var params = {
                model: 'ir.actions.report',
                method: 'get_html_report',
                args: [session_id, report_name],
            }
            rpc.query(params, {async: false})
            .then(function(report_html){
                if(report_html && report_html[0]){
                    self.pos.proxy.print_receipt(report_html[0]);
                }
            });
        },
        location_report_pdf: function(e){
            var self = this;
            var location_id = $(e.currentTarget).data('id');
            self.pos.chrome.do_action('pos_sales_dashboard.report_pos_inventory_location_pdf_front',{additional_context:{
                active_ids:[location_id],
            }}).catch(function(){
                alert("Connection lost");
            });
        },
        location_report_thermal: function(e){
            var self = this;
            var location_id = $(e.currentTarget).data('id');
            var report_name = "pos_sales_dashboard.front_inventory_location_thermal_report_template";
            var params = {
                model: 'ir.actions.report',
                method: 'get_html_report',
                args: [location_id, report_name],
            }
            rpc.query(params, {async: false})
            .then(function(report_html){
                if(report_html && report_html[0]){
                    self.pos.proxy.print_receipt(report_html[0]);
                }
            });
        },
    });
    gui.define_popup({name:'report_popup', widget: ReportPopupWidget});

});