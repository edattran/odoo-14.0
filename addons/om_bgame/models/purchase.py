from odoo import api, fields, models
import requests


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def send_quotation(self):
        url = '/customapi/venGreatProtein'
        line = self.env['purchase.order.line'].browse(self.id)
        start_game = self.env['bgame.start'].search([('player_status', '=', 'active')])
        myobj = {'productName': line.name,
                 'quantity': line.product_qty,
                 'start': {
                     'id': start_game.player_extern_id
                 }}
        reply = requests.post(start_game.spring_url + url, json=myobj)
        print(reply)
        for order in self:
            order.write({'state': 'sent'})

    def button_confirm(self):
        for order in self:
            if order.state not in ['sent']:
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
