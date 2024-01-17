{
    "name": "Promote Birthday Sales",
    "version": "13.0.1.0.1",
    "author": "Er. Vaidehi Vasani",
    "summary": "Send Birthday Promotion Plans with Greeting Email to Partner/Customer",

    "license": "OPL-1",
    "category": "Extra Tools",

    'author': 'Er. Vaidehi Vasani',
    'maintainer': 'Er. Vaidehi Vasani',

    "data": [
        "views/res_partner_view.xml",
        "views/birthday_reminder_cron.xml",
        "edi/birthday_reminder_action_data.xml",
    ],
    "depends": ["sale_management"],

    'images': ['static/description/birthday_promotion_plan_coverpage.jpeg'],

    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 0.00,
    'currency': 'EUR',
}
