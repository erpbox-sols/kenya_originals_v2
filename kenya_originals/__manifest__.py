# -*- coding: utf-8 -*-
{
    'name': 'Kenya Originals',
    'summary': """Kenya Originals""",
    'description': 'Kenya Originals',

    'author': 'Arpit Goel',
    'website': 'https://www.erpbox-solutions.com/',
    "support": "goelarpit1997@gmail.com",

    'category': 'Contact',
    'version': '14.0.0.1.1',
    'depends': ['base', 'contacts', 'sale_management', 'stock', 'mrp', 'purchase', 'account_asset', 'hr'],

    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/hr_employee.xml',
        'views/account_move.xml',
        'views/account_tax.xml',
        'views/account_asset.xml',
        'views/stock_picking.xml',
        'views/region_area.xml',
        'views/mrp_views.xml',
        'reports/sale_report_template.xml',
        'reports/report_deliveryslip.xml',
        'reports/invoice_report_template.xml',
        'data/ir_sequence.xml',
        'data/decimal_precision_data.xml',
    ],

    'license': "LGPL-3",

    "auto_install": False,
    "installable": True,
}