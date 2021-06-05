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

    # Function to start the game
    def start_game(self):
        status = self.player_status
        # Checks if the player status is active
        if status == "active":
            self.env.user.notify_warning(message='Game is already running!')
            return True
        # Checks if the player status is finished
        if status == "finished":
            self.env.user.notify_warning(message='Game already finished, please create a new DB!')
            return True
        # If status is not finished or active, products, vendors etc. will be created and the game started
        # Creates the product aspartame
        product1 = self.env['product.product'].create({'name': 'Aspartame',
                                                       'type': 'product',
                                                       'list_price': '1',
                                                       'sale_ok': 'false',
                                                       'purchase_ok': 'true'
                                                       })
        # Product_tmpl_id needed to assign the product to the vendor
        product1_tmpl_int = int(product1.product_tmpl_id)
        # Product ID needed to create bom
        product1_id_int = int(product1.id)
        # Creates the vendor Super Sweet
        vendor1 = self.env['res.partner'].create({'name': 'Super Sweet',
                                                  'display_name': 'Super Sweet'})
        # Vendor ID needed to assign the product to the vendor
        vendor1_int = int(vendor1.id)
        # Assign aspartame to the vendor Super Sweet
        self.env['product.supplierinfo'].create({'name': vendor1_int,
                                                 'price': '10.00',
                                                 'product_tmpl_id': product1_tmpl_int})

        # Creates the product whey isolate
        product2 = self.env['product.product'].create({'name': 'Whey Isolate',
                                                       'type': 'product',
                                                       'list_price': '1',
                                                       'sale_ok': 'false',
                                                       'purchase_ok': 'true'
                                                       })
        # Product_tmpl_id needed to assign the product to the vendor
        product2_tmpl_int = int(product2.product_tmpl_id)
        # Product ID needed to create bom
        product2_id_int = int(product2.id)
        # Creates the vendor Great Protein
        vendor2 = self.env['res.partner'].create({'name': 'Great Protein',
                                                  'display_name': 'Great Protein'})
        # Vendor ID needed to assign the product to the vendor
        vendor2_int = int(vendor2.id)
        # Assign whey isolate to the vendor Great Protein
        self.env['product.supplierinfo'].create({'name': vendor2_int,
                                                 'price': '13.00',
                                                 'product_tmpl_id': product2_tmpl_int})

        # Creates the product cacao powder
        product3 = self.env['product.product'].create({'name': 'Cacao Powder',
                                                       'type': 'product',
                                                       'list_price': '1',
                                                       'sale_ok': 'false',
                                                       'purchase_ok': 'true'
                                                       })
        # Product_tmpl_id needed to assign the product to the vendor
        product3_tmpl_int = int(product3.product_tmpl_id)
        # Product ID needed to create bom
        product3_id_int = int(product3.id)
        # Creates the vendor Choco Loco
        vendor3 = self.env['res.partner'].create({'name': 'Choco Loco',
                                                  'display_name': 'Choco Loco'})
        # Vendor ID needed to assign the product to the vendor
        vendor3_int = int(vendor3.id)
        # Assign cacao powder to the vendor Choco Loco
        self.env['product.supplierinfo'].create({'name': vendor3_int,
                                                 'price': '40.00',
                                                 'product_tmpl_id': product3_tmpl_int})

        # Creates the product pea protein isolate
        product4 = self.env['product.product'].create({'name': 'Pea Protein Isolate',
                                                       'type': 'product',
                                                       'list_price': '1',
                                                       'sale_ok': 'false',
                                                       'purchase_ok': 'true'
                                                       })
        # Product_tmpl_id needed to assign the product to the vendor
        product4_tmpl_int = int(product4.product_tmpl_id)
        # Product ID needed to create bom
        product4_id_int = int(product4.id)
        # Creates the vendor Healthy Nutrition
        vendor4 = self.env['res.partner'].create({'name': 'Healthy Nutrition',
                                                  'display_name': 'Healthy Nutrition'})
        # Vendor ID needed to assign the product to the vendor
        vendor4_int = int(vendor4.id)
        # Assign pea protein isolate to the vendor Healthy Nutrition
        self.env['product.supplierinfo'].create({'name': vendor4_int,
                                                 'price': '50.00',
                                                 'product_tmpl_id': product4_tmpl_int})

        # Creates the bom whey bars
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

        # Creates the bom vegan bars
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

        # Creates all four customers
        self.env['res.partner'].create({'name': 'Protein Store',
                                        'display_name': 'Protein Store'})
        self.env['res.partner'].create({'name': 'Power Store',
                                        'display_name': 'Power Store'})
        self.env['res.partner'].create({'name': 'Nature Store',
                                        'display_name': 'Nature Store'})
        self.env['res.partner'].create({'name': 'Vegan Store',
                                        'display_name': 'Vegan Store'})
        # Starts the game over rest
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

