# -*- coding: utf-8 -*-

# Created on 2018-10-30
# author: 广州尚鹏，https://www.sunpop.cn
# email: 300883@qq.com
# resource of Sunpop
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# Odoo在线中文用户手册（长期更新）
# https://www.sunpop.cn/documentation/user/10.0/zh_CN/index.html

# Odoo10离线中文用户手册下载
# https://www.sunpop.cn/odoo10_user_manual_document_offline/
# Odoo10离线开发手册下载-含python教程，jquery参考，Jinja2模板，PostgresSQL参考（odoo开发必备）
# https://www.sunpop.cn/odoo10_developer_document_offline/
# description:

from odoo import api, fields, models, exceptions, _


class ProductTemplate(models.Model):
    _inherit = ['product.template']

    # 计算出来的 seq，当没有时自动使用上级的
    auto_tracking_number = fields.Boolean('Auto Create Tracking Number', default=True)
    tracking_sequence = fields.Many2one('ir.sequence', 'Auto Serial Numbers Sequence',
                                        auto_join=True, domain="[('code', 'ilike', 'product.tracking')]")



