# -*- coding: utf-8 -*-
from odoo import fields, models
import xmlrpc.client

from odoo.http import request
from odoo import exceptions, _


class FetchProduct(models.TransientModel):
    """ wizard model"""
    _name = 'fetch.product'
    local_host = fields.Char(required=True, string="Local Host",help="http://10.0.20.174:8016")
    database1 = fields.Char(required=True, string="DataBase Name")
    database2 = fields.Char(string="DataBase Name", default=lambda x: x.env.cr.dbname)
    user_name1 = fields.Char(string="User Name", required=True)
    user_name2 = fields.Char(string="User Name", required=True)
    password1 = fields.Char(string="Password", required=True)
    password2 = fields.Char(string="Password", required=True)

    def fetch_product(self):
        """to fetch product from odoo16 DB to odoo17 DB"""
        print(request.httprequest.host_url)
        url_str = request.httprequest.host_url
        db17 = url_str[:len(url_str) - 1]

        url_db1 = self.local_host
        db_1 = self.database1
        username_db_1 = self.user_name1
        password_db_1 = self.password1
        common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1))
        models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1))
        version_db1 = common_1.version()
        uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})

        url_db2 = db17
        db_2 = self.database2
        username_db_2 = self.user_name2
        password_db_2 = self.password2
        common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db2))
        models_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2))
        version_db2 = common_2.version()
        uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
        uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})
        db_1_leads = models_1.execute_kw(db_1, uid_db1, password_db_1, 'product.template', 'search_read', [],
                                         {'fields': ['name', 'list_price', 'standard_price', 'image_1920', 'taxes_id',
                                                     ]})
        for rec in db_1_leads:
            models_2.execute_kw(db_2, uid_db1, password_db_2, 'product.template',
                                'create',
                                [{'name': rec['name'],
                                  'list_price': rec['list_price'],
                                  'standard_price': rec['standard_price'],
                                  'image_1920': rec['image_1920'],
                                  'taxes_id': rec['taxes_id'],
                                  }])
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Refresh Page...',
                'type': 'rainbow_man',
            }
        }
