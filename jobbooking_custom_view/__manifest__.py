{
    'name': 'Job Booking custom view',
    'author': 'Arun Seedor',
    'summary': """
                   module contains the view that added extra in front end to setup in a backend.
               """,
    'description': """
                    
                    """,
    'depends': ['scs_freight',"hb_freight_extend"],
    'data': [
        'views/job_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}