from odoo import api, fields, models
from odoo.exceptions import UserError
import requests


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    def action_create_payments(self):
        _name = self.partner_id.name
        cname = ''
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
        url = '/customapi/' + cname + '/payment'

        start_game = self.env['bgame.start'].search([('player_status', '=', 'active')])
        order = self.env['account.move'].search([('name', '=', self.communication)])
        print(order.invoice_origin)
        myobj = {'name': order.invoice_origin,
                 cname: {
                     'start': {
                         'id': start_game.player_extern_id
                     }
                 }
                 }
        reply = requests.post(start_game.spring_url + url, json=myobj)
        print(reply)
        payments = self._create_payments()

        if self._context.get('dont_redirect_to_payments'):
            return True

        action = {
            'name': _('Payments'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'context': {'create': False},
        }
        if len(payments) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': payments.id,
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', payments.ids)],
            })
        return action
