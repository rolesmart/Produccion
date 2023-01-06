from odoo import models, fields, api


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

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['precio_promedio','ciudad','p_producto_30','p_producto_60','p_producto_90','p_producto_cty_30','p_producto_cty_60','p_producto_cty_90', \
               'p_producto_ven_30','p_producto_ven_60','p_producto_ven_90',] = ", l.precio_promedio as precio_promedio, s.ciudad as ciudad, \
               sol01.p_producto_30 as p_producto_30, sol01.p_producto_60 as p_producto_60, sol01.p_producto_90 as p_producto_90, \
               sol02.p_producto_cty_30 as p_producto_cty_30, sol02.p_producto_cty_60 as p_producto_cty_60, sol02.p_producto_cty_90 as p_producto_cty_90, \
               sol03.p_producto_ven_30 as p_producto_ven_30, sol03.p_producto_ven_60 as p_producto_ven_60, sol03.p_producto_ven_90 as p_producto_ven_90"
        
        groupby += ', l.precio_promedio, s.ciudad, sol01.p_producto_30, sol01.p_producto_60, sol01.p_producto_90, sol02.p_producto_cty_30, sol02.p_producto_cty_60, \
        sol02.p_producto_cty_90, sol03.p_producto_ven_30, sol03.p_producto_ven_60, sol03.p_producto_ven_90'
        
        from_clause +=' inner join (select  product_id, \
        ( sum(case when so1.date_order > current_date -30 then price_total end) / sum(case when so1.date_order > current_date -30 then qty_invoiced end) \
        ) as p_producto_30, \
        ( sum(case when so1.date_order > current_date -60 then price_total end) / sum(case when so1.date_order > current_date -60 then qty_invoiced end) \
        ) as p_producto_60, \
        ( sum(case when so1.date_order > current_date -90 then price_total end) / sum(case when so1.date_order > current_date -90 then qty_invoiced end) \
        ) as p_producto_90	\
        from sale_order_line sol1 left join sale_order so1 on so1.id =sol1.order_id where sol1.invoice_status = \'invoiced\' and sol1.qty_invoiced > 0 \
        and sol1.company_id = 1 group by product_id) as sol01 on sol01.product_id=l.product_id '
        
        from_clause += ' inner join (select  product_id, so1.ciudad,  \
        ( sum(case when so1.date_order > current_date -30 then price_total end) / sum(case when so1.date_order > current_date -30 then qty_invoiced end) \
        ) as p_producto_cty_30, \
        ( sum(case when so1.date_order > current_date -60 then price_total end) / sum(case when so1.date_order > current_date -60 then qty_invoiced end) \
        ) as p_producto_cty_60, \
        ( sum(case when so1.date_order > current_date -90 then price_total end) / sum(case when so1.date_order > current_date -90 then qty_invoiced end) \
        ) as p_producto_cty_90	\
        from sale_order_line sol1 left join sale_order so1 on so1.id =sol1.order_id where sol1.invoice_status = \'invoiced\' and sol1.qty_invoiced > 0 \
        and sol1.company_id = 1 group by product_id, so1.ciudad) as sol02 on sol02.product_id=l.product_id and sol02.ciudad  = s.ciudad '
        
        from_clause += 'inner join (select  product_id, so1.user_id ,  \
        ( sum(case when so1.date_order > current_date -30 then price_total end) / sum(case when so1.date_order > current_date -30 then qty_invoiced end) \
        ) as p_producto_ven_30, \
        ( sum(case when so1.date_order > current_date -60 then price_total end) / sum(case when so1.date_order > current_date -60 then qty_invoiced end) \
        ) as p_producto_ven_60, \
        ( sum(case when so1.date_order > current_date -90 then price_total end) / sum(case when so1.date_order > current_date -90 then qty_invoiced end) \
        ) as p_producto_ven_90	\
        from sale_order_line sol1 left join sale_order so1 on so1.id =sol1.order_id where sol1.invoice_status = \'invoiced\' and sol1.qty_invoiced > 0 \
        and sol1.company_id = 1 group by product_id, so1.user_id) as sol03 on sol03.product_id=l.product_id and sol03.user_id  = s.user_id '
        
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
