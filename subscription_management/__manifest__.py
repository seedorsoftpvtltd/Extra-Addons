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
  "name"                 :  "Subscription Management",
  "summary"              :  """This module helps to create a subscription from the sales order on the basis of product.""",
  "category"             :  "Sales",
  "version"              :  "1.3.3",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Subscription-Management.html",
  "description"          :  """This module helps to create a subscription from the sales order on the basis of product. handle subscription-based services in Odoo, Easily manage recurring bills in odoo, Subscription management Software in odoo, Use of subscription module for odoo users, module for subscription management in odoo, recurring billing management in odoo, Subscription Module for Odoo, how to manage recurring services bills in Odoo, subscription services, subscription, Odoo subscription, manage subscription products in Odoo, Subscription products.""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=subscription_management&version=11.0",
  "depends"              :  [
                             'sale_management',
                             'product',
                             'base',
                            ],
  "data"                 :  [
                             'security/subscription_security.xml',
                             'security/ir.model.access.csv',
                             'views/inherit_product_view.xml',
                             'views/subscription_plan_view.xml',
                             'views/subscription_subscription_view.xml',
                             'views/subscription_sequence.xml',
                             'views/res_config_view.xml',
                             'wizard/cancel_reason_wizard_view.xml',
                             'wizard/message_wizard_view.xml',
                             'wizard/sale_order_line_wizard_view.xml',
                             'views/refund_invoice.xml',
                             'views/subscription_reason_view.xml',
                             'data/automatic_invoice.xml',
                            ],
 # "demo"                 :  ['data/subscription_management_data.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  69,
  "currency"             :  "USD",
 # "pre_init_hook"        :  "pre_init_check",
}
