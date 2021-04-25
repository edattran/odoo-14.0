from odoo import api, fields, models
import requests
import time


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def send_quotation(self):
        url = '/customapi/newOrder'
        line = self.env['purchase.order.line'].browse(self.id)
        start_game = self.env['bgame.start'].search([('player_status', '=', 'active')])
        myobj = {'id': self.name,
                 'reqQty': line.product_qty,
                 'greatProtein': {
                     'productName': line.name,
                     'start': {
                         'id': start_game.player_extern_id
                     }
                 }}
        reply = requests.post(start_game.spring_url + url, json=myobj)
        for order in self:
            order.write({'state': 'sent'})
        print(reply)


    def receive_order(self):
        self.button_confirm()
        print('fuck')
        return True


    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True
