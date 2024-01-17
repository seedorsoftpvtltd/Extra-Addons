# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# from odoo import http
import odoo.http as http
from json import dumps


class ChatterPasteController(http.Controller):

    @http.route('/web_chatter_paste/upload_attachment', type='http', auth="user")
    def upload_attachment(self, **kw):
        request = http.request
        model_obj = request.env['ir.attachment']
        out = """<script language="javascript" type="text/javascript">
                    var win = window.top.window;
                    win.jQuery(win).trigger(%s, %s);
                </script>"""
        attachment = model_obj.create({
            'name': kw['filename'],
            'datas': kw['content'],
            # 'datas_fname': kw['filename'],
            'res_model': kw['model'],
            'res_id': int(kw['id'])
        })
        args = {
            'filename': kw['filename'],
            'mimetype': kw['mimetype'],
            'id': attachment.id
        }
        return out % (dumps(kw['callback']), dumps(args))
