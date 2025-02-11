{
    'name': 'Kawiil Base',
    'summary': 'This module adds the configurations required for the Kawiil Motors training exercise production database.',
    'license': 'OPL-1',
    'category': 'Kawiil/Kawiil',
    'author': 'Odoo, Inc.',
    'website': 'https://github.com/odoo-trainings/kawiil-base/',
    'version': '18.0.1.0.0',
    'depends': ['sale_management', 'website', 'mrp', 'contacts'],
    'data': [
        'data/product_data.xml',
        'data/partner_data.xml',
        'data/sale_data.xml',
    ],
    'demo': [
    ],
} 