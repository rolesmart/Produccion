# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleReport(models.Model):
    _inherit = "sale.report"

    precio_promedio = fields.Float('Precio promedio', readonly=True, group_operator="avg")
    ciudad = fields.Char(string='Ciudad', readonly=True)
    p_producto_30 = fields.Float('p_producto_30', readonly=True, group_operator="avg")
    p_producto_60 = fields.Float('p_producto_60', readonly=True, group_operator="avg")
    p_producto_90 = fields.Float('p_producto_90', readonly=True, group_operator="avg")
    p_producto_cty_30 = fields.Float('p_producto_cty_30', readonly=True, group_operator="avg")
    p_producto_cty_60 = fields.Float('p_producto_cty_60', readonly=True, group_operator="avg")
    p_producto_cty_90 = fields.Float('p_producto_cty_90', readonly=True, group_operator="avg")
    p_producto_ven_30 = fields.Float('p_producto_ven_30', readonly=True, group_operator="avg")
    p_producto_ven_60 = fields.Float('p_producto_ven_60', readonly=True, group_operator="avg")
    p_producto_ven_90  = fields.Float('p_producto_ven_90 ', readonly=True, group_operator="avg")

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['precio_promedio'] = "l.precio_promedio"
        res['ciudad'] = "s.ciudad"
        res['p_producto_30'] = "sol01.p_producto_30"
        res['p_producto_60'] = "sol01.p_producto_60"
        res['p_producto_90'] = "sol01.p_producto_90"
        res['p_producto_cty_30'] = "sol02.p_producto_cty_30"
        res['p_producto_cty_60'] = "sol02.p_producto_cty_60"
        res['p_producto_cty_90'] = "sol02.p_producto_cty_90"
        res['p_producto_ven_30'] = "sol03.p_producto_ven_30"
        res['p_producto_ven_60'] = "sol03.p_producto_ven_60"
        res['p_producto_ven_90'] = "sol03.p_producto_ven_90"
        return res


    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """, l.precio_promedio, s.ciudad, sol01.p_producto_30, sol01.p_producto_60, sol01.p_producto_90, sol02.p_producto_cty_30, sol02.p_producto_cty_60, \
        sol02.p_producto_cty_90, sol03.p_producto_ven_30, sol03.p_producto_ven_60, sol03.p_producto_ven_90"""
        return res


    def _from_sale(self):
        res = super()._from_sale()
        res += ' inner join (select  product_id, \
        ( sum(case when so1.date_order > current_date -30 then price_total end) / sum(case when so1.date_order > current_date -30 then qty_invoiced end) \
        ) as p_producto_30, \
        ( sum(case when so1.date_order > current_date -60 then price_total end) / sum(case when so1.date_order > current_date -60 then qty_invoiced end) \
        ) as p_producto_60, \
        ( sum(case when so1.date_order > current_date -90 then price_total end) / sum(case when so1.date_order > current_date -90 then qty_invoiced end) \
        ) as p_producto_90	\
        from sale_order_line sol1 left join sale_order so1 on so1.id =sol1.order_id where sol1.invoice_status = \'invoiced\' and sol1.qty_invoiced > 0 \
        and sol1.company_id = 1 group by product_id) as sol01 on sol01.product_id=l.product_id '

        res += ' inner join (select  product_id, so1.ciudad,  \
         ( sum(case when so1.date_order > current_date -30 then price_total end) / sum(case when so1.date_order > current_date -30 then qty_invoiced end) \
         ) as p_producto_cty_30, \
         ( sum(case when so1.date_order > current_date -60 then price_total end) / sum(case when so1.date_order > current_date -60 then qty_invoiced end) \
         ) as p_producto_cty_60, \
         ( sum(case when so1.date_order > current_date -90 then price_total end) / sum(case when so1.date_order > current_date -90 then qty_invoiced end) \
         ) as p_producto_cty_90	\
         from sale_order_line sol1 left join sale_order so1 on so1.id =sol1.order_id where sol1.invoice_status = \'invoiced\' and sol1.qty_invoiced > 0 \
         and sol1.company_id = 1 group by product_id, so1.ciudad) as sol02 on sol02.product_id=l.product_id and sol02.ciudad  = s.ciudad '

        res += 'inner join (select  product_id, so1.user_id ,  \
         ( sum(case when so1.date_order > current_date -30 then price_total end) / sum(case when so1.date_order > current_date -30 then qty_invoiced end) \
         ) as p_producto_ven_30, \
         ( sum(case when so1.date_order > current_date -60 then price_total end) / sum(case when so1.date_order > current_date -60 then qty_invoiced end) \
         ) as p_producto_ven_60, \
         ( sum(case when so1.date_order > current_date -90 then price_total end) / sum(case when so1.date_order > current_date -90 then qty_invoiced end) \
         ) as p_producto_ven_90	\
         from sale_order_line sol1 left join sale_order so1 on so1.id =sol1.order_id where sol1.invoice_status = \'invoiced\' and sol1.qty_invoiced > 0 \
         and sol1.company_id = 1 group by product_id, so1.user_id) as sol03 on sol03.product_id=l.product_id and sol03.user_id  = s.user_id '

        return res
