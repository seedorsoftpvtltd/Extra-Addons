{
    'name':'Geofencing',
    'summary': """geo fencing in employees and geo location in attendance""",
    'version': '13.0.1.0.0',
    'description': """geo fencing in employees and geo location in attendance""",
    'author': 'Herlin Breese',
    'company': 'Seedorsoft Pvt Ltd',
    'website': 'https://www.seedorsoft.com',
    'category': 'Tools',
    'depends': ['base','base_setup','hr','base_geolocalize','hr_attendance','attendance_face_recognition'],
    'data': [
        'views/hr_employee_views.xml',
        'views/hr_attendance_views.xml',
        'views/hr_employee_face.xml',
        'views/automation.xml'

    ],
    'installable': True,
}




