# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseReport(models.Model):

    _inherit = "purchase.report"

    precio_promedio = fields.Float('Precio promedio', readonly=True, group_operator="avg")

    def _select(self):
        select_str = super(PurchaseReport, self)._select()
        return select_str + ", l.precio_promedio as precio_promedio"

    def _group_by(self):
        group_by_str = super(PurchaseReport, self)._group_by()
        return group_by_str + ", l.precio_promedio"
