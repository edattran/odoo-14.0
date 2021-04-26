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
        url = '/customapi/startGame'
        myobj = {'playerName': self.player_name,
                 'databaseName': self.database_name,
                 'playerMail': self.player_mail,
                 'playerPassword': self.player_password,
                 'springUrl': self.spring_url,
                 'odooUrl': self.odoo_url,
                 'externalId': self.id,
                 }
        reply = requests.post(self.spring_url + url, json=myobj)
        print(reply)

    def test(self):
        user = self.env['res.partner'].search([('name', '=', 'Administrator')])
        self.env.user.notify_success(message='This is a Test Message')


