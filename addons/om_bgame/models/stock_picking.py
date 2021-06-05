from odoo import api, fields, models
from odoo.exceptions import UserError
import requests


class PickingType(models.Model):
    _inherit = 'stock.picking'

    # Function to send and receive over rest
    def send_delivery(self):
        # Set quantity to done
        line = self.env['stock.move.line'].search([('picking_id', '=', self.id)])
        vals = {
            'qty_done': line.product_uom_qty
        }
        line.write(vals)
        req_qty = self.env['stock.move'].search([('picking_id', '=', self.id)])
        # Check if quantity requested and done are the same
        if line.qty_done == req_qty.product_qty:
            _name = self.partner_id.name
            cname = ''
            # Rename vendor name for rest url
            if _name == "Protein Store":
                cname = 'proteinStore'
            elif _name == "Power Store":
                cname = 'powerStore'
            elif _name == "Nature Store":
                cname = 'natureStore'
            elif _name == "Vegan Store":
                cname = 'veganStore'
            elif _name == 'Super Sweet':
                cname = 'superSweet'
            elif _name == 'Great Protein':
                cname = 'greatProtein'
            elif _name == 'Choco Loco':
                cname = 'chocoLoco'
            elif _name == 'Healthy Nutrition':
                cname = 'healthyNutrition'
            # Send over rest
            url = '/customapi/' + cname + '/deliver'
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
            requests.post(start_game.spring_url + url, json=myobj)
            return True
        # Notification for the player if the quantities are not the same
        else:
            str = "% s" % req_qty.product_qty
            self.env.user.notify_danger(message="You promised " + str + " !")
            return True
