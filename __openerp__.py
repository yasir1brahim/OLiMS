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
        'templates.xml',
        'labpal_report.xml',
        'labpal_database_template.xml',
        'labpal_experiment_template.xml',
        'labpal_mail_template.xml',
        'views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}