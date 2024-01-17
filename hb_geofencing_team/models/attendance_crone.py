from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta


class AttendStatus(models.AbstractModel):
    _inherit = "hr.attendance"

    def action_attend_status(self, ):
        for res_user_id in self.env['res.users'].search([]):
            print(res_user_id, res_user_id.name)
            partner_list = []
            if res_user_id.has_group('hb_geofencing_team.group_attend_status'):
                print(res_user_id, res_user_id.name, 'groupppppp')
                partner_list.append(res_user_id.partner_id.id)
                td_date = datetime.now()
                atend_ids = self.search([('check_in', 'like', td_date.strftime("%m-%d"))])
                records = []
                print(records)
                for attend in atend_ids:
                    attend_list = {}
                    if str(attend.checkin_status).__contains__('Failed') or str(attend.checkout_status).__contains__(
                            'Failed'):
                        attend_list['emp_name'] = attend.employee_id.name
                        attend_list['emp_checkin_status'] = attend.checkin_status
                        attend_list['emp_checkout_status'] = attend.checkout_status
                        records.append(attend_list)
                print(records)
                # res_user_id = self.env.user
                html = """
                                            <html>
                                            <div style="margin: 0px; padding: 0px;">
                                                        <p style="margin: 0px; padding: 0px; font-size: 14px;">
                                                            Hello ,
                                                            <br/>
                                                            Today's	Attendance Status Details
                                                            </p>
                                                            <br/>
                                            <table border="1" style="font-size: 14px;">
                                            <tr>
                                            <th style="font-size: 14px;">Employee Name</th>
                                            <th style="font-size: 14px;">Check In Status</th>
                                            <th style="font-size: 14px;">Check Out Status</th>
                                            </tr>



                                        """
                vals = []
                for rec in records:
                    print(rec['emp_name'], "recccccccccccccccccccccccccccccc")

                    html += "<tr><td>{}</td>".format(rec['emp_name'])
                    html += "<td>{}</td>".format(rec['emp_checkin_status'])
                    html += "<td>{}</td>".format(rec['emp_checkout_status'])
                    vals = {
                        'subject': "Employee Attandance Report",
                        'email_to': res_user_id.partner_id.email,
                        'author_id': res_user_id.partner_id.id,
                        'body_html': html,
                    }

                print(vals)
                print(html)
                print(res_user_id)
                mail_id = res_user_id.env['mail.mail'].create(vals)
                print(mail_id)
                if mail_id:
                    mail_id.send(res_user_id.id)

        return True


