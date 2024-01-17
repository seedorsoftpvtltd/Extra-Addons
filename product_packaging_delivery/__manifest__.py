# -*- coding: utf-8 -*-

{
  "name" : "Product Bundle Pack Package",
  "summary" : """The purpose of this module to add multiple product items in packaging (like cardboard boxes, filling material, etc).""",
  "category" : "Sale","Inventory"
  "version" : "1.0",
  "author" : "HAK Solutions",
      'support':'hunainfast@gmail.com',
   "license": "AGPL-3",
  "description" : """The purpose of this module is to modify the packaging. When you define a new packaging, now you can add multiple product items in packaging (like cardboard boxes, filling material, etc). So when you use this packaging (eg. in a deliverly) the products you tied to packaging are added to the stock picking for the delivery.""",
  "depends" : ['sale','product','stock'],
  "data" : [
    'security/ir.model.access.csv',
    'views/product_pack.xml',
  ],
 'images': ['static/description/icon.png'],
  "application" : True,
  "installable" : True,
  "auto_install" : False,
    "price": 0,
    "currency": "EUR",

}
