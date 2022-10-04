# -*- coding: utf-8 -*-
{
    'name': "partner_edocta",

    'summary': """
        Estado de cuenta (CONSTRUNORTE)""",

    'description': """
        Facturas con pagos aplicados y pagos sin aplicar + Productos incluidos 
    """,

    'author': "Staff  Informático y Sistemas Computacionales, S.A. de C.V.",
    'website': "https://staffinformatico.com.mx",
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    "license": "AGPL-3",
    "depends": ["account", "report_xlsx", "report_xlsx_helper"],
    
    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "security/edocta_security.xml",        
        'reports/cn.xml',
        'wizard/partner_edocta.xml',
    ],
    "installable": True,
    "application": False,
}
