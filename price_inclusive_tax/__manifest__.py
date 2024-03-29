# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Price Inclusive For Group Taxes",
  "summary"              :  """With the module, the user can correctly calculate the tax amount for taxes that have multiple components.""",
  "category"             :  "Accounting",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Price-Inclusive-Group-Taxes.html",
  "description"          :  """multiple taxes
Odoo Price Inclusive For Group Taxes
Group taxes calculation
Group tax
Include group tax
calculate group tax
group tax error""",
  "live_test_url"        :  "http://odoo.webkul.com:8010/web?db=gst_db#action=272&model=gst.dashboard&view_type=kanban&cids=&menu_id=165",
  "depends"              :  ['account'],
  "data"                 :  ['views/account_tax_views.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  10,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}