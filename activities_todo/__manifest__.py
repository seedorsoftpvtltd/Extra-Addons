# -*- coding: utf-8 -*-
{
    "name": "Activities To-Do Interface",
    "version": "13.0.1.0.3",
    "category": "Productivity",
    "author": "faOtools",
    "website": "https://faotools.com/apps/13.0/activities-to-do-interface-393",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "mail"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/assets.xml",
        "data/data.xml",
        "wizard/do_with_feedback.xml",
        "wizard/create_new_activity.xml",
        "views/mail_activity_todo.xml",
        "views/res_users.xml"
    ],
    "qweb": [
        "static/src/xml/*.xml"
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to process activities one-by-one in a single interface",
    "description": """
For the full details look at static/description/index.html

* Features * 
- 2 clicks to start working
- Any decision by each activity
- Full information to do a task
- Only topical activities



#odootools_proprietary

    """,
    "images": [
        "static/description/main.png"
    ],
    "price": "48.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=98&ticket_version=13.0&url_type_id=3",
}