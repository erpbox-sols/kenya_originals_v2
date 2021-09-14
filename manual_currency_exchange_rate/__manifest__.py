# -*- coding: utf-8 -*-

{
    'name': "Manual Currency Exchange rate",
    'version': "1.2",
    'summary': "This module will provide you the facility to enter exchange currency rate at the time of sales order, invoice order, purchase order and payments",
    'category': 'Accounting Management',
    'description': """
    manual currency exchange rate
      
    """,
    'author': "Teclea Limited",
    'website':"",
    'depends': ['base', 'sale_management', 'purchase', 'stock', 'account'],
    'data': [
        'views/inherited_invoice_payment.xml',
        'views/inherited_invoice.xml',
        'views/inherited_purchase_order.xml',
        'views/inherited_sale_order.xml'
    ],
    'demo': [],
    "external_dependencies": {},
    'installable': True,
    'auto_install': False,
    "price": 30,

}
