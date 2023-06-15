# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    industry_id = fields.Many2one('res.partner.industry', 'Sector', readonly=True)
    x_studio_municipio = fields.Many2one(comodel_name='x_mx_municipio', string='Municipio', readonly=True)
    categoria = fields.Char(string='Categoría Cliente', translate=True, readonly=True)

    def _select(self):
        return super()._select() + ", partner.industry_id, partner.x_studio_municipio, rpc.name as categoria"

    def _from(self):
        return super()._from() + \
            "    left join res_partner_res_partner_category_rel rprpcr on rprpcr.partner_id = partner.id \
                 left join res_partner_category rpc on rpc.id = rprpcr.category_id"
