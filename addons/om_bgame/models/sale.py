from odoo import api, fields, models
from odoo.exceptions import UserError
import requests
import time


class PurchaseOrder(models.Model):
    _inherit = 'sale.order'

    def send_quotation(self):
        customer_name = self.partner_id.name
        cname = ''
        if customer_name == "Protein Store":
            cname = 'proteinStore'
        elif customer_name == "Power Store":
            cname = 'powerStore'
        elif customer_name == "Nature Store":
            cname = 'natureStore'
        url = '/customapi/' + cname + '/newOrder'
        line = self.env['sale.order.line'].browse(self.id)
        start_game = self.env['bgame.start'].search([('player_status', '=', 'active')])
        myobj = {'name': self.name,
                 'reqQty': line.product_uom_qty,
                 cname: {
                     'productName': line.name,
                     'start': {
                         'id': start_game.player_extern_id
                     }
                 }}
        reply = requests.post(start_game.spring_url + url, json=myobj)
        for order in self:
            order.write({'state': 'sent'})
        print(reply)
        return True

    def action_confirm(self):
        if self.state == 'sent':
            if self._get_forbidden_state_confirm() & set(self.mapped('state')):
                raise UserError(_(
                    'It is not allowed to confirm an order in the following states: %s'
                ) % (', '.join(self._get_forbidden_state_confirm())))

            for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
                order.message_subscribe([order.partner_id.id])
            self.write(self._prepare_confirmation_values())

            # Context key 'default_name' is sometimes propagated up to here.
            # We don't need it and it creates issues in the creation of linked records.
            context = self._context.copy()
            context.pop('default_name', None)

            self.with_context(context)._action_confirm()
            if self.env.user.has_group('sale.group_auto_done_setting'):
                self.action_done()
            return True
