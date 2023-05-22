# -*- coding: utf-8 -*-
import datetime

import werkzeug

from odoo import models, fields, api
from odoo.exceptions import UserError
import pytz


class VisitGps(models.Model):
    _name = 'visit.gps'
    _description = 'Registro de visitas al cliente obteniendo su Geoloclaización'

    #name = fields.Char()
    fecha_visita = fields.Datetime(string="Fecha", default=fields.Datetime.now, readonly=True)
    partner_id = fields.Many2one(string='Cliente', comodel_name='res.partner', ondelete='cascade', required=True)
    survey_id = fields.Many2one(string='Encuesta', comodel_name='survey.survey', required=True, ondelete='cascade')
    pedido = fields.Selection([('Sí', 'Sí'), ('No', 'No')], string="Realizó pedido", required=True)
    survey_start_url = fields.Char(string='Encuesta', compute="_survey_start_url")
    # latitud = fields.Float(digits="Location", readonly=True)
    # longitud = fields.Float(digits="Location", readonly=True)
    latitud = fields.Float(required=True, digits=(3,8))
    longitud = fields.Float(required=True, digits=(3,8))

    state = fields.Selection(selection=[
        ('draft', 'Borrador'),
        ('done', 'Procesado'),
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='draft')

    def button_in_done(self):
        self.write({
            'state': "done"
        })
        partner_id = self.partner_id
        if partner_id and self.state == 'done':
            fila = self.env['res.partner'].search([('id', '=', partner_id.id)])
            if fila:
                for busca in fila:
                    msg1 = 'Visita al cliente, se obtuvo Pedido? ' + str(self.pedido)
                    busca.message_post(body=msg1)

            calendar_event = self.env['calendar.event'].create({
                'name': 'Visita: ' + partner_id.name,
                'start': datetime.datetime.now(),
                'stop': datetime.datetime.now() + datetime.timedelta(hours=2),
                'res_model_id': self.env['ir.model']._get_id('res.partner'),
                'res_id': self.id,
                'partner_ids': [(4, partner_id.id), (4, self.env.user.partner_id.id)],
            })


    def write(self, vals):
        if any(state == 'done' for state in set(self.mapped('state'))):
            raise UserError("Registro Procesado, no esta permitido efectuar modificaciones")
        else:
            return super().write(vals)

    @api.ondelete(at_uninstall=False)
    def _draft(self):
        for visit_gps in self:
            if visit_gps.state not in ('draft'):
                raise UserError(
                    "Registro Procesado, no se puede eliminar")

    @api.depends('survey_id.access_token')
    def _survey_start_url(self):
        for record in self:
            record.survey_start_url = werkzeug.urls.url_join(record.survey_id.get_base_url(),
                                                             record.survey_id.get_start_url()) + '?encuestado=' + str(
                record.partner_id.id) if record.survey_id else False
