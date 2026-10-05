{
    'name': "HR Hospital ( Lesson 2.2 )",

    'summary': 'Odoo Scholl Lesson 2.2 - Hr Hospital',

    'description': 'Odoo Scholl Lesson 2.2 - Hr Hospital',

    'author': "Volodymyr",
    'website': "https://odoo.school/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'license': 'OPL-1',
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/odoo_hospital_menu.xml',
        'views/odoo_hospital_doctor_views.xml',
        'views/odoo_hospital_patient_views.xml',
        'views/odoo_hospital_type_disease_views.xml',
        'views/odoo_hospital_appointment_views.xml',

        'data/osl_type_disease_data.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/osl_doctor_demo.xml',
        'demo/osl_patient_demo.xml',

    ],

    'installable': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ]
}