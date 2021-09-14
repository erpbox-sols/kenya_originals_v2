{
    "name": "Auto Generate Lot Number in Incoming Shipment",
    "version": "14.0.12.01.2021",
    "category": "Purchase",
    "summary": """
	Auto generate Lot no in Incoming Shipment when we have confirm Purchase Order based on Purchase Order Date/Schedule date of Incoming Shipment/Today Date.
	""",
    "author": 'Vraja Technologies',
    'price': 41,
    'currency': 'EUR',
    "depends": ['stock','purchase'],
    "data": [
        'wizard/res_config.xml',
    ],
    'qweb': [],
    'css': [],
    'js': [],
    'images': [
        'static/description/auto_gen_po.jpg',
    ],
    # 'images': ['static/description/christmas.gif'],
    'demo': [],
    'live_test_url': 'http://www.vrajatechnologies.com/contactus',
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'OPL-1',
}
