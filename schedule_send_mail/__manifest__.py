# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "Schedule Emails To Send Later",
    "version" : "13.0.0.6",
    "category" : "Extra Tools",
    'summary': 'Send email scheduled mail with chatter send email later send email later Schedule mail send Schedule emails to send Schedule emails send Delay Send email Scheduling emails to send emailing Schedule send message Scheduling Email send message scheduled',
    "description": """
    
Send Later email in Odoo Write now send later with Schedule Schedule Sending Email Scheduling Email Odoo Scheduling Email odoo Schedule Emails Delay or schedule sending email messages Delay sending email messages
Schedule when messages are delivered Schedule messages are delivered Schedule Emails To Send Later
Scheduling Event Emails Send an email on a schedule Send Campaign Emails
schedule Campaign Emails Emails Campaign schedules Scheduled Emails
Schedule mail send Schedule emails to send Schedule emails send
Schedule email send Scheduling Email Deliveries Schedule Email At Specific Time
send schedule mails send mail on selected date send and link mail with chatter link mail with chatter 
Scheduling emails to send emailing Schedule activities Recurring Activities Schedule Activity
schedule emailing schedule mails schedule messages in odoo Website Emailing
Delay Send email Email Scheduling and Recurring Emails Send Later - Schedule Emails send post email Schedule Emails To Send Later schedule email
    
    """,
    "author": "BrowseInfo",
    "website" : "https://www.browseinfo.in",
    "price": 29,
    "currency": 'EUR',
    "depends" : ['base','sale_management','mail'],
    "data": [
        'security/ir.model.access.csv',
        'views/mail_message_data.xml',
        'views/view_schedule_send_message.xml',
    ],
    'qweb': [
        'static/src/xml/schedule_activity.xml',
        'static/src/xml/schedule_send_message.xml',
        
    ],
    "auto_install": False,
    "installable": True,
    "live_test_url":'https://youtu.be/vQCVH8TOsUc',
    "images":["static/description/Banner.png"],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: