
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

    'depends': ['base','product'],

    'data': [
        'security/ir.model.access.csv',

        'views/up_menu.xml',
        'views/up_apartment_view.xml',
        'views/up_product_view.xml',
        'views/up_type_utility_view.xml',
        'wizard/up_generate_period_wizard_view.xml',
        'views/up_period_view.xml',

        'views/up_charge_view.xml',
        'views/up_payment_view.xml',

        'data/up_type_utility_data.xml',

        'report/up_custom_external_template.xml',
        'report/up_payment_report.xml',
    ],

    'demo': [
        'demo/up_period_demo.xml',
        'demo/up_product_demo.xml',
        'demo/up_apartment_demo.xml',
        'demo/up_apartment_utility_demo.xml',
        'demo/up_charge_demo.xml',
    ],

    'installable': True,
    'images': ['static/description/icon.png'],

    'assets': {
        'web.report_assets_common': [
            'utility_payments/static/src/**/*.scss',
        ],
    },
}
