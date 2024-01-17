# -*- coding: utf-8 -*-
{
    "name": "KnowSystem: Knowledge Base System",
    "version": "13.0.2.0.17",
    "category": "Extra Tools",
    "author": "faOtools",
    "website": "https://faotools.com/apps/13.0/knowsystem-knowledge-base-system-432",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "mail",
        "web_editor"
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/res_config_settings.xml",
        "views/know_system_article_revision.xml",
        "views/knowsystem_article_template.xml",
        "wizard/create_from_template.xml",
        "views/editor/options.xml",
        "views/editor/snippets.xml",
        "views/knowsystem_article.xml",
        "views/knowsystem_section.xml",
        "views/knowsystem_tag.xml",
        "views/knowsystem_tour.xml",
        "views/ir_attachment.xml",
        "reports/article_report.xml",
        "reports/article_report_template.xml",
        "wizard/article_update.xml",
        "wizard/add_to_tour.xml",
        "wizard/article_search.xml",
        "views/menu.xml",
        "wizard/mail_compose_message.xml",
        "data/data.xml"
    ],
    "qweb": [
        "static/src/xml/*.xml"
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to build deep and structured knowledge base for internal and external use. Knowledge System. KMS",
    "description": """

For the full details look at static/description/index.html

* Features * 

- Innovative single-view interface

- Fast, comfortable, and professional knowledge recording

- Get benefit from your knowledge

- &lt;i class='fa fa-globe'&gt;&lt;/i&gt; Individual partner knowledge base portal

- WIKI-like revision system

- &lt;i class='fa fa-globe'&gt;&lt;/i&gt; Public knowledge system

- Team work for knowledge creation

- &lt;i class='fa fa-gears'&gt;&lt;/i&gt; Custom fields to structure knowledge

- Knowledge is secured and might be safely shared

- &lt;i class='fa fa-dedent'&gt;&lt;/i&gt; Website documentation builder

- Create learning tours

- &lt;i class='fa fa-language'&gt;&lt;/i&gt; Multilingual knowledge base

- Knowledge base for any industry and business
 
* Extra Notes *

- Interface solutions

- Available mass actions

- How document types and articles are linked for a quick access

- How to overview articles which might be useful for this document

- How to use company knowledge for communication

- &lt;i class='fa fa-globe'&gt;&lt;/i&gt; How to use the website builder for editing articles

- How to use article templates

- How to recover a previous article version

- How to share knowledge base with specific partners

- How to make an article available for all website visitors

- How custom knowledge attributes work

- How to manage user accesses to articles

- How to configure a learning tour

- How to make an article available for a few languages

- Typical use cases

- How to add sections, tags or &lt;i class='fa fa-gears'&gt;&lt;/i&gt; article types to portal / website



#odootools_proprietary

    """,
    "images": [
        "static/description/main.png"
    ],
    "price": "298.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=83&ticket_version=13.0&url_type_id=3",
}