# -*- coding: utf-8 -*-
{
    'name': "Registro de Visita a Cliente",

    'summary': """
        Recabar pedido e información
        Válido para CONSTRUNORTE 
     """,

    'description': """
        Al realizar la visita con el cliente para recabar pedido se obtiene:
        Si levantó pedido o no, generar vínculo de encuesta de manera opcional, 
        registro de la reunión en Calendario y Geolocalización sitio de visita
    """,

    'author': "Rolando Estrada Martínez, SIySC",
    'website': "https://www.staffinformatico.com.mx'",
    "license": "AGPL-3",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '16.1',

    # any module necessary for this one to work correctly
    'depends': ['mail', 'calendar', 'contacts', 'sale', 'survey'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/visit_gps_views.xml',
        'views/visit_gps_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'visit_gps/static/src/js/visit_gps.js',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
