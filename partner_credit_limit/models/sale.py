# See LICENSE file for full copyright and licensing details.


from odoo import _, api, models
from odoo.exceptions import UserError

#import logging
#_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def check_limit(self):
        self.ensure_one()
        partner = self.partner_id
        user_id = self.env['res.users'].search([
            ('partner_id', '=', partner.id)], limit=1)
        if user_id and not user_id.has_group('base.group_portal') or not \
                user_id:
            moveline_obj = self.env['account.move.line']
            #modificado por staff 27/09/22 ver original
            movelines = moveline_obj.search(
                [('partner_id', '=', partner.id),
                 ('account_id.user_type_id.name', 'in',
                    ['Receivable', 'Por cobrar']),                 
                 ('parent_state','!=','cancel')]                
            )
            confirm_sale_order = self.search(
                [('partner_id', '=', partner.id),
                 ('state', '=', 'sale'),
                 ('invoice_status', '!=', 'invoiced')])
            debit, credit = 0.0, 0.0
            amount_total = 0.0
            for status in confirm_sale_order:
                amount_total += status.amount_total
            for line in movelines:
                credit += line.credit
                debit += line.debit
                #_logger.info('Movimientos %s  %s     %s      %s \n', line.account_id.user_type_id, line.account_id.user_type_id.name, line.credit, line.debit)
            partner_credit_limit = (
                debit + amount_total) - credit
            available_credit_limit = round(
                partner.credit_limit - partner_credit_limit, 2)
            #_logger.info('available_credit_limit %s \n', available_credit_limit )
            if partner_credit_limit > partner.credit_limit and \
                    partner.credit_limit > 0.0:
                if not partner.over_credit:
                    msg = 'Su límite de crédito disponible' \
                          ' es = %s \nCheck "%s" Límite ' \
                          'Crédito. ' % (available_credit_limit,
                                       self.partner_id.name )
                    raise UserError(_('Imposible confirmar la venta '
                                      ' \n' + msg))
            return True

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.check_limit()
        return res

    @api.constrains('amount_total')
    def check_amount(self):
        for order in self:
            order.check_limit()

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        if res.partner_id.credit_limit > 0.0 and \
                not res.partner_id.over_credit:
            res.check_limit()
        return res
