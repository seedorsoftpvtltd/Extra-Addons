# -*- coding: utf-8 -*-

{
    "name": "Activity Reminder | Activities Daily Reminder | Mail Activity Reminder | Activity Alarm",
    "version":"13.0.1",
    "license": "OPL-1",
    "support": "relief.4technologies@gmail.com",  
    "author" : "Relief Technologies",  
    "live_test_url": "https://youtu.be/YKd8kfGbRuY",       
    "category": "Extra Tools",
    "summary": "to do list, Daily Activities Management",
    "description": """

    """,
    "depends": ["mail"],
    "data": [

        "views/mail_activity.xml",
        "views/assets_backend.xml",       
    ],
    'qweb': [
        'static/src/xml/systray.xml',
    ],
    
    "images": ["static/description/background.png",],              
    "installable": True,
    "application": True,
    "auto_install": False,
    "price": 35,
    "currency": "EUR"   
}
