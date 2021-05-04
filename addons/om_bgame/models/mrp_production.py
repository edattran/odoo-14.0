from odoo import api, fields, models
from odoo.exceptions import UserError
import requests
import time


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    bgame_status = fields.Char(string='Status')

    def production_confirm(self):
        start_game = self.env['bgame.start'].search([('player_status', '=', 'active')])
        url = '/customapi/manufacturer/newMaOrder'
        products = self.env['stock.move.line'].search_count([('reference', '=', self.name)])
        if products < 3:
            self.env.user.notify_danger(message='Check product availability!')
            return True
        stock = self.env['stock.move.line'].search([('reference', '=', self.name)])
        object_int1 = int(stock[0].product_id)
        product1_name = self.env['product.template'].search([('id', '=', object_int1)])
        pqty1 = stock[0].product_qty
        object_int2 = int(stock[1].product_id)
        product2_name = self.env['product.template'].search([('id', '=', object_int2)])
        pqty2 = stock[1].product_qty
        object_int3 = int(stock[2].product_id)
        product3_name = self.env['product.template'].search([('id', '=', object_int3)])
        pqty3 = stock[2].product_qty
        if products == 3:
            myobj = {'name': self.name,
                     'product1': product1_name.name,
                     'qtyP1': pqty1,
                     'product2': product2_name.name,
                     'qtyP2': pqty2,
                     'product3': product3_name.name,
                     'qtyP3': pqty3,
                     'manufacturer': {
                         'start': {
                             'id': start_game.player_extern_id
                         }
                     }
                     }
            reply = requests.post(start_game.spring_url + url, json=myobj)
        else:
            self.env.user.notify_warning(message='Check Products!')
        return True

    def set_progress(self):
        self.write({'state': 'progress'})
        return True

    def set_done(self):
        vals = {
            'bgame_status': 'True'
        }
        self.write(vals)
        self.button_mark_done()
        return True

    def button_mark_done(self):
        if self.bgame_status == 'True':
            stock = self.env['stock.move.line'].search([('reference', '=', self.name)])
            vals = {
                'qty_done': stock[0].product_uom_qty
            }
            for s in stock:
                s.write(vals)
            vals2 = {
                'qty_producing': self.product_qty
            }
            self.write(vals2)
            self._button_mark_done_sanity_checks()

            if not self.env.context.get('button_mark_done_production_ids'):
                self = self.with_context(button_mark_done_production_ids=self.ids)
            res = self._pre_button_mark_done()
            if res is not True:
                return res

            if self.env.context.get('mo_ids_to_backorder'):
                productions_to_backorder = self.browse(self.env.context['mo_ids_to_backorder'])
                productions_not_to_backorder = self - productions_to_backorder
            else:
                productions_not_to_backorder = self
                productions_to_backorder = self.env['mrp.production']

            self.workorder_ids.button_finish()

            productions_not_to_backorder._post_inventory(cancel_backorder=True)
            productions_to_backorder._post_inventory(cancel_backorder=False)
            backorders = productions_to_backorder._generate_backorder_productions()

            # if completed products make other confirmed/partially_available moves available, assign them
            done_move_finished_ids = (
                    productions_to_backorder.move_finished_ids | productions_not_to_backorder.move_finished_ids).filtered(
                lambda m: m.state == 'done')
            done_move_finished_ids._trigger_assign()

            # Moves without quantity done are not posted => set them as done instead of canceling. In
            # case the user edits the MO later on and sets some consumed quantity on those, we do not
            # want the move lines to be canceled.
            (productions_not_to_backorder.move_raw_ids | productions_not_to_backorder.move_finished_ids).filtered(
                lambda x: x.state not in ('done', 'cancel')).write({
                'state': 'done',
                'product_uom_qty': 0.0,
            })

            for production in self:
                production.write({
                    'date_finished': fields.Datetime.now(),
                    'product_qty': production.qty_produced,
                    'priority': '0',
                    'is_locked': True,
                })

            for workorder in self.workorder_ids.filtered(lambda w: w.state not in ('done', 'cancel')):
                workorder.duration_expected = workorder._get_duration_expected()

            if not backorders:
                if self.env.context.get('from_workorder'):
                    return {
                        'type': 'ir.actions.act_window',
                        'res_model': 'mrp.production',
                        'views': [[self.env.ref('mrp.mrp_production_form_view').id, 'form']],
                        'res_id': self.id,
                        'target': 'main',
                    }
                return True
            context = self.env.context.copy()
            context = {k: v for k, v in context.items() if not k.startswith('default_')}
            for k, v in context.items():
                if k.startswith('skip_'):
                    context[k] = False
            action = {
                'res_model': 'mrp.production',
                'type': 'ir.actions.act_window',
                'context': dict(context, mo_ids_to_backorder=None)
            }
            if len(backorders) == 1:
                action.update({
                    'view_mode': 'form',
                    'res_id': backorders[0].id,
                })
            else:
                action.update({
                    'name': _("Backorder MO"),
                    'domain': [('id', 'in', backorders.ids)],
                    'view_mode': 'tree,form',
                })
            return action
