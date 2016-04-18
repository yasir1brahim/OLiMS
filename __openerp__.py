# -*- coding: utf-8 -*-
{
    'name': "labpal",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web','mail','report','report_webkit'],
    'css': ['static/css/js/*.css'],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'web_preload': True,

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views.xml',
        # 'experiment_export.xml',
        'templates.xml',
        #'labpal_mail_compose_wizard.xml',
        # 'labpal_report.xml',
        # 'sale_template.xml',
        # 'report_experiment.xml',
        'pdf_template.xml',
        'topdf.xml',
        'pdf_db_template.xml',
        'topdf_db.xml',
        'wizard/export_experiment_view.xml'
        #'tocsv.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}