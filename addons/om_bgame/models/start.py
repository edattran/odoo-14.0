from odoo import api, fields, models
import requests
import json


class BgameStart(models.Model):
    _name = 'bgame.start'
    _description = 'Business Game Start Record'

    player_name = fields.Char(string='Nick Name', required=True)
    database_name = fields.Char(string='DB Name', required=True)
    player_mail = fields.Char(string='Mail Address', required=True)
    player_password = fields.Char(string='Password', required=True)
    spring_url = fields.Char(string='URL Spring Applikation', required=True)
    odoo_url = fields.Char(string='URL Odoo Instanz', required=True)
    player_status = fields.Char(string="Game Status")
    player_extern_id = fields.Char(string="External ID")

    def start_game(self):
        status = self.player_status
        if status == "active":
            self.env.user.notify_warning(message='Game is already running!')
            return True
        if status == "finished":
            self.env.user.notify_warning(message='Game already finished, please create a new DB!')
            return True
        product1 = self.env['product.product'].create({'name': 'Aspartame',
                                                       'type': 'product',
                                                       'list_price': '1',
                                                       'sale_ok': 'false',
                                                       'purchase_ok': 'true'
                                                       })
        product1_tmpl_int = int(product1.product_tmpl_id)
        product1_id_int = int(product1.id)
        vendor1 = self.env['res.partner'].create({'name': 'Super Sweet',
                                                  'display_name': 'Super Sweet'})
        vendor1_int = int(vendor1.id)
        self.env['product.supplierinfo'].create({'name': vendor1_int,
                                                 'price': '10.00',
                                                 'product_tmpl_id': product1_tmpl_int})

        product2 = self.env['product.product'].create({'name': 'Whey Isolate',
                                                       'type': 'product',
                                                       'list_price': '1',
                                                       'sale_ok': 'false',
                                                       'purchase_ok': 'true'
                                                       })
        product2_tmpl_int = int(product2.product_tmpl_id)
        product2_id_int = int(product2.id)
        vendor2 = self.env['res.partner'].create({'name': 'Great Protein',
                                                  'display_name': 'Great Protein'})
        vendor2_int = int(vendor2.id)
        self.env['product.supplierinfo'].create({'name': vendor2_int,
                                                 'price': '13.00',
                                                 'product_tmpl_id': product2_tmpl_int})

        product3 = self.env['product.product'].create({'name': 'Cacao Powder',
                                                       'type': 'product',
                                                       'list_price': '1',
                                                       'sale_ok': 'false',
                                                       'purchase_ok': 'true'
                                                       })
        product3_tmpl_int = int(product3.product_tmpl_id)
        product3_id_int = int(product3.id)
        vendor3 = self.env['res.partner'].create({'name': 'Choco Loco',
                                                  'display_name': 'Choco Loco'})
        vendor3_int = int(vendor3.id)
        self.env['product.supplierinfo'].create({'name': vendor3_int,
                                                 'price': '40.00',
                                                 'product_tmpl_id': product3_tmpl_int})

        product4 = self.env['product.product'].create({'name': 'Pea Protein Isolate',
                                                       'type': 'product',
                                                       'list_price': '1',
                                                       'sale_ok': 'false',
                                                       'purchase_ok': 'true'
                                                       })
        product4_tmpl_int = int(product4.product_tmpl_id)
        product4_id_int = int(product4.id)
        vendor4 = self.env['res.partner'].create({'name': 'Healthy Nutrition',
                                                  'display_name': 'Healthy Nutrition'})
        vendor4_int = int(vendor4.id)
        self.env['product.supplierinfo'].create({'name': vendor4_int,
                                                 'price': '50.00',
                                                 'product_tmpl_id': product4_tmpl_int})

        pbom1 = self.env['product.product'].create({'name': 'Whey Bars',
                                                    'type': 'product',
                                                    'list_price': '3',
                                                    'sale_ok': 'true',
                                                    'purchase_ok': 'false'})
        pbom1_tmpl_int = int(pbom1.product_tmpl_id)
        bom1 = self.env['mrp.bom'].create({'product_qty': '46',
                                           'product_tmpl_id': pbom1_tmpl_int})
        self.env['mrp.bom.line'].create({'product_id': product1_id_int,
                                         'product_qty': '1',
                                         'bom_id': bom1.id})
        self.env['mrp.bom.line'].create({'product_id': product2_id_int,
                                         'product_qty': '1',
                                         'bom_id': bom1.id})
        self.env['mrp.bom.line'].create({'product_id': product3_id_int,
                                         'product_qty': '1',
                                         'bom_id': bom1.id})

        pbom2 = self.env['product.product'].create({'name': 'Vegan Bars',
                                                    'type': 'product',
                                                    'list_price': '5',
                                                    'sale_ok': 'true',
                                                    'purchase_ok': 'false'})
        pbom2_tmpl_int = int(pbom2.product_tmpl_id)
        bom2 = self.env['mrp.bom'].create({'product_qty': '46',
                                           'product_tmpl_id': pbom2_tmpl_int})
        self.env['mrp.bom.line'].create({'product_id': product1_id_int,
                                         'product_qty': '1',
                                         'bom_id': bom2.id})
        self.env['mrp.bom.line'].create({'product_id': product4_id_int,
                                         'product_qty': '1',
                                         'bom_id': bom2.id})
        self.env['mrp.bom.line'].create({'product_id': product3_id_int,
                                         'product_qty': '1',
                                         'bom_id': bom2.id})

        customer1 = self.env['res.partner'].create({'name': 'Protein Store',
                                                    'display_name': 'Protein Store'})
        customer2 = self.env['res.partner'].create({'name': 'Power Store',
                                                    'display_name': 'Power Store'})
        customer3 = self.env['res.partner'].create({'name': 'Nature Store',
                                                    'display_name': 'Nature Store'})
        customer4 = self.env['res.partner'].create({'name': 'Vegan Store',
                                                    'display_name': 'Vegan Store'})
        url = '/customapi/startGame'
        myobj = {'playerName': self.player_name,
                 'databaseName': self.database_name,
                 'playerMail': self.player_mail,
                 'playerPassword': self.player_password,
                 'springUrl': self.spring_url,
                 'odooUrl': self.odoo_url,
                 'externalId': self.id,
                 }
        requests.post(self.spring_url + url, json=myobj)

