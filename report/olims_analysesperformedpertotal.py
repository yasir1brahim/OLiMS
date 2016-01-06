import time
from openerp import api, models
import datetime


class ReportAnalysisPerformedPerTotal(models.AbstractModel):
    _name = 'report.olims.report_analysesperformedpertotal'

    @api.multi
    def render_html(self, data):
        groupby = str(data['form'].get('groupby'))
        startdate = datetime.datetime.strptime(data['form'].get('date_from'), \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        enddate = datetime.datetime.strptime(data['form'].get('date_to'), \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        analyses = self.env['olims.analysis_request'].search([('create_date', '>=', startdate), \
            ('create_date', '<=', enddate),
            ])
        datalines, footlines = self.with_context(data['form'].get('used_context'))._get_analyses(analyses,groupby)
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'datalines': datalines,
            'footlines' : footlines
        }
        return self.env['report'].render('olims.report_analysesperformedpertotal', docargs)

    def _get_analyses(self, analyses, groupby):

        datalines = {}
        footlines = {}
        totalcount = len(analyses)
        totalpublishedcount = 0
        totalperformedcount = 0
        for analysis in analyses:
            # analysis = analysis.getObject()
            analysisfiledservice = analysis.FieldService
            analysislabservice  = analysis.LabService
            for service in analysisfiledservice:
                ankeyword = service.Service.Keyword
                antitle = service.Service.Service
            for service in analysislabservice:
                ankeyword = service.LabService.Keyword
                antitle = service.LabService.Service
            daterequested = analysis.create_date
            daterequested = datetime.datetime.strptime(daterequested, \
                                                "%Y-%m-%d %H:%M:%S")

            group = ''
            if groupby == 'Day':
                group = self.ulocalized_time(daterequested)
            elif groupby == 'Week':
                group = daterequested.strftime(
                    "%Y") + ", " + daterequested.strftime("%U")
            elif groupby == 'Month':
                group = daterequested.strftime(
                    "%B") + " " + daterequested.strftime("%Y")
            elif groupby == 'Year':
                group = daterequested.strftime("%Y")
            else:
                group = ''

            dataline = {'Group': group, 'Requested': 0, 'Performed': 0,
                        'Published': 0, 'Analyses': {}}
            anline = {'Analysis': antitle, 'Requested': 0, 'Performed': 0,
                      'Published': 0}
            if (group in datalines):
                dataline = datalines[group]
                if (ankeyword in dataline['Analyses']):
                    anline = dataline['Analyses'][ankeyword]

            grouptotalcount = dataline['Requested'] + 1
            groupperformedcount = dataline['Performed']
            grouppublishedcount = dataline['Published']

            anltotalcount = anline['Requested'] + 1
            anlperformedcount = anline['Performed']
            anlpublishedcount = anline['Published']

            arstate = analysis.state
            if (arstate == 'published'):
                anlpublishedcount += 1
                grouppublishedcount += 1
                totalpublishedcount += 1
            # TODO
            # if (analysis.getResult()):
            #     anlperformedcount += 1
            #     groupperformedcount += 1
            #     totalperformedcount += 1

            group_performedrequested_ratio = float(groupperformedcount) / float(
                grouptotalcount)
            group_publishedperformed_ratio = groupperformedcount > 0 and float(
                grouppublishedcount) / float(groupperformedcount) or 0

            anl_performedrequested_ratio = float(anlperformedcount) / float(
                anltotalcount)
            anl_publishedperformed_ratio = anlperformedcount > 0 and float(
                anlpublishedcount) / float(anlperformedcount) or 0

            dataline['Requested'] = grouptotalcount
            dataline['Performed'] = groupperformedcount
            dataline['Published'] = grouppublishedcount
            dataline['PerformedRequestedRatio'] = group_performedrequested_ratio
            dataline['PerformedRequestedRatioPercentage'] = ('{0:.0f}'.format(
                group_performedrequested_ratio * 100)) + "%"
            dataline['PublishedPerformedRatio'] = group_publishedperformed_ratio
            dataline['PublishedPerformedRatioPercentage'] = ('{0:.0f}'.format(
                group_publishedperformed_ratio * 100)) + "%"

            anline['Requested'] = anltotalcount
            anline['Performed'] = anlperformedcount
            anline['Published'] = anlpublishedcount
            anline['PerformedRequestedRatio'] = anl_performedrequested_ratio
            anline['PerformedRequestedRatioPercentage'] = ('{0:.0f}'.format(
                anl_performedrequested_ratio * 100)) + "%"
            anline['PublishedPerformedRatio'] = anl_publishedperformed_ratio
            anline['PublishedPerformedRatioPercentage'] = ('{0:.0f}'.format(
                anl_publishedperformed_ratio * 100)) + "%"

            dataline['Analyses'][ankeyword] = anline
            datalines[group] = dataline

        # Footer total data
        total_performedrequested_ratio = float(totalperformedcount) / float(
            totalcount)
        total_publishedperformed_ratio = totalperformedcount > 0 and float(
            totalpublishedcount) / float(totalperformedcount) or 0

        footline = {'Requested': totalcount,
                    'Performed': totalperformedcount,
                    'Published': totalpublishedcount,
                    'PerformedRequestedRatio': total_performedrequested_ratio,
                    'PerformedRequestedRatioPercentage': ('{0:.0f}'.format(
                        total_performedrequested_ratio * 100)) + "%",
                    'PublishedPerformedRatio': total_publishedperformed_ratio,
                    'PublishedPerformedRatioPercentage': ('{0:.0f}'.format(
                        total_publishedperformed_ratio * 100)) + "%"}

        footlines['Total'] = footline

        return datalines, footlines
