from odoo import api, fields, models
from odoo.exceptions import UserError
import requests
import time


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def send_quotation(self):
        suplier_name = self.partner_id.name
        vname = ''
        if suplier_name == "Great Protein":
            vname = 'greatProtein'
        elif suplier_name == "Super Sweet":
            vname = 'superSweet'
        url = '/customapi/' + vname + '/newOrder'
        line = self.env['purchase.order.line'].browse(self.id)
        start_game = self.env['bgame.start'].search([('player_status', '=', 'active')])
        myobj = {'id': self.name,
                 'reqQty': line.product_qty,
                 vname: {
                     'productName': line.name,
                     'start': {
                         'id': start_game.player_extern_id
                     }
                 }}
        reply = requests.post(start_game.spring_url + url, json=myobj)
        for order in self:
            order.write({'state': 'sent'})
        print(reply)

    def notify(self):
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

    def button_cancel(self):
        for order in self:
            for inv in order.invoice_ids:
                if inv and inv.state not in ('cancel', 'draft'):
                    raise UserError(
                        _("Unable to cancel this purchase order. You must first cancel the related vendor bills."))

        self.write({'state': 'cancel'})
        return True
