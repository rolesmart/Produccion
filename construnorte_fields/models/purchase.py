# -*- coding: utf-8 -*-

from odoo import api, fields, models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    precio_promedio = fields.Float('Precio promedio', compute="_precio_promedio", readonly=True, store=True)
	
    def _precio_promedio(self):
        for rec in self:
            if rec.product_uom_qty > 0:
                precio_promedio = ( rec.price_total / rec.product_uom_qty )
            else: 
                precio_promedio = 0
            rec.precio_promedio = precio_promedio	