# -*- coding: utf-8 -*-
{
    'name': "Estado de Cuenta CONSTRUNORTE",

    'summary': """
        Facturas VS Pagos (detalle)""",

    'description': """
        Facturas, pagos y detalle de productos entregados.
    """,

    'author': "Rolando Estrada Martínez",
    'website': "https://staffinformatico.com.mx",
    'license": "LGPL-3',    
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'wizards/edocta_wiz.xml',
        'reports/edocta_rep.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #    'demo/demo.xml',
    # ],
}
