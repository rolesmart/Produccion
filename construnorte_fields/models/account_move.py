# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    term_vta_id = fields.Integer('Términos de Venta', compute="_term_vta_id", readonly=True)

    @api.depends('invoice_origin')    
    def _term_vta_id(self):
        for rec in self:
            id_venta=0
            pedido=''
            pedido = rec.invoice_origin
            venta = env['sale.order'].search([('name','=',pedido)])
            if venta:
                for busca in venta:
                    if busca.payment_term_id.id > 0:
                        id_venta = busca.payment_term_id.id
            rec['term_vta_id'] = id_venta