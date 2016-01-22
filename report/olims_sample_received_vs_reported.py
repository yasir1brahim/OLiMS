# -*- coding: utf-8 -*-

import time
from openerp import api, models
import datetime


class ReportSampleReceivedvsReported(models.AbstractModel):
    _name = 'report.olims.report_sample_received_vs_reported'

    def _get_samples(self, samples):
        datalines = {}
        footlines = {}
        total_received_count = 0
        total_published_count = 0
        for sample in samples:

            # For each sample, retrieve check is has results published
            # and add it to datalines
            published = False
            analyses = self.env['olims.analysis_request'].search([('Sample_id', '=', sample.id)])
            if analyses:
                for analysis in analyses:
                    if not (analysis.DatePublished is False):
                        published = True
                        break

            datereceived = datetime.datetime.strptime(sample.DateReceived, \
                                "%Y-%m-%d %H:%M:%S")
            monthyear = datereceived.strftime("%B") + " " + datereceived.strftime(
                "%Y")
            received = 1
            publishedcnt = published and 1 or 0
            if (monthyear in datalines):
                received = datalines[monthyear]['ReceivedCount'] + 1
                publishedcnt = published and datalines[monthyear][
                                                 'PublishedCount'] + 1 or \
                               datalines[monthyear]['PublishedCount']
            ratio = publishedcnt / received
            dataline = {'MonthYear': monthyear,
                        'ReceivedCount': received,
                        'PublishedCount': publishedcnt,
                        'UnpublishedCount': received - publishedcnt,
                        'Ratio': ratio,
                        'RatioPercentage': '%02d' % (
                        100 * (float(publishedcnt) / float(received))) + '%'}
            datalines[monthyear] = dataline

            total_received_count += 1
            total_published_count = published and total_published_count + 1 or total_published_count

        # Footer total data
        if total_received_count > 0:
            ratio = total_published_count / total_received_count
        else:
            ratio = total_published_count / 1
        try:
            footline = {'ReceivedCount': total_received_count,
                    'PublishedCount': total_published_count,
                    'UnpublishedCount': total_received_count - total_published_count,
                    'Ratio': ratio,
                    'RatioPercentage': '%02d' % (100 * (
                    float(total_published_count) / float(
                        total_received_count))) + '%'
            }
        except:
            footline = {'ReceivedCount': total_received_count,
                    'PublishedCount': total_published_count,
                    'UnpublishedCount': total_received_count - total_published_count,
                    'Ratio': ratio,
                    'RatioPercentage': '%02d' % (100 * (
                    float(total_published_count) / float(
                        1))) + '%'
            }
            
        footlines['Total'] = footline

        return datalines, footlines


    @api.multi
    def render_html(self, data):
        startdate = datetime.datetime.strptime(data['form'].get('date_from'), \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        enddate = datetime.datetime.strptime(data['form'].get('date_to'), \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        samples = self.env['olims.sample'].search([('SamplingDate', '>=', startdate), \
                    ('SamplingDate', '<=', enddate), \
                    ('state', 'in', ['sample_received','expired','disposed'])])
        samples_res, footlines= self.with_context(data['form'].get('used_context'))._get_samples(samples)

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Samples': samples_res,
            'footlines' : footlines #sum(samples_res.values())
        }
        return self.env['report'].render('olims.report_sample_received_vs_reported', docargs)