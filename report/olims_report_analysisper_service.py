import time
from openerp import api, models
import datetime


class ReportAnalysisPerService(models.AbstractModel):
    _name = 'report.olims.report_analysisper_service'

    def _get_analyses(self, analyses, analyses_services):
        service_analyses_dict = {}
        service_category = {}
        for service in analyses_services:
            service_analyses_dict[service.Service] = 0
            if service.category.Category not in service_category:
                service_category[service.category.Category] = [str(service.Service)]
            else:
                service_category[service.category.Category].append(str(service.Service))
        for analysis in analyses:
            for servie_val in analysis.FieldService:
                service_analyses_dict[servie_val.Service.Service] += 1
            for lab_servie_val in analysis.LabService:
                service_analyses_dict[lab_servie_val.LabService.Service] += 1


        return service_analyses_dict , service_category


    @api.multi
    def render_html(self, data):
        startdate = datetime.datetime.strptime(data['form'].get('date_from'), \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        enddate = datetime.datetime.strptime(data['form'].get('date_to'), \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        analysisstate = str(data['form'].get('analysis_state'))
        client = data['form'].get('client')[0]
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        analyses = self.env['olims.analysis_request'].search([('create_date', '>=', startdate), \
            ('create_date', '<=', enddate), \
            ('state', '=', analysisstate),\
            ('Client', '=', client)
            ])
        analyses_services = self.env['olims.analysis_service'].search([])
        analysis_res, service_category = self.with_context(data['form'].get('used_context'))._get_analyses(analyses, analyses_services)
        total = sum(analysis_res.values())
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Analyses': analysis_res,
            'Category': service_category,
            'Total': total
        }
        return self.env['report'].render('olims.report_analysisper_service', docargs)