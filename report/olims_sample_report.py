# -*- coding: utf-8 -*-

import time
from openerp import api, models
import datetime


class ReportSample(models.AbstractModel):
    _name = 'report.olims.report_sample'

    def _get_samples(self, samples):
        samples_res = []
        for sample in samples:
            res = dict((fn, sample.name) for fn in ['name'])
            res['SampleID'] = sample.SampleID
            res['SampleType'] = sample.SampleType.SampleType
            res['DateReceived'] = sample.DateReceived
            res['ClientSampleID'] = sample.Client.Name
            samples_res.append(res)
        return samples_res


    @api.multi
    def render_html(self, data):
        startdate = datetime.datetime.strptime(data['form'].get('date_from'), \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        enddate = datetime.datetime.strptime(data['form'].get('date_to'), \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        samples = self.env['olims.sample'].search([('SamplingDate', '>=', startdate), ('SamplingDate', '<=', enddate)])
        samples_res = self.with_context(data['form'].get('used_context'))._get_samples(samples)

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Samples': samples_res,
            'Count' : len(samples_res)
        }
        return self.env['report'].render('olims.report_sample', docargs)