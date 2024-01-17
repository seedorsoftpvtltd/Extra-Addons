import datetime

from odoo.addons.web.controllers.main import Session
from odoo import http
import requests
import json
from odoo.http import request
from odoo.addons.web.controllers.main import Home


class Inherit_Home(Home):
    @http.route()
    def web_login(self, redirect=None, **kw):
        res = super(Inherit_Home, self).web_login()
        if 'login' in kw:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            payload = json.dumps(
                # {"username": str(request.session.login)}
                {
                    "clientid": str(request.session.db),
                    "userid": request.session.uid,
                    "login_datetime": now,
                    "username": str(request.session.login),
                    "login_source": "SEEDOR"
                }
            )

            print(payload)
            headers = {
                'Content-Type': 'application/json'
            }
#            url = "http://eiuat.seedors.com:8290/seedor-api/login-trace"
            url = "https://miprod.seedors.com/seedor-api/login-trace"
            print(url)
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            print(response.text)
            print(response)
            print(response.status_code)
#            print("hhhhhhhhhhhhhhhhhhhbbbbbbbbbbbbbbbbbbbbbb")
        return res


class Inherit_Session(Session):
    @http.route()
    def logout(self, redirect=None, **kw):
        payload = json.dumps(
            {"username": str(request.session.login)})

        print(payload)
        headers = {
            'Content-Type': 'application/json'
        }
        url = "http://eiuat.seedors.com:8001/idm-logout"
#        url = "http://miprod.seedors.com:7010/idm-logout"

        print(url)
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        print(response.text)
        print(response)
        print(response.status_code)
#        print("hhhhhhhhhhhhhhhhhhhbbbbbbbbbbbbbbbbbbbbbb")
        return super(Inherit_Session, self).logout()

