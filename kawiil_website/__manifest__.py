{
    'name': 'Kawiil Website',
    'summary': "K'awiil Motors website: theme settings, header, footer, menu, logo and home page.",
    'license': 'OPL-1',
    'category': 'Kawiil/Kawiil',
    'author': 'Odoo, Inc.',
    'website': 'https://github.com/odoo-trainings/kawiil-base/',
    'version': '1.0.0',
    'depends': ['website_sale', 'website_crm', 'kawiil_base'],
    'data': [
        'views/website_templates.xml',
        'views/homepage_templates.xml',
        'views/bike_page_templates.xml',
        'views/financing_page_templates.xml',
        'views/about_page_templates.xml',
        'views/test_ride_page_templates.xml',
        'data/res_config_settings_data.xml',
        'data/product_template_data.xml',
        'data/website_data.xml',
        'data/website_menu_data.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'kawiil_website/static/src/scss/primary_variables.scss',
        ],
        'web.assets_frontend': [
            'kawiil_website/static/src/scss/typography.scss',
        ],
    },
}
