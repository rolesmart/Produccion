# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    term_vta = fields.Char(string='Términos de Venta', compute="_term_vta", readonly=True)

    @api.depends('invoice_origin','move_type')    
    def _term_vta(self):
        for rec in self:
            id_venta=''
            pedido=''
            if rec.move_type == 'out_invoice':
                pedido = rec.invoice_origin
                venta = self.env['sale.order'].search([('name','=',pedido)])
                if venta:
                    for busca in venta:
                        if busca.payment_term_id.name != '':
                            id_venta = busca.payment_term_id.name
            
            rec['term_vta'] = id_venta
