# Copyright 2018 ForgeFlow, S.L. (http://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from datetime import date, timedelta, datetime
from json import dumps

import json
import logging

_logger = logging.getLogger(__name__)

class PartnerEdoctaWizard(models.TransientModel):
    _name = "partner.edocta"
    _description = "Estado de Cuenta"

    @api.model
    def _get_date_start(self):
        return (
            fields.Date.context_today(self).replace(day=1) - relativedelta(days=1)
        ).replace(day=1)

    date_start = fields.Date(required=True, default=_get_date_start, string='Fecha de inicio: ')

    def button_export_pdf(self):
        self.ensure_one()
        report_type = "qweb-pdf"
        data = {'date_start': self.date_start, 'partner_ids': self._context['active_ids']}
        _logger.info('prueba de staff 3 %s \n', data)        
        return self.env.ref(
            "partner_edocta.report_cn"
        ).report_action(self, data=data)


class CnReport(models.AbstractModel):
    _name = "report.partner_edocta.report_cn"

    @api.model
    def _get_report_values(self, docids, data=None):
        if not docids:
            docids = data['partner_ids']

        _logger.info('prueba de staff 2 %s \n', docids)
        company_id = self.env.company.id
        
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('partner_edocta.report_cn')
        facturas = self.env['account.move'].search([('partner_id', 'in', docids), ('move_type', '=', 'out_invoice'),
                                                    ('state', '=', 'posted'), ('company_id','=', company_id)], order='id')
        facturas_list = []
        partidas_list = []
        tot_pago1 = 0
        for move in facturas:
            # trae los pagos aplicados a la factura
            reconciled_payments_widget_vals = json.loads(move.invoice_payments_widget)
            if reconciled_payments_widget_vals:
                for vals in reconciled_payments_widget_vals['content']:
                    idpago = vals['account_payment_id']
                    numpago = self.env['account.payment'].search([('id', '=', idpago)])
                    newvals = vals
                    newvals['factura'] = move.name
                    newvals['numpago'] = numpago.name
                    facturas_list.append(newvals)
                    tot_pago1 += newvals['amount']

            # trae las partidas de la factura
            partidas = self.env['account.move.line'].search([('move_id', '=', move.id)], order='id')
            for idx0 in range(len(partidas)):
                registro={}
                registro['move_id'] = partidas[idx0]['move_id'].id
                registro['quantity'] = partidas[idx0]['quantity']
                registro['name'] = partidas[idx0]['name']
                registro['price_unit'] = partidas[idx0]['price_unit']
                registro['price_subtotal'] = partidas[idx0]['price_subtotal']
                registro['price_total'] = partidas[idx0]['price_total']
                #hay algunos registro que aunque son de IVA reportan price_tota, entonces
                if registro['name'] == 'IVA(16%) VENTAS':
                    registro['price_total'] = 0.0

                if registro['price_total'] > 0.0:
                    partidas_list.append(registro)

        # trae todos los pagos del cliente
        pagos = self.env['account.payment'].search([('partner_id', 'in', docids), ('payment_type', '=', 'inbound'),
                                                    ('state', '=', 'posted')], order='id')
        # vaciarlos en una lista
        pagos_list = []
        for idx0 in range(len(pagos)):
            registro={}
            registro['payment_date'] = pagos[idx0]['date']
            registro['name'] = pagos[idx0]['name']
            busqueda0 = pagos[idx0]['journal_id']
            registro['diario'] = busqueda0.display_name
                #pagos[idx0]['journal_id']
            registro['amount'] = pagos[idx0]['amount']
            registro['saldo'] = 0
            pagos_list.append(registro)

        # y compararlos contra los ya aplicados, buscar si hay residuos (pagos no asignados)
        total = 0
        for idx1 in range(len(pagos_list)):
            busqueda = pagos_list[idx1]['name']
            # en facturas_list se encuentran los pagos ya aplicados
            pagoasignado = 0
            for idx2 in range(len(facturas_list)):
                if busqueda == facturas_list[idx2]['numpago']:
                    pagoasignado += facturas_list[idx2]['amount']
            saldo = pagos_list[idx1]['amount'] - pagoasignado
            pagos_list[idx1]['saldo'] = saldo

        docs = self.env['account.move'].search([('partner_id', 'in', docids), ('move_type', '=', 'out_invoice'),
                                                ('state', '=', 'posted'), ('company_id','=', company_id)], order='id')

        docs_list = []
        tot_factura = 0
        saldo_inicial = 0
        for idx0 in range(len(docs)):
            registro={}
            registro['id'] = docs[idx0]['id']
            registro['invoice_date'] = docs[idx0]['invoice_date']
            registro['name'] = docs[idx0]['name']
            registro['invoice_origin'] = docs[idx0]['invoice_origin']
            registro['amount_total_signed'] = docs[idx0]['amount_total_signed']
            registro['amount_residual_signed'] = docs[idx0]['amount_residual_signed']
            #Si la fecha de inicio del rango es superior a la fecha de factura, acumula saldo_inicial
            _logger.info('data inicia %s \n', data['date_start'] )            
            if datetime.strptime(data['date_start'], "%Y-%m-%d").date() > docs[idx0]['invoice_date']:
                registro['date_start'] = 'n'
                saldo_inicial += docs[idx0]['amount_residual_signed']
            else:
                registro['date_start'] = 's'
            docs_list.append(registro)
            #acumula el monto total de las facturas emitidas
            tot_factura += docs[idx0]['amount_total_signed']

        fecha_inicial0 = datetime.strptime(data['date_start'], "%Y-%m-%d").date()
        fecha_inicial = 'Saldo al iniciar el '+ fecha_inicial0.strftime("%d/%m/%Y") + ':'

        return {
            'docs_ids': docids,
            'doc_model': 'account.move',
            'docs': docs,
            'docs_list': docs_list,
            'facturas_list': facturas_list,
            'pagos_list': pagos_list,
            'partidas_list': partidas_list,
            'tot_factura': tot_factura,
            'tot_pago1': tot_pago1,
            'saldo_inicial': saldo_inicial,
            'fecha_inicial': fecha_inicial,
        }
