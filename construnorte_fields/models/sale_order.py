# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    precio_promedio = fields.Float('Precio promedio', compute="_precio_promedio", readonly=True, store=True)
    
    @api.depends('product_uom_qty','price_total')
    def _precio_promedio(self):
        for rec in self:
            if rec.product_uom_qty is None or rec.product_uom_qty == 0:
                precio_promedio = ( rec.price_total / 1.0 )
            else: 
                precio_promedio = ( rec.price_total / rec.product_uom_qty )
            rec.precio_promedio = precio_promedio

class SaleOrder(models.Model):
    _inherit = "sale.order"
    ciudad = fields.Char("Ciudad", related='partner_id.city', readonly=True, store=True)
