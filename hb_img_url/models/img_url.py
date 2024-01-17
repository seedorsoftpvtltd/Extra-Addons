import base64  # file encode
import urllib.request  # file download from url

from odoo.http import request
from odoo import api, fields, models, tools, osv, http, _
import odoo.osv.osv


class soreport(models.Model):
    _inherit = "sale.order"

    def so_report_urls(self, orderid):
        print(orderid)
        id = self.env['sale.order'].search([('id', '=', orderid)])
        print(id)
        hb = id._portal_ensure_token()
        print(hb)
        access_token = id.access_token
        print(access_token)
        print(request.httprequest.environ['HTTP_HOST'])
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        print(base_url)
        print_url = '%s/my/orders/%s?access_token=%s&report_type=pdf' % (base_url, orderid, id.access_token)
        download_url = '%s/my/orders/%s?access_token=%s&report_type=pdf&download=true' % (
        base_url, orderid, id.access_token)
        print(print_url, download_url)
        return print_url, download_url

        # for record in self:
        #     print(record.id)
        #     if record.id == orderid:
        #         base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        #         print_url = 'https://%s/my/orders/%s?access_token=%s&report_type=pdf' % (base_url, orderid, record.access_token)
        #         download_url = 'https://%s/my/orders/%s?access_token=%s&report_type=pdf&download=true' % (base_url, orderid, record.access_token)
        #         print(print_url, download_url)
        #     return print_url, download_url


class invreport(models.Model):
    _inherit = "account.move"

    def inv_report_urls(self, orderid):
        print(orderid)
        id = self.env['account.move'].search([('id', '=', orderid)])
        print(id)
        hb = id._portal_ensure_token()
        print(hb)
        access_token = id.access_token
        print(access_token)
        print(request.httprequest.environ['HTTP_HOST'])
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        print(base_url)
        print_url = '%s/my/invoices/%s?access_token=%s&report_type=pdf' % (base_url, orderid, id.access_token)
        download_url = '%s/my/invoices/%s?access_token=%s&report_type=pdf&download=true' % (
        base_url, orderid, id.access_token)
        print(print_url, download_url)
        return print_url, download_url


class image_url(models.Model):
    _inherit = "product.product"

    image_url = fields.Char('Image url', related='img.local_url')
    image_location = fields.Char('Image location', compute='_image_location')
    img = fields.Many2one('ir.attachment', string="Image Attachment", compute='_img_att')

    @api.depends('image_url')
    def _image_location(self):
        for rec in self:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            url = rec.image_url
            if url:
                rec['image_location'] = base_url + url
            else:
                rec['image_location'] = ''

                # @api.depends('image_1920')

    # def _img_url(self):
    #     for rec in self:
    #         print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    #         base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #         url = '%s/web/image?model=product.product&id=%s&field=image_1920' % (base_url, rec.id)
    #         rec['image_url'] = url

    @api.depends('image_1920')
    def _img_att(self):
        for rec in self:
            print(request.session, 'jjjjjjjjjjjjjjjjjjj')
            if rec.image_1920 and rec.img:
                att = rec.img
                att.datas = rec.image_1920
                print(rec.img, rec.image_url)
            if rec.image_1920 and not rec.img:
                print('publiccccccccccccccccc')
                # for rec in self:
                print("bbbbbbbbbbbbbbbbbbbbbbbbb")
                vals = {
                    'name': 'Product Image',
                    'type': 'binary',
                    'res_id': rec.id,
                    'res_model': 'product.product',
                    'public': True,
                    'datas': rec.image_1920,
                    # 'res_field':'img'
                    # 'local_url':'/web/image?model=product.product&id=%s&field=image_1920' % (rec.id),

                }
                # print(vals)
                old = self.env['ir.attachment'].search([('id', '=', rec.id)])
                print(old, 'old')
                if not old:
                    att = self.env['ir.attachment'].create(vals)
                    rec['img'] = att
                    print(rec.img, rec.image_url)

            else:
                rec['img'] = []

    # @api.onchange('image_1920')
    # def _onchange_img_att(self):
    #     for rec in self:
    #         if rec.image_1920 and rec.img:
    #             att = rec.img
    #             att.datas = rec.image_1920
    #             print(rec.img, rec.image_url)

    # def hbb(self):
    #     # for
    #     print('publiccccccccccccccccc')
    #     # for rec in self:
    #     print("bbbbbbbbbbbbbbbbbbbbbbbbb")
    #     vals = {
    #         'name': 'Product Image',
    #         'type': 'binary',
    #         'res_id': self.id,
    #         'res_model': 'product.product',
    #         'public': True,
    #         'datas': self.image_1920
    #         # 'local_url':'/web/image?model=product.product&id=%s&field=image_1920' % (rec.id),
    #
    #     }
    #     print(vals)
    #     att = self.env['ir.attachment'].create(vals)
    #     self['img'] = att
    #
    #
    #     print(self.img)

    # @api.model
    # def create(self, vals):
    #     print('publiccccccccccccccccc')
    #     image_1920 = {'public': True}
    #     vals.update(image_1920)
    #     return super(image_url,self).create(vals)

    # @http.route(["/web/image?model=product.product&id=6&field=image_1920"],type='http', auth='public', website=True)
    # def image_url(self):
    #     print("hgfdsdfgh")
    #     return request.redirect("/contactus")


class Attachmentimg(models.Model):
    _inherit = "ir.attachment"

    def publicimg(self):
        print(self.res_model)
        if self.res_model == 'product.product':
            self.public = True
