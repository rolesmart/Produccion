# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


import json
import logging

_logger = logging.getLogger(__name__)

class EdoctaReportWizard(models.TransientModel):
    _name = 'edocta.report.wizard'

    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)
    #date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)

    @api.model
    def _get_date_start(self):
        return (
            fields.Date.context_today(self).replace(day=1) - relativedelta(days=1)
        ).replace(day=1)

    date_start = fields.Date(required=True, default=_get_date_start, string='Fecha de inicio: ')

    # @api.multi
    def button_export_pdf(self):
        """Call when button 'button_export_pdf' clicked.
        """

        data = {
            'ids': self.ids,
            'model': self._name,
            'date_start': self.date_start,
            'partner_ids': self._context['active_ids']
        }

        # use `module_name.report_id` as reference.
        # `report_action()` will call `_get_report_values()` and pass `data` automatically.
        return self.env.ref('partner_edocta.edocta_report').report_action(self, data=data)


class ReportEdocta(models.AbstractModel):
    """Abstract Model for report template.

    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = 'report.partner_edocta.edocta_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        # date_start = data['form']['date_start']
        # date_end = data['form']['date_end']
        # date_start_obj = datetime.strptime(date_start, DATE_FORMAT)
        # date_end_obj = datetime.strptime(date_end, DATE_FORMAT)
        # date_diff = (date_end_obj - date_start_obj).days + 1
        # data['date_start'] = date_start
        if not docids:
            docids = data['partner_ids']

        company_id = self.env.company.id
        docs = []
        facturas = self.env['account.move'].search([('partner_id', 'in', docids), ('move_type', '=', 'out_invoice'),
                                                    ('state', '=', 'posted'), ('company_id','=', company_id)], order='id')
        facturas_list = []
        partidas_list = []
        tot_pago1 = 0
        for move in facturas:
            # trae los pagos aplicados a la factura
            if move.invoice_payments_widget:
                reconciled_payments_widget_vals = move.invoice_payments_widget
            else:
                reconciled_payments_widget_vals = False
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


        #return {
        #    'doc_ids': data['ids'],
        #    'doc_model': data['model'],
        #    'date_start': date_start,
        #    'date_end': date_end,
        #    'docs': docs,
        #}
