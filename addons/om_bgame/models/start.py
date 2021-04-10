from odoo import api, fields, models
import requests


class BgameStart(models.Model):
    _name = 'bgame.start'
    _description = 'Business Game Start Record'

    player_name = fields.Char(string='Name', required=True)

    def get_rest(self):
        response = requests.get("http://localhost:8070/api/users")
        print(response.text)
