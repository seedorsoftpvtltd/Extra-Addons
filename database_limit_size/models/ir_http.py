# Copyright 2020 Eugene Molotov <https://it-projects.info/team/em230418>
# License MIT (https://opensource.org/licenses/MIT).

import os
from odoo import models, fields, api, _
from odoo import models
from odoo.tools import human_size
import requests
import math
import datetime
# https://stackoverflow.com/a/1392549
def get_directory_size(start_path):
    total_size = 0
    for dirpath, _dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size



class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        res = super(IrHttp, self).session_info()

        Config = self.env["ir.config_parameter"].sudo()
        try:
            database_limit_size = int(Config.get_param("database_limit_size", 0))
            filestore_limit_size = int(Config.get_param("filestore_limit_size", 0))
            int(Config.set_param("filestore_usage", 0))
            int(Config.set_param("database_usage", 0))
            int(Config.set_param("filestore_per", 0))
            int(Config.set_param("database_per", 0))

        except ValueError:
            return res

        if not database_limit_size:
            return res

        self.env.cr.execute("select pg_database_size(%s)", [self.env.cr.dbname])
        database_size = self.env.cr.fetchone()[0]
        filestore_size = get_directory_size(self.env["ir.attachment"]._filestore())
        total_size = database_size

        filestore_size = filestore_size

        # self.env['ir.config_parameter'].sudo().set_param('filestoree_usage',0)
        # self.env['ir.config_parameter'].sudo().set_param('databasee_usage', 0)


        if total_size > database_limit_size and filestore_size > filestore_limit_size:

            res["database_block_message"] = "Database size and Filestore size exceed"
            # self.env['ir.config_parameter'].sudo().set_param('database_usage', total_size)
            # self.env['ir.config_parameter'].sudo().set_param('filestore_usage', filestore_size)
            # self.env['ir.config_parameter'].sudo().set_param('filestore_per', 100)
            # self.env['ir.config_parameter'].sudo().set_param('database_per', 100)
        elif total_size > database_limit_size:

            res["database_block_message"] = "Database size exceed ({} / {})".format(
                human_size(total_size), human_size(database_limit_size),
            )
            # self.env['ir.config_parameter'].sudo().set_param('database_usage', total_size)
            # self.env['ir.config_parameter'].sudo().set_param('database_per', 100)
        elif filestore_size > filestore_limit_size:

            res["database_block_message"] = "Filestore size exceed ({} / {})".format(
                human_size(filestore_size), human_size(filestore_limit_size),
            )
            # self.env['ir.config_parameter'].sudo().set_param('filestore_usage', total_size)
            # self.env['ir.config_parameter'].sudo().set_param('filestore_per', 100)
        elif total_size > database_limit_size * 0.9 and filestore_size > filestore_limit_size * 0.9:

            res["database_block_message"] = (
                    "Database size and Filestore size is about to be exceed"

            )
            res["database_block_is_warning"] = True
            # self.env['ir.config_parameter'].sudo().set_param('database_usage', total_size)
            # self.env['ir.config_parameter'].sudo().set_param('filestore_usage', filestore_size)
            # limit_file = math.floor((filestore_size / filestore_limit_size) * 100)
            # limit_db = math.floor((total_size / database_limit_size) * 100)
            # self.env['ir.config_parameter'].sudo().set_param('filestore_per',limit_file)
            # self.env['ir.config_parameter'].sudo().set_param('database_per',limit_db)
            # self.limitation_api()
        elif filestore_size > filestore_limit_size * 0.9:

            res["database_block_message"] = (
                    "Filestore size is about to be exceed (%s / %s)"
                    % (human_size(filestore_size), human_size(filestore_limit_size))
            )
            res["database_block_is_warning"] = True
            # self.env['ir.config_parameter'].sudo().set_param('filestore_usage', total_size)
            # limit_file = math.floor((filestore_size / filestore_limit_size) * 100)
            # self.env['ir.config_parameter'].sudo().set_param('filestore_per',limit_file)
            # self.limitation_api()
        elif total_size > database_limit_size * 0.9:

            res["database_block_message"] = (
                    "Database size is about to be exceed (%s / %s)"
                    % (human_size(total_size), human_size(database_limit_size))
            )
            res["database_block_is_warning"] = True
            # self.env['ir.config_parameter'].sudo().set_param('database_usage',total_size)
            # limit_db = math.floor((total_size / database_limit_size) * 100)
            # self.env['ir.config_parameter'].sudo().set_param('database_per',limit_db)

        elif total_size > database_limit_size * 0.5 and filestore_size > filestore_limit_size * 0.5:

            res["database_block_message"] = (
                    "Database size and Filestore size is about to be exceed"

            )
            res["database_block_is_warning"] = True
            # self.env['ir.config_parameter'].sudo().set_param('database_usage', total_size)
            # self.env['ir.config_parameter'].sudo().set_param('filestore_usage', filestore_size)
            # limit_file=math.floor((filestore_size/filestore_limit_size)*100)
            # limit_db= math.floor((total_size/database_limit_size)*100)
            # self.env['ir.config_parameter'].sudo().set_param('filestore_per',limit_file)
            # self.env['ir.config_parameter'].sudo().set_param('database_per',limit_db )
            # self.limitation_api()
        elif filestore_size > filestore_limit_size * 0.5:

            res["database_block_message"] = (
                    "Filestore size is about to be exceed (%s / %s)"
                    % (human_size(filestore_size), human_size(filestore_limit_size))
            )
            res["database_block_is_warning"] = True
            # self.env['ir.config_parameter'].sudo().set_param('filestore_usage', total_size)
            # limit_file=math.floor((filestore_size / filestore_limit_size) * 100)
            # self.env['ir.config_parameter'].sudo().set_param('filestore_per',limit_file)
            # self.limitation_api()
        elif total_size > database_limit_size * 0.5:

            res["database_block_message"] = (
                    "Database size is about to be exceed (%s / %s)"
                    % (human_size(total_size), human_size(database_limit_size))
            )
            res["database_block_is_warning"] = True
            # self.env['ir.config_parameter'].sudo().set_param('database_usage', total_size)
            # limit_db=math.floor((total_size/database_limit_size)*100)
            #
            # self.env['ir.config_parameter'].sudo().set_param('database_per',limit_db)
            # self.limitation_api()
        limit_file = math.floor((filestore_size / filestore_limit_size) * 100)
        limit_db = math.floor((total_size / database_limit_size) * 100)
        self.env['ir.config_parameter'].sudo().set_param('filestore_per', limit_file)
        self.env['ir.config_parameter'].sudo().set_param('database_per', limit_db)
        self.env['ir.config_parameter'].sudo().set_param('database_usage', total_size)
        self.env['ir.config_parameter'].sudo().set_param('filestore_usage', filestore_size)
        self.limitation_api(limit_file,limit_db)




        return res

    def limitation_api(self, limit_file,limit_db ):
        if limit_file >50 or limit_db >50:
            API_ENDPOINT = "http://eiuat.seedors.com:8290/seedor-api/limit-management"
            date=datetime.datetime.now().strftime('%Y-%m-%d')

            # your API key here


            # your source code here

            data = {
            "clientid":self.env.cr.dbname,
            "filestore_usage":self.env['ir.config_parameter'].sudo().get_param('filestore_per'),
            "database_usage":self.env['ir.config_parameter'].sudo().get_param('database_per'),
            "filestore_limit_size": self.env['ir.config_parameter'].sudo().get_param('filestore_limit_size'),
            "database_limit_size": self.env['ir.config_parameter'].sudo().get_param('database_limit_size'),
            "datetime":date
                    }

            # sending post request and saving response as response object
            r = requests.post(url=API_ENDPOINT, data=data)
            if requests.status_codes == 200:
                requestss = r.text

            return True
