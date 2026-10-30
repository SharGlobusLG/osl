{
    'name': "HR Hospital ( Lesson 4.0 )",
    'sequence': -1000000,

    'summary': 'Odoo Scholl Lesson 4.0 - Hr Hospital',

    'description': 'Odoo Scholl Lesson 4.0 - Hr Hospital',

    'author': "Volodymyr",
    'website': "https://odoo.school/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'license': 'OPL-1',
    'category': 'Human Resources',
    'version': '19.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'phone_validation', 'mail', 'web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/odoo_hospital_menu.xml',
        'views/odoo_hospital_doctor_views.xml',
        'views/odoo_hospital_doctor_category_views.xml',
        'views/odoo_hospital_patient_views.xml',
        'views/odoo_hospital_type_disease_views.xml',
        'views/odoo_hospital_appointment_views.xml',
        'views/odoo_hospital_doctor_history_views.xml',

        'wizard/osl_hospotal_set_doctor_wizard_view.xml',
        'wizard/osl_hospital_visit_report_wizard_view.xml',

        'data/osl_doctor_category_data.xml',
        'data/osl_appointment_server_action.xml',
        'data/osl_hospital_cron.xml',

        'report/osl_hospital_custom_external_template.xml',
        'report/osl_hospital_doctor_report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/osl_type_disease_demo.xml',
        'demo/osl_doctor_demo.xml',
        'demo/osl_patient_demo.xml',
        'demo/osl_appointment_demo.xml',
        'demo/osl_doctor_history.xml',
    ],

    'installable': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],

    'assets': {
        'web.report_assets_common': [
            'hr_hospital/static/src/**/*.scss',
        ],
        # 'web.assets_common': [
        #     'hr_hospital/static/src/**/*.scss',
        # ],
        # 'web.assets_backend': [
        #     'hr_hospital/static/src/**/*.scss',
        # ]
    },

}
