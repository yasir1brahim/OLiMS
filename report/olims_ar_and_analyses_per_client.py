# -*- coding: utf-8 -*-

import time
from openerp import api, models
import datetime


class ReportAnalysisRequestsAndAnalysesPerClient(models.AbstractModel):
    _name = 'report.OLiMS.report_ar_and_analyses_per_client'

    def _get_client_analysis(self, analyses_request):

        datalines = {}
        footlines = {}
        data = {}
        total_analyses = total_requests = 0
        for analysis in analyses_request:
            total_requests += 1
            data['request'] = 1
            data['analyses'] = 0
            for servie_val in analysis.FieldService:
                if servie_val.Service.Service:
                    data['analyses'] += 1
            for lab_servie_val in analysis.LabService:
                if lab_servie_val.LabService.Service:
                    data['analyses'] += 1
            total_analyses += data['analyses']
            if str(analysis.Client.Name) in datalines:
                oldData = datalines[str(analysis.Client.Name)]
                oldData['request'] += 1
                oldData['analyses'] += data['analyses']
                datalines[str(analysis.Client.Name)] = oldData
            else:
                datalines[str(analysis.Client.Name)] = {'request' : 1, 'analyses' : data['analyses']}
        
        footline = {'request' : total_requests,
                    'analyses' : total_analyses
                    }
        footlines['Total'] = footline
        return datalines, footlines


    @api.multi
    def render_html(self, data):
        client = None
        startdate = datetime.datetime.strptime(data['form'].get('date_from'), \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        enddate = datetime.datetime.strptime(data['form'].get('date_to'), \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        analysisstate = str(data['form'].get('analysis_state'))
        if data['form'].get('client'):
            client = data['form'].get('client')[0]
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        if not (client is None):
            analyses_request = self.env['olims.analysis_request'].search([('create_date', '>=', startdate), \
            ('create_date', '<=', enddate), \
            ('state', '=', analysisstate),\
            ('Client', '=', client)
            ])
        else:
            analyses_request = self.env['olims.analysis_request'].search([('create_date', '>=', startdate), \
            ('create_date', '<=', enddate), \
            ('state', '=', analysisstate),
            ])

        analysis_res, footlines = self.with_context(data['form'].get('used_context'))._get_client_analysis(analyses_request)
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Analyses': analysis_res,
            'footlines' : footlines
        }
        return self.env['report'].render('OLiMS.report_ar_and_analyses_per_client', docargs)