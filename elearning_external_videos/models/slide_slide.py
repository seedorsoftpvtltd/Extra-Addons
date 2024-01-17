# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import datetime
import io
import re
import requests
import PyPDF2
import json
import mimetypes

from PIL import Image
from werkzeug import urls

from odoo import api, fields, models, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.exceptions import Warning, UserError, AccessError
from werkzeug import urls
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import url_for

class Channel(models.Model):
    """ A channel is a container of slides. """
    _inherit = 'slide.channel'
    _name = 'slide.channel'

    nbr_zoom_meeting = fields.Integer('Zoom Meeting', compute='_compute_slides_statistics', store=True)
    nbr_externalvideo = fields.Integer('External Videos (mp4)', compute='_compute_slides_statistics', store=True)
    nbr_googledrivevideo = fields.Integer('Google Drive Videos', compute='_compute_slides_statistics', store=True)
    nbr_clapprvideo = fields.Integer('External Videos (livestream and other supported)', compute='_compute_slides_statistics', store=True)
    nbr_vimeovideo = fields.Integer('Vimeo Videos', compute='_compute_slides_statistics', store=True)
    nbr_localvideo = fields.Integer('Local Video', compute='_compute_slides_statistics', store=True)

class Slide(models.Model):
    _inherit = 'slide.slide'
    _name = 'slide.slide'

    # content
    slide_type = fields.Selection(selection_add=[
        ('externalvideo', 'MP4 external video'),
        ('googledrivevideo', 'Google Drive video (put long id, example: 1oOIeTJwf4CWTRmcOONtTigfGDQpCMHPe)'),
        ('clapprvideo', 'External video (mp4, etc, livestream m3u8 and other supported formats)'),
        ('vimeovideo', 'Vimeo Video'),
        ('localvideo', 'Local Video (Ensure upload size limit in your server)'),
        ("zoom_meeting","Zoom Meeting")])
    external_url = fields.Char(string="External video URL")
    localvideo_mime_type = fields.Char(string="Localvideo mime type")
    zoom_meeting_ID = fields.Char(string="Meeting ID")
    zoom_meeting_name = fields.Char(string="Zoom Meeting Name", placeholder="Paste Here Zoom Meeting Name")
    nbr_zoom_meeting = fields.Integer('Zoom Meeting', compute='_compute_slides_statistics', store=True)
    nbr_externalvideo = fields.Integer('External Video', compute='_compute_slides_statistics', store=True)
    nbr_googledrivevideo = fields.Integer('Google Drive Video', compute='_compute_slides_statistics', store=True)
    nbr_clapprvideo = fields.Integer('External Video (livestream and other supported)', compute='_compute_slides_statistics', store=True)
    nbr_vimeovideo = fields.Integer('Vimeo Video', compute='_compute_slides_statistics', store=True)
    nbr_localvideo = fields.Integer('Local Video', compute='_compute_slides_statistics', store=True)

    @api.depends('document_id', 'slide_type', 'mime_type', 'external_url')
    def _compute_embed_code(self):
        res = super(Slide, self)._compute_embed_code()
        for record in self:
            if record.slide_type == 'externalvideo':
                content_url = record.external_url
                record.embed_code = '<video class="external_video" controls controlsList="nodownload"><source src="' + content_url + '" type="video/mp4"/></video>'
            if record.slide_type == 'googledrivevideo':
                #content_url = record.external_url + '/preview'
                content_url = 'https://drive.google.com/file/d/' + record.external_url + '/preview'
                record.embed_code ='<div class="drivehidecontrols"></div><iframe id="googleDriveVideo' + str(record.id) + '" class="external_video" src="' + content_url + '" oncontextmenu="return false" onload="disableContext()"></iframe>'
                #content_url = 'https://drive.google.com/uc?export=download&id=' + record.external_url
                #record.embed_code = '<video class="external_video" controls controlsList="nodownload"><source src="' + content_url + '" type="video/mp4"/></video>'
                #https://drive.google.com/file/d/1oOIeTJwf4CWTRmcOONtTigfGDQpCMHPe
            if record.slide_type == 'clapprvideo':
                content_url = record.external_url
                record.embed_code = content_url
            if record.slide_type == 'vimeovideo':
                vimeo_parse = self.parse_video_url(record.external_url)
                content_url = 'https://player.vimeo.com/video/' + vimeo_parse[1]
                record.embed_code = '<iframe class="vimeoVideo" src="' + content_url + '"></iframe>'
            if record.slide_type == 'zoom_meeting':
                #content_url = 'https://zoom.us/wc/' + record.zoom_meeting_ID + '/start?prefer=1&un=' + str(base64.b64encode(record.zoom_meeting_name.strip().encode("utf-8")), "utf-8")
                content_url = 'https://zoom.us/wc/join/' + record.zoom_meeting_ID
                #record.embed_code ='<iframe id="zoom_meeting_' + str(record.id) + '" class="external_video" src="' + content_url + '" sandbox="allow-forms allow-scripts allow-same-origin" allow="microphone; camera; fullscreen" style="border:0; height:100%; left:0; position:absolute; top:0; width:100%;"></iframe>'
                #record.embed_code = '<iframe id="zoom_meeting_' + str(record.id) + '" class="external_video" src="' + content_url + '" allow="microphone https://zoom.us; camera https://zoom.us; fullscreen https://zoom.us" style="border:0; height:100%; left:0; position:absolute; top:0; width:100%;"></iframe>'
                record.embed_code = '<div class="hidecontrols"></div><iframe allow="microphone; camera; fullscreen" id="zoom_meeting_' + str(record.id) + '" class="external_video" src="' + content_url + '" frameborder="0" wmode="transparent" oncontextmenu="return false"></iframe>'
            if record.slide_type == 'localvideo':
                vals = {
                    "video/mp4": b'MPEG-4',
                    "video/webm": b'libVorbis',
                    "video/ogg": b'Ogg'
                }
                data = base64.b64decode(record.datas)

                for key, value in vals.items():
                    if data.find(value) != -1:
                        record.mime_type = key

                content_url = 'data:' + record.mime_type + ';base64,' + record.datas.decode("utf-8")
                record.embed_code = '<video class="local_video" controls controlsList="nodownload"><source src="' + content_url + '" type="' + record.mime_type + '"/></video>'

    def parse_video_url(self, url):
        url_obj = urls.url_parse(url)
        if url_obj.ascii_host == 'vimeo.com':
            if url_obj.path:
                response = requests.get("https://vimeo.com/api/oembed.json?url=" + url)
            else:
                response = False
            return ('vimeo', url_obj.path[1:] if url_obj.path else False, response)
        #elif url_obj.ascii_host in ('youtube.com', 'www.youtube.com', 'm.youtube.com'):
        #    v_query_value = url_obj.decode_query().get('v')
        #    if v_query_value:
        #        return ('youtube', v_query_value)
        #    split_path = url_obj.path.split('/')
        #    if len(split_path) >= 3 and split_path[1] in ('v', 'embed'):
        #        return ('youtube', split_path[2])

    @api.onchange('slide_type', 'external_url')
    def onchange_slide_type(self):
        for record in self:
            if record.slide_type == 'vimeovideo' and record.external_url:
                parse_url = self.parse_video_url(record.external_url)
                if parse_url[2]:
                    jsonResponse = parse_url[2].json()
                    #jsonResponse = json.loads(parse_url[2].text)
                    if 'duration' in jsonResponse:
                        record.completion_time = jsonResponse['duration']/3600
                    else:
                        record.completion_time = 0
                    if 'title' in jsonResponse:
                        record.name = jsonResponse['title']
                    else:
                        record.name = 'Video with security restrictions (embed in this domain for example). Verify in your vimeo account or contact with video owner.'
                    if 'description' in jsonResponse:
                        record.description = jsonResponse['description']
                    else:
                        record.description = 'Video with security restrictions (embed in this domain for example). Verify in your vimeo account or contact with video owner.'
                    if 'thumbnail_url' in jsonResponse:
                        record.image_1920 = base64.b64encode(requests.get(jsonResponse['thumbnail_url']).content)
                    else:
                        record.image_1920 = False

    @api.onchange('datas')
    def _on_change_datas(self):
        res = super(Slide, self)._on_change_datas()
        vals = {
            "video/mp4": b'MPEG-4',
            "video/webm": b'libVorbis',
            "video/ogg": b'Ogg'
        }
        if self.datas:
            data = base64.b64decode(self.datas)

            for key, value in vals.items():
                if data.find(value) != -1:
                    self.mime_type = key
            if self.slide_type == 'localvideo':
                if self.mime_type not in ["video/mp4", "video/webm", "video/ogg"]:
                    self.datas = False
                    #self.mime_type = False
                    return {
                        'warning': {
                            'title': 'Warning!',
                            'message': 'The media file format is not supported. Please upload only mp4, ogg or webm files.'
                        }
                    }
        return res
