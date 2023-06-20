# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # m2m_field = fields.Many2many('hr.department')
    # comma_separated_field = fields.Char('Comma Separated Field')
    categoria = fields.Char(string='Categoría Cliente', translate=True, compute='_categoria', store=True, readonly=True)


    # @api.depends('category_id')
    def _categoria(self):
        for rec in self:
            strcat = ', '.join(rec.category_id.mapped('name')) if rec.category_id else False
            rec['categoria'] = strcat