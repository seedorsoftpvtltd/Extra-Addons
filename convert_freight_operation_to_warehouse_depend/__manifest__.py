{
    'name' : 'Job Booking to ASN Depend',
    'version' : '1.1',
    'summary': 'Job Booking to ASN',
    'sequence': 15,
    'description': """======================""",
    'category': 'Hr',
    'website': ' ',
    'images' : [],
    'depends' : ['warehouse','scs_freight',"jobbooking_custom_view","hb_freight_extend"],
    'data': [
       'views/views.xml',
],
    'installable': True,
    #'application': True,
    #'auto_install': False,
    # 'post_init_hook': '_auto_install_l10n',
}
