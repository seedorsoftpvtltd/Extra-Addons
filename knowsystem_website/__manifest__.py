# -*- coding: utf-8 -*-
{
    "name": "KnowSystem: Website and Portal",
    "version": "13.0.2.0.10",
    "category": "Website",
    "author": "faOtools",
    "website": "https://faotools.com/apps/13.0/knowsystem-website-and-portal-433",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "knowsystem",
        "website"
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/knowsystem_article.xml",
        "views/knowsystem_tag.xml",
        "views/res_partner.xml",
        "wizard/article_update.xml",
        "views/views.xml",
        "views/templates.xml",
        "views/res_config_settings.xml"
    ],
    "qweb": [
        
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The extension to KnowSystem to publish articles to portal and public users",
    "description": """
For the full details look at static/description/index.html

* Features * 
- Share knowledge base articles with portal users
- Publish knowledge system articles for community
- Use website builder to prepare new articles



#odootools_proprietary

    """,
    "images": [
        "static/description/main.png"
    ],
    "price": "40.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=84&ticket_version=13.0&url_type_id=3",
}