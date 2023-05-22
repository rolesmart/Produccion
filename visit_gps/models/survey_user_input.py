# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, fields, models
from odoo.tools import plaintext2html


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    partner_svy_id = fields.Many2one('res.partner', string='Entrevistado', readonly=True)
