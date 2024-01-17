{
        'name': 'RFQ Public Form',
        'version': '0.1',
        'category': 'Purchase',
        'author': 'Herlin Breese J',
        'summary': '',
        'description': """
        
    """,
    'depends': [
        'base','web','mail','purchase','sale', 'purchase_requisition', 'purchase_comparison_chart'
    ],

    'data': [
        'views/view.xml',
        'views/agreement.xml',
    ],

    'installable': True,
    'application': True,
}