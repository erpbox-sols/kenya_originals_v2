{
    "name": "Auto Generate Lot Number in Manufacturing WorkOrder",
    "version": "14.0.02.11.2020",
    "category": "Manufacturing",
    "summary": """
	Auto generate Lot no in Manufacturing Workorder when we have PLAN Manufacturing Order.Lot no generate based on production Date/Today Date.
	""",
    "author": 'Vraja Technologies',
    'price': 30,
    'currency': 'EUR',
    "depends": ['mrp','stock','mrp_workorder'],
    "data": [
        'wizard/res_config.xml',
    ],
    'qweb': [],
    'css': [],
    'js': [],
    'images': [
        'static/description/auto_generate_mo.jpg',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'OPL-1',
}
