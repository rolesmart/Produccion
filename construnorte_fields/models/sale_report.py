from odoo import models, fields, api


class SaleReport(models.Model):
    _inherit = "sale.report"

    precio_promedio = fields.Float('Precio promedio', readonly=True, group_operator="avg")
    ciudad = fields.Char(string='Ciudad', readonly=True)	

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['precio_promedio','ciudad',] = ", l.precio_promedio as precio_promedio, s.ciudad as ciudad"
        groupby += ', l.precio_promedio, s.ciudad'
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
