# -*- coding: utf-8 -*-
{
    "name": "Odoo Documentation Builder",
    "version": "13.0.1.0.4",
    "category": "Website",
    "author": "faOtools",
    "website": "https://faotools.com/apps/13.0/odoo-documentation-builder-475",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "knowsystem_website"
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/data.xml",
        "views/res_config_settings.xml",
        "views/documentation_section.xml",
        "views/documentation_category.xml",
        "views/documentation_version.xml",
        "wizard/add_to_documentation.xml",
        "views/templates.xml",
        "views/menu.xml",
        "views/views.xml"
    ],
    "qweb": [
        "static/src/xml/*.xml"
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to create website documentation based on your knowledge base",
    "description": """
For the full details look at static/description/index.html

* Features * 
- Structured and Customizable Documentation
- Simple to Prepare and Update
- Dynamic Navigation
- Inline Search
- Documentation Versioning
- Documentation Security
- Multi Websites



#odootools_proprietary

    """,
    "images": [
        "static/description/main.png"
    ],
    "price": "99.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=137&ticket_version=13.0&url_type_id=3",
}