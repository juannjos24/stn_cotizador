# -*- coding: utf-8 -*-
{
    'name': "Stn Cotizador de Seguro",

    'summary': "Modulo encargado para realizar una cotizacion de seguro, dependiendo del ",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/car_brand.xml',
        'views/car_year.xml',
        'views/car_model.xml', 
        'views/car_version.xml',    
        'views/crm_lead_views.xml',
        'views/form_website.xml',
        'views/website_lead_thank_you.xml',   
        'views/menu_items.xml',        
        'views/templates.xml',
    
    ],
    'assets': {
        'web.assets_frontend': [            
            'stn_cotizador/static/src/js/controller_form.js',
            
        ], 
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

