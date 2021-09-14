# Copyright 2020 Teclea Limited
{
    'name': 'Stock Total Cost Plus Landed Cost',
    'description': """Slight changes within calculation of valuation lines to allow 
    overwrite some line values if necessary. Requested by Alpharama.
    """,
    'version': '14.0.1.0.1',
    "author": "Teclea Limited",
    'license': 'AGPL-3',
    'category': 'Stock',
    'website': 'Teclea Limited',
	'depends': ['stock_landed_costs'],
    'data': [
        'views/views.xml',
    ],

    'installable': True,
	'auto_install': False,
}
