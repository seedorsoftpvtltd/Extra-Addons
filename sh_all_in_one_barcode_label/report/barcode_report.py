# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, models


class BarcodeReport(models.AbstractModel):
    _name = 'report.sh_all_in_one_barcode_label.sh_barcode_report_doc'
    _description = 'Barcode Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        data_list = []
        template_id = self.env['sh.dynamic.template'].sudo().browse(
            data.get('sh_lable_template_id'))
        template_line = template_id.sh_template_line_ids.sudo().search(
            [('sh_field_id', '=', template_id.sh_barcode_field_id.id),('template_id','=',template_id.id)], limit=1)
        if template_line:
            for record in data.get('product_dic'):
                product_id = self.env['product.product'].sudo().browse(
                    int(record.get('product_id')))
                for i in range(0, record.get('qty')):
                    product_vals = {}
                    for line in template_id.sh_template_line_ids:
                        field_value = line.sh_field_id.name
                        field_type = line.sh_field_id.ttype
                        style = ''
                        if line.sh_margin:
                            style += 'padding:'+line.sh_margin + ';'
                        if line.sh_font_size:
                            style += 'font-size:'+line.sh_font_size + ';'
                        if line.sh_font_color:
                            style += 'color:'+line.sh_font_color + ';'
                        if line.sh_position:
                            style += 'text-align:'+line.sh_position + ';'
                        if line.sh_font_bold:
                            style += 'font-weight:bold;'
                        if line.sh_font_underline:
                            style += 'text-decoration: underline;'
                        if line.sh_font_italic:
                            style += 'font-style: italic;'
                        if line.id == template_line.id:
                            template_field = template_id.sh_barcode_field_id.name
                            template_field_value = product_id[template_field]
                            if template_id.sh_barcode_field_id.ttype == 'many2one':
                                template_field_value = product_id[template_field].name
                            if template_id.sh_print_barcode_or_qr == 'qr':
                                if template_id.sh_label_display:
                                    label_style = ''
                                    if line.sh_margin:
                                        label_style += 'padding:'+line.sh_margin + ';'
                                    if line.sh_font_size:
                                        label_style += 'font-size:'+line.sh_font_size + ';'
                                    if line.sh_font_color:
                                        label_style += 'color:'+line.sh_font_color + ';'
                                    if line.sh_position:
                                        label_style += 'text-align:'+line.sh_position + ';'
                                    if line.sh_font_bold:
                                        label_style += 'font-weight:bold;'
                                    if line.sh_font_underline:
                                        label_style += 'text-decoration: underline;'
                                    if line.sh_font_italic:
                                        label_style += 'font-style: italic;'
                                    if line.sh_field_id.ttype == 'many2one':
                                        product_vals.update({
                                            'barcode_url': ['/report/barcode/QR/' + str(product_id[line.sh_field_id.name].name), template_field_value, label_style],
                                        })
                                    else:
                                        product_vals.update({
                                            'barcode_url': ['/report/barcode/QR/' + str(product_id[line.sh_field_id.name]), template_field_value, label_style],
                                        })
                                else:
                                    if line.sh_field_id.ttype == 'many2one':
                                        product_vals.update({
                                            'barcode_url': ['/report/barcode/QR/' + str(product_id[line.sh_field_id.name].name)],
                                        })
                                    else:
                                        product_vals.update({
                                            'barcode_url': ['/report/barcode/QR/' + str(product_id[line.sh_field_id.name])],
                                        })
                            elif template_id.sh_print_barcode_or_qr == 'barcode':
                                if template_id.sh_label_display:
                                    label_style = ''
                                    if line.sh_margin:
                                        label_style += 'padding:'+line.sh_margin + ';'
                                    if line.sh_font_size:
                                        label_style += 'font-size:'+line.sh_font_size + ';'
                                    if line.sh_font_color:
                                        label_style += 'color:'+line.sh_font_color + ';'
                                    if line.sh_position:
                                        label_style += 'text-align:'+line.sh_position + ';'
                                    if line.sh_font_bold:
                                        label_style += 'font-weight:bold;'
                                    if line.sh_font_underline:
                                        label_style += 'text-decoration: underline;'
                                    if line.sh_font_italic:
                                        label_style += 'font-style: italic;'
                                    if line.sh_field_id.ttype == 'many2one':
                                        product_vals.update({
                                            'barcode_url': ['/report/barcode/' + str(template_id.sh_barcode_type)+'/'+str(product_id[line.sh_field_id.name].name), template_field_value, label_style],
                                        })
                                    else:
                                        product_vals.update({
                                            'barcode_url': ['/report/barcode/' + str(template_id.sh_barcode_type)+'/'+str(product_id[line.sh_field_id.name]), template_field_value, label_style],
                                        })
                                else:
                                    if line.sh_field_id.ttype == 'many2one':
                                        product_vals.update({
                                            'barcode_url': ['/report/barcode/' + str(template_id.sh_barcode_type)+'/'+str(product_id[line.sh_field_id.name].name)],
                                        })
                                    else:
                                        product_vals.update({
                                            'barcode_url': ['/report/barcode/' + str(template_id.sh_barcode_type)+'/'+str(product_id[line.sh_field_id.name])],
                                        })
                        else:
                            if line.sh_field_id.ttype == 'many2one':
                                product_vals.update({
                                    line.sh_field_id.name: [product_id[field_value].name, style],
                                })
                            elif line.sh_field_id.ttype == 'binary':
                                if product_id[field_value]:
                                    image_style = ''
                                    td_style = ''
                                    if line.sh_position:
                                        td_style += 'text-align:'+line.sh_position + ';'
                                    if line.sh_margin:
                                        image_style += 'padding:'+line.sh_margin + ';'
                                    if line.image_height:
                                        image_style += 'height:'+line.image_height + ';'
                                    if line.image_width:
                                        image_style += 'width:'+line.image_height + ';'
                                    product_vals.update({
                                        line.sh_field_id.name: [product_id[field_value], image_style,'binary_field',td_style],
                                    })
                            else:
                                if line.type == 'field':
                                    if line.sh_is_price_field and line.sh_currency_position == 'after':
                                        if field_type == 'float':
                                            value_of_field = format(product_id[field_value],'.2f')
                                            product_vals.update({
                                                line.sh_field_id.name: [str(value_of_field)+' ' + line.currency_id.symbol, style],
                                            })
                                        else:
                                            product_vals.update({
                                                line.sh_field_id.name: [str(product_id[field_value])+' ' + line.currency_id.symbol, style],
                                            })
                                    elif line.sh_is_price_field and line.sh_currency_position == 'before':
                                        if field_type == 'float':
                                            value_of_field = format(product_id[field_value],'.2f')
                                            product_vals.update({
                                                line.sh_field_id.name: [line.currency_id.symbol + ' '+str(value_of_field), style],
                                            })
                                        else:
                                            product_vals.update({
                                                line.sh_field_id.name: [line.currency_id.symbol + ' '+str(product_id[field_value]), style],
                                            })
                                    else:
                                        if field_type == 'float':
                                            value_of_field = format(product_id[field_value],'.2f')
                                            product_vals.update({
                                                line.sh_field_id.name: [value_of_field, style],
                                            })
                                        else:
                                            product_vals.update({
                                                line.sh_field_id.name: [product_id[field_value], style],
                                            })
                                else:
                                    product_vals.update({
                                        'sample_text': [str(line.name), style,'sample_text'],
                                    })
                    data_list.append(product_vals)
        else:
            for record in data.get('product_dic'):
                product_id = self.env['product.product'].sudo().browse(
                    int(record.get('product_id')))
                for i in range(0, record.get('qty')):
                    product_vals = {}
                    for line in template_id.sh_template_line_ids:
                        field_value = line.sh_field_id.name
                        field_type = line.sh_field_id.ttype
                        style = ''
                        if line.sh_margin:
                            style += 'padding:'+line.sh_margin + ';'
                        if line.sh_font_size:
                            style += 'font-size:'+line.sh_font_size + ';'
                        if line.sh_font_color:
                            style += 'color:'+line.sh_font_color + ';'
                        if line.sh_position:
                            style += 'text-align:'+line.sh_position + ';'
                        if line.sh_font_bold:
                            style += 'font-weight:bold;'
                        if line.sh_font_underline:
                            style += 'text-decoration: underline;'
                        if line.sh_font_italic:
                            style += 'font-style: italic;'
                        if line.sh_field_id.ttype == 'many2one':
                            product_vals.update({
                                line.sh_field_id.name: [product_id[field_value].name, style],
                            })
                        elif line.sh_field_id.ttype == 'binary':
                            if product_id[field_value]:
                                image_style = ''
                                td_style = ''
                                if line.sh_position:
                                    td_style += 'text-align:'+line.sh_position + ';'
                                if line.sh_margin:
                                    image_style += 'padding:'+line.sh_margin + ';'
                                if line.image_height:
                                    image_style += 'height:'+line.image_height + ';'
                                if line.image_width:
                                    image_style += 'width:'+line.image_height + ';'
                                product_vals.update({
                                    line.sh_field_id.name: [product_id[field_value], image_style,'binary_field',td_style],
                                })
                        else:
                            if line.type == 'field':
                                if line.sh_is_price_field and line.sh_currency_position == 'after':
                                    if field_type == 'float':
                                        value_of_field = format(product_id[field_value],'.2f')
                                        product_vals.update({
                                            line.sh_field_id.name: [str(value_of_field)+' ' + line.currency_id.symbol, style],
                                        })
                                    else:
                                        product_vals.update({
                                            line.sh_field_id.name: [str(product_id[field_value])+' ' + line.currency_id.symbol, style],
                                        })
                                elif line.sh_is_price_field and line.sh_currency_position == 'before':
                                    if field_type == 'float':
                                        value_of_field = format(product_id[field_value],'.2f')
                                        product_vals.update({
                                            line.sh_field_id.name: [line.currency_id.symbol + ' '+str(value_of_field), style],
                                        })
                                    else:
                                        product_vals.update({
                                            line.sh_field_id.name: [line.currency_id.symbol + ' '+str(product_id[field_value]), style],
                                        })
                                else:
                                    if field_type == 'float':
                                        value_of_field = format(product_id[field_value],'.2f')
                                        product_vals.update({
                                            line.sh_field_id.name: [value_of_field, style],
                                        })
                                    else:
                                        product_vals.update({
                                            line.sh_field_id.name: [product_id[field_value], style],
                                        })
                            else:
                                product_vals.update({
                                    'sample_text': [str(line.name), style,'sample_text'],
                                })
                    data_list.append(product_vals)
        barcode_style = ''
        align_style = ''
        if template_id.sh_barcode_height:
            barcode_style += 'height:' + template_id.sh_barcode_height + ';'
        if template_id.sh_barcode_width:
            barcode_style += 'width:' + template_id.sh_barcode_width + ';'
        if template_line:
            align_style += 'text-align:' + str(template_line.sh_position)
        data.update({
            'data_list': data_list,
            'barcode_style': barcode_style,
            'align_style': align_style
        })
        return data
