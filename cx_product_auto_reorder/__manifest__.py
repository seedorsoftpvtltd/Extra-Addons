###################################################################################
# 
#    Copyright (C) 2020 Cetmix OÜ
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU LESSER GENERAL PUBLIC LICENSE as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

# -*- coding: utf-8 -*-
{
    'name': 'Advanced Auto Reordering Rules Control. Create and Manage Reordering Rules using Templates, Automatic Reordering Rule Order Point Generator',
    'version': '13.0.1.0',
    'author': 'Ivan Sokolov, Cetmix',
    'category': 'Warehouse',
    'license': 'LGPL-3',
    'website': 'https://demo.cetmix.com',
    'live_test_url': 'https://demo.cetmix.com',
    'summary': """Create and manage reordering rules automatically using templates""",
    'description': """
    Create reordering rules automatically from templates. Create stock orderpoint automatically. Use template to manage
     reordering rules. Automatically generate purchase order, Automatically generate manufacturing order. 
""",
    'depends': ['stock'],
    'images': ['static/description/banner.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/cx_stock_product.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
