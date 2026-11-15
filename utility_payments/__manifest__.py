
{
    'name': "Utility Payments",
    'sequence': -16,
    'summary': "Module for personal tracking of utility payments",

    'description': """
Allows for the recording of utility charges and payments made for utility services
    """,

    'author': "Volodymyr A.",
    'website': "https://www.i.have.no.site.com",

    'license': 'OPL-1',
    'category': 'Services',
    'version': '19.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/up_menu.xml',
        'views/up_apartment_view.xml',
        'views/up_product_view.xml',
        'views/up_type_utility_view.xml',
        'wizard/up_generate_period_wizard_view.xml',
        'views/up_period_view.xml',
        'views/up_charge_view.xml',

        'data/up_type_utility_data.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/up_product_demo.xml',
        'demo/up_apartment_demo.xml',
        'demo/up_apartment_utility_demo.xml'
    ],

    'installable': True,
    'images': ['static/description/icon.png'],
}
