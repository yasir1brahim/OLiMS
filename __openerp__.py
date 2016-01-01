# -*- coding: utf-8 -*-
{
    'name': "OLiMS",

    'summary': """Open Source LIMS""",

    'description': """
        OLiMS Modules:
            - Analysis management
            - Sampling management
    """,

    'author': "Lablynx Inc.",
    'website': "http://www.lablynx.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'data/res.groups.csv',
        'demo.xml',
        'views/olims.xml',
        'views/partner.xml',
        'views/session_workflow.xml',
        'security/ir.model.access.csv',
        'workflows/sample_workflow.xml',
        'data/workflow.csv',
        'data/workflow.activity.csv',
        'data/workflow.transition.csv',
        'data/olims.country.csv',
        'data/olims.state.csv',
        'OLiMS_report.xml',
        'views/report_sample.xml',
        'views/report_analysisper_service.xml',
        'views/report_analysisper_sample_type.xml',
        'views/report_sample_received_vs_reported.xml',
        'views/report_ar_and_analyses_per_client.xml',
        'views/report_analyses_per_department.xml',
        'wizard/olims_report_commom_view.xml',
        'wizard/olims_report_sample_view.xml',
        'wizard/olims_report_analysisper_service.xml',
        'wizard/olims_analysis_per_sample_type_report.xml',
        'wizard/olims_sample_received_vs_reported_view.xml',
        'wizard/olims_ar_and_analyses_per_client_view.xml',
        'wizard/olims_analyses_per_department_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}