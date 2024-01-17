# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta ,date
from odoo import api, fields, models,tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.osv import expression


class InterWarehouseTransfer(models.Model):
	_name = 'inter.warehouse.transfer'
	_inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
	_mail_post_access = 'read'
	_description = 'Inter Warehouse Transfer'	
	_order = 'id desc'



	name = fields.Char(string='Transfer Reference', required=True, readonly=True, default='New', copy=False)
	company_id = fields.Many2one('res.company', 'Company',default=lambda self: self.env.company, index=True)
	
	transfer_type = fields.Selection([('request','Request'),('make_transfer','Make Transfer')],default='request', 
		string='Transfer Type',required=True,readonly=True,states={'draft': [('readonly', False)] })
	
	state = fields.Selection([('draft','Draft'),('waiting','Waiting'),
		('done','Done'), ('return','Return')], default='draft', string='State',track_visibility='always')

	from_loc_id = fields.Many2one('stock.location',string="From (Pick up) Location",required=True,track_visibility='always',
		domain = "[('usage', '=', 'internal'),('company_id', 'in', [company_id,False])]",
		readonly=True,states={'draft': [('readonly', False)] })
	dest_loc_id = fields.Many2one('stock.location',string="To (Dropdown) Location",required=True,track_visibility='always',
		domain = "[('usage', '=', 'internal'),('company_id', 'in', [company_id,False])]",
		readonly=True,states={'draft': [('readonly', False)] })

	transfer_lines = fields.One2many("inter.transfer.line","iwt_id",string="Transfer Lines",
		readonly=True,states={'draft': [('readonly', False)] })

	validated_by_src = fields.Boolean("Validated By Source",default=False,copy=False)


	picking_id = fields.Many2one('stock.picking',"Picking",copy=False)
	validate = fields.Boolean('Show Validate Button', default= False, copy=False)
	r_id = fields.Many2one('return.inter.warehouse.transfer')
	


	@api.onchange('transfer_type','from_loc_id','dest_loc_id')
	def onc_transfer_type(self):
		user = self.env.user
		location_id = self.env['stock.picking.type'].sudo().search([('company_id', '=', user.company_id.id), ('code', '=', 'internal')], limit=1)
		src_id = location_id.default_location_src_id
		dest_id = location_id.default_location_dest_id
		
		selected_src = self.from_loc_id 
		selected_dest = self.dest_loc_id
		
		if user:
			if self.transfer_type == 'request':
				if not selected_dest:
					self.dest_loc_id = dest_id.id
				if self.dest_loc_id == self.from_loc_id :
					self.from_loc_id = False
			else:
				if not selected_src:
					self.from_loc_id = src_id.id
				if self.dest_loc_id == self.from_loc_id :
					self.dest_loc_id = False
			if selected_src and selected_dest and selected_src == selected_dest :
				return {
					'warning': {
						'title': _('Same Source and Destination Locations.'),
						'message': _("You can not set same location as source and destination location.")
					}
				}		

	
	@api.model
	def create(self, vals):
		vals['name'] = self.env['ir.sequence'].next_by_code('inter.warehouse.transfer') or 'New'
		res = super(InterWarehouseTransfer, self).create(vals)
		return res



	def reset_to_draft(self):
		self.write({'state':'draft'})


	def validate(self):
		for qty in self.picking_id.sudo().move_lines:
			qty.write({
				'quantity_done' : qty.product_uom_qty
			})
		self.picking_id.sudo().button_validate()
		self.picking_id.sudo().action_done()

	def process(self):
		if len(self.transfer_lines) < 1:
			raise ValidationError(_("No Product is added. Please add some products to transfer."))
		else:
			trnsfr = 'MAKE TRANSFER' if self.transfer_type == 'make_transfer' else 'REQUEST'
			src_name = self.sudo().from_loc_id.complete_name
			dest_name = self.sudo().dest_loc_id.complete_name
			message = _("<b>Transfer Type :%s,<br/>From : %s,<br/>To : %s</b>") % (trnsfr,src_name, dest_name)
			self.message_post(body=message)
			self.write({'state':'waiting'})
			self.create_picking()

	

	def create_picking(self):
		picking_obj = self.env['stock.picking']
		pick_type_obj = self.env['stock.picking.type']
		pck_type = pick_type_obj.sudo().search([('code','=','internal'),
			('default_location_src_id','=',self.from_loc_id.id),
			('default_location_dest_id','=',self.dest_loc_id.id)
		])
		if not pck_type :
			s_code = 'INT'+'/'+str(self.from_loc_id.id)+'/'+str(self.dest_loc_id.id)+'/'
			src_name = self.sudo().from_loc_id.complete_name
			dest_name = self.sudo().dest_loc_id.complete_name
			pck_type = pick_type_obj.sudo().create({
				'name' : 'Internal Warehouse Transfer '+'/'+str(src_name)+'->'+str(dest_name),
				'code' : 'internal',
				'default_location_src_id' : self.from_loc_id.id,
				'default_location_dest_id' : self.dest_loc_id.id,
				'sequence_code' : s_code,
				'warehouse_id': False,
			})

		create_vals = {
			'scheduled_date' : datetime.now(),
			'picking_type_id': pck_type.id,
			'location_id': self.from_loc_id.id,
			'location_dest_id': self.dest_loc_id.id,
			'move_type': 'direct',
			'inter_trans_id' : self.id,
			'origin' : 'Internal Transfer',
			'name' : pck_type.sudo().sequence_id.next_by_id()
		}

		pick_id = picking_obj.sudo().create(create_vals)
		message = _("This transfer has been created from the Inter Warehouse Transfer: <a href=# data-oe-model=inter.warehouse.transfer data-oe-id=%d>%s</a>") % (self.id, self.name)

		for line in self.transfer_lines :
			mv = self.env['stock.move'].sudo().create({
				'name': line.product_id.display_name,
				'product_uom': line.product_id.uom_id.id,
				'picking_id': pick_id.id,
				'picking_type_id': pck_type.id,
				'product_id': line.product_id.id,
				'product_uom_qty': abs(line.qty),
				'state': 'draft',
				'location_id': self.from_loc_id.id,
				'location_dest_id': self.dest_loc_id.id,
			})

			mvl = self.env['stock.move.line'].sudo().create({
				'picking_id':pick_id.id,
				'location_id':pick_id.location_id.id,
				'location_dest_id':pick_id.location_dest_id.id,
				'qty_done': line.qty,
				'product_id': line.product_id.id,
				'move_id':mv.id,
				'product_uom_id':line.product_id.uom_id.id,
			})

		pick_id.sudo().action_confirm()
		# pick_id.sudo().action_assign()

		self.write({
			'picking_id' : pick_id.id,
		})

	def action_view_picking(self):
		return{
			'name': _('Stock Transfer'),
			'view_mode': 'tree,form',
			'res_model': 'stock.picking',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': ['|', ('id', '=',self.sudo().picking_id.id), ('backorder_id', '=', self.sudo().picking_id.id)],
		}
	
	
	
	def action_view_return_inter_warehouse(self):
		return{
			'name': _('Return Inter Warehouse Transfer'),
			'view_mode': 'tree,form',
			'res_model': 'return.inter.warehouse.transfer',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': [('id', '=',self.sudo().r_id.id)],

		}
	
	
	def action_view_return_form(self):
	    '''
	    This function returns an action that display existing vendor bills of given purchase order ids.
	    When only one found, show the vendor bill immediately.
	    '''
	    action = self.env.ref('bi_inter_warehouse_transfer_generic.action_return_warehouse_form_template')
	    result = action.read()[0]
	
	    # override the context to get rid of the default filtering
	    
	    value = []
	    for i in self.transfer_lines:
	        vals = ({
	        'product_id' : i.product_id.id,
	        'qty' : i.qty,
	        })
	        value.append(vals)
	    result['context'] = {
 	      'default_internal_id': self.id,
	        'default_from_loc_id': self.from_loc_id.id,
	        'default_dest_loc_id': self.dest_loc_id.id,
	        'default_transfer_lines':value
	    }
	
	    return result
