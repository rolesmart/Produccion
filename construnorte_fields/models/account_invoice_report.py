# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    industry_id = fields.Many2one('res.partner.industry', 'Sector', readonly=True)
    x_studio_municipio = fields.Many2one(comodel_name='x_mx_municipio', string='Municipio', readonly=True)
    categoria = fields.Char(string='Categoría Cliente', translate=True, readonly=True)

    def _select(self):
        return super()._select() + ", partner.industry_id, partner.x_studio_municipio, partner.categoria"

