from odoo import api, fields, models
from odoo.exceptions import UserError
import requests
import time


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Function to send quotation over rest
    def send_quotation(self):
        suplier_name = self.partner_id.name
        vname = ''
        # Rename vendor for rest url
        if suplier_name == "Great Protein":
            vname = 'greatProtein'
        elif suplier_name == "Super Sweet":
            vname = 'superSweet'
        elif suplier_name == "Choco Loco":
            vname = 'chocoLoco'
        elif suplier_name == "Healthy Nutrition":
            vname = 'healthyNutrition'
        else:
            # Notification for the player if vendor is false
            self.env.user.notify_danger(message='Check Vendor!')
            return True
        # Send over rest
        url = '/customapi/' + vname + '/newOrder'
        line = self.env['purchase.order.line'].browse(self.id)
        start_game = self.env['bgame.start'].search([('player_status', '=', 'active')])
        myobj = {'name': self.name,
                 'reqQty': line.product_qty,
                 'reqPrice': self.amount_total,
                 vname: {
                     'productName': line.name,
                     'start': {
                         'id': start_game.player_extern_id
                     }
                 }}
        requests.post(start_game.spring_url + url, json=myobj)
        # Set status to sent
        for order in self:
            order.write({'state': 'sent'})

    # Inherited function from purchase.sy
    # Status check changed
    def button_confirm(self):
        for order in self:
            # Status check changed from the default - 'draft' deleted
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

    # Inherited function from purchase.py
    # Return True added
    def button_cancel(self):
        for order in self:
            for inv in order.invoice_ids:
                if inv and inv.state not in ('cancel', 'draft'):
                    raise UserError(
                        _("Unable to cancel this purchase order. You must first cancel the related vendor bills."))

        self.write({'state': 'cancel'})
        return True
