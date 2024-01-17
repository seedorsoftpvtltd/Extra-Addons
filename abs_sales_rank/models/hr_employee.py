# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from odoo import api, fields, models, _

## inherit class 'hr.employee' to get details of employee and set rank according to assigned sale order to salesperson
class Employee(models.Model):
    _inherit = "hr.employee"

    number_sale_order_rank = fields.Integer(string="Rank", compute='sale_order_rank')
    amount_sale_order_rank = fields.Float(string="Amount")

    def sale_order_rank(self):
        employee_rank_list = []
        for employee in self:
            if employee.user_id:
                sale_order_list = []
                total_amount = 0
                sale_orders = self.env['sale.order'].search([('state','in',['sale','done']),('user_id','=',employee.user_id.id)])
                if sale_orders:
                    for order in sale_orders:
                        sale_order_list.append(order)
                        total_amount = total_amount + order.amount_total
                    employee_dict = { 'employee' : employee,'length' : len(sale_order_list),'total_amount' : total_amount}
                    employee_rank_list.append(employee_dict)

                ## sorted dictionary to get rank of employee
                if employee_rank_list:
                    newlist = sorted(employee_rank_list, key=lambda k: k['length'], reverse=True)
                    rank = 0
                    for line in newlist:
                        if line:
                            rank = rank + 1
                            line['employee'].update({'number_sale_order_rank' : rank})
                            line['employee'].write({'amount_sale_order_rank' : line['total_amount']})
            else:
                employee.number_sale_order_rank = 0
                employee.amount_sale_order_rank = 0

