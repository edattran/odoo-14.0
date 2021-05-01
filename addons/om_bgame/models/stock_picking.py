from odoo import api, fields, models
from odoo.exceptions import UserError
import requests


class PickingType(models.Model):
    _inherit = 'stock.picking'

    def send_delivery(self):
        customer_name = self.partner_id.name
        cname = ''
        if customer_name == "Protein Store":
            cname = 'proteinStore'
        elif customer_name == "Power Store":
            cname = 'powerStore'
        elif customer_name == "Nature Store":
            cname = 'natureStore'
        url = '/customapi/' + cname + '/deliver'
        line = self.env['stock.move.line'].search([('picking_id', '=', self.id)])
        start_game = self.env['bgame.start'].search([('player_status', '=', 'active')])
        product_name = self.env['sale.order'].search([('name', '=', self.origin)])
        myobj = {'name': self.origin,
                 'delQty': line.product_uom_qty,
                 cname: {
                     'productName': product_name.name,
                     'start': {
                         'id': start_game.player_extern_id
                     }
                 }}
        reply = requests.post(start_game.spring_url + url, json=myobj)
        print(reply)
        return True