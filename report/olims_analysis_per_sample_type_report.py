import time
from openerp import api, models
import datetime
from collections import OrderedDict


class ReportAnalysisPerSampleType(models.AbstractModel):
    _name = 'report.olims.report_analysisper_sample_type'

    def _get_analyses(self, analyses, sample_types):
        samples_analyses_dict = {}
        for sample_type in sample_types:
            samples_analyses_dict[sample_type.SampleType] = 0
        for analysis in analyses:
            samples_analyses_dict[analysis.SampleType.SampleType] += 1
        sorted_samples_analyses_dict = OrderedDict(sorted(samples_analyses_dict.items()))
        return sorted_samples_analyses_dict



    @api.multi
    def render_html(self, data):
        client = data['form'].get('client_id')[0]
        startdate = datetime.datetime.strptime(data['form'].get('date_from'), \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        enddate = datetime.datetime.strptime(data['form'].get('date_to'), \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        analysisstate = str(data['form'].get('analysis_state'))
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        analyses = self.env['olims.analysis_request'].search([('create_date', '>=', startdate), \
            ('create_date', '<=', enddate), \
            ('state', '=', analysisstate),\
            ('Client', '=', client),
            ])
        sample_types = self.env['olims.sample_type'].search([])
        analysis_res = self.with_context(data['form'].get('used_context'))._get_analyses(analyses,sample_types)
        total = sum(analysis_res.values())
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Analyses': analysis_res,
            'Total' : total
        }
        return self.env['report'].render('olims.report_analysisper_sample_type', docargs)