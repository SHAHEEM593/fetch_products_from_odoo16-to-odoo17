# -*- coding: utf-8 -*-
{
    'name': "Fetch Product",
    'version': '17.0.1.0.0',
    'depends': ['base','sale_management'],
    'author': "Shaheem",
    'category': 'category',
    'description': """
    Fetch Product
    """,
    'summary': 'Fetch Product',
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'wizard/fetch_product_odoo_view.xml',
        'views/sales_menu.xml',
    ],

    'application': True,
    'installable': True,

}
