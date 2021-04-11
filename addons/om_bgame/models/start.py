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
    player_status = fields.Char(string="Game Status")

    def start_game(self):
        url = 'http://localhost:8070/customapi/startGame'
        myobj = {'playerName': self.player_name,
                 'databaseName': self.database_name,
                 'playerMail': self.player_mail,
                 'playerPassword': self.player_password,
                 }
        reply = requests.post(url, json=myobj)
        print(reply)
