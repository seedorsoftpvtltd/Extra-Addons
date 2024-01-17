from odoo import http, _
from odoo.http import request
from odoo.addons.web.controllers.main import Home, Session
from datetime import datetime
import json
import requests
from user_agents import parse
from odoo.addons.web.controllers.main import ensure_db
import logging
_logger = logging.getLogger(__name__)


def getting_ip(row):
    """This function calls the api and return the response"""
    url = f"https://freegeoip.app/json/{row}"       # getting records from getting ip address
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }
    response = requests.request("GET", url, headers=headers)
    respond = json.loads(response.text)
    print(respond, '-------------------- from getting_ip --------------------')
    return respond

class user_login(Home):

    @http.route()
    def web_login(self, redirect=None, **kw):
        print(request.session.sid, '----------------request.session.sid--------------[web_login]')
        print(request.session, '----------------request.session--------------[web_login]')
        print(request, '----------------request--------------[web_login]')
        print(request.uid, '--------------------------request.uid---------------------------[web_login]')
        print(request.session.uid, '------------------------request.session.uid--------------------[web_login]')
        ensure_db()
        response = super(user_login, self).web_login(redirect, **kw)
        if request.params['login_success']:
            
            try:
                ip = ''
                if 'HTTP_X_REAL_IP' in request.httprequest.environ.keys():
                    ip = request.httprequest.environ['HTTP_X_REAL_IP']
                value = getting_ip(ip)
                _logger.info('\nIP : %s\n' % (ip))
                # value = json.loads(loc_res.text)
                country = value['country_name'] or ''
                city = value['city'] or ''
                state = value['region_name'] or ''
            except:
                country = ''
                state = ''
                city = ''
            uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
            if not request.env['res.users'].sudo().browse(uid).has_group('base.group_portal'):
                user_agent = parse(request.httprequest.environ.get('HTTP_USER_AGENT', ''))
                device = user_agent.device.family
                if user_agent.device.family == 'Other':
                    if user_agent.is_pc:
                        device = 'PC'
                    elif user_agent.is_mobile:
                        device = 'Mobile'
                    elif user_agent.is_tablet:
                        device = 'Tablet'
                    
                request.env['login.log'].sudo().create({
                    'login_date':datetime.now(),
                    'user_id':uid,
                    'user_agent':user_agent,
                    'state':'active',
                    'ip':ip,
                    'browser':user_agent.browser.family,
                    # 'session_id':request.session.sid,
                    'device':device,
                    'os':user_agent.os.family,
                    'country':country,
                    'loc_state':state,
                    'city':city
                })
        return response

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        print(request.session.sid, '----------------request.session.sid--------------[web_client]')
        print(request.session, '----------------request.session--------------[web_client]')
        print(request, '----------------request--------------[web_client]')
        print(request.uid, '--------------------------request.uid---------------------------[web_client]')
        print(request.session.uid,'------------------------request.session.uid--------------------[web_client]')
        response = super(user_login, self).web_client(s_action, **kw)
        login_log = request.env['login.log'].sudo().search([('user_id','=',request.uid),('session_id','=',False)], order='id desc',limit=1)
        if login_log:
            login_log.session_id = request.session.sid
        return response

class user_logout(Session):

    @http.route('/web/session/logout', type='http', auth="none")
    def logout(self, redirect='/web'):
        print(request.session.sid, '----------------request.session.sid--------------[logout]')
        print(request.session, '----------------request.session--------------[logout]')
        print(request, '----------------request--------------[logout]')
        print(request.uid, '--------------------------request.uid---------------------------[logout]')
        print(request.session.uid,'----------------------request.session.uid----------[logout]')
        uid = request.session['uid']
        login_log = request.env['login.log'].sudo().search([('user_id', '=', uid),('session_id', '=',request.session.sid)],limit=1)
        login_log.write({
            'state':'close',
            'logout_date':datetime.now(),
        })
        
        return super(user_logout, self).logout(redirect)

