import time
from openerp import api, models
import datetime


class ReportDataEntryDayBook(models.AbstractModel):
    _name = 'report.olims.report_dataentrydaybook'

    @api.multi
    def render_html(self, data):
        startdate = datetime.datetime.strptime(data['form'].get('date_from'), \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        enddate = datetime.datetime.strptime(data['form'].get('date_to'), \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        AnalysesRequest = self.env['olims.analysis_request'].search([('create_date', '>=', startdate), \
            ('create_date', '<=', enddate),
            ])
        datalines, footlines = self.with_context(data['form'].get('used_context'))._get_analyses(AnalysesRequest)
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'datalines': datalines,
            'footlines' : footlines
        }
        return self.env['report'].render('olims.report_dataentrydaybook', docargs)

    def _get_analyses(self, AnalysesRequest):

        # # parms = []
        # # titles = []

        # # # Apply filters
        # # self.contentFilter = {'portal_type': 'AnalysisRequest'}
        # # val = self.selection_macros.parse_daterange(self.request,
        # #                                             'getDateCreated',
        # #                                             _('Date Created'))
        # # if val:
        # #     self.contentFilter[val['contentFilter'][0]] = val['contentFilter'][1]
        # #     parms.append(val['parms'])
        # #     titles.append(val['titles'])

        # # Query the catalog and store results in a dictionary
        ars = AnalysesRequest
        # if not ars:
        #     message = _("No Analysis Requests matched your query")
        #     self.context.plone_utils.addPortalMessage(message, "error")
        #     return self.default_template()

        datalines = {}
        footlines = {}
        totalcreatedcount = len(ars)
        totalreceivedcount = 0
        totalpublishedcount = 0
        totalanlcount = 0
        totalreceptionlag = 0
        totalpublicationlag = 0
        datereceived = ''
        datepublished = ''
        totalreceivedcreated_ratio = 0
        totalpublishedcreated_ratio = 0
        for ar in ars:
            # ar = ar.getObject()
            datecreated = datetime.datetime.strptime(ar.create_date, \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
            if ar.state == 'sample_received':
                datereceived = datetime.datetime.strptime(ar.DateReceived, \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
            if ar.state == 'published':
                datepublished = datetime.datetime.strptime(ar.DatePublished, \
            "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")

            receptionlag = 0
            publicationlag = 0
            anlcount = len(ar.FieldService.Service) or len(ar.FieldService.LabService)

            dataline = {
                "AnalysisRequestID": ar.RequestID,
                "DateCreated": datecreated,
                "DateReceived": datereceived,
                "DatePublished": datepublished,
                "ReceptionLag": receptionlag,
                "PublicationLag": publicationlag,
                "TotalLag": receptionlag + publicationlag,
                "BatchID": ar.Batch.Title if ar.Batch else '',
                "SampleID": ar.Sample_id.SampleID,
                "SampleType": ar.SampleType.SampleType,
                "NumAnalyses": anlcount,
                "ClientID": ar.Client.ClientID,
                "Creator": ar.create_uid.name,
                # "Remarks": #ar.Remarks
            }

            datalines[ar.getRequestID()] = dataline

            totalreceivedcount += ar.getDateReceived() and 1 or 0
            totalpublishedcount += ar.getDatePublished() and 1 or 0
            totalanlcount += anlcount
            totalreceptionlag += receptionlag
            totalpublicationlag += publicationlag

        # Footer total data
        if totalcreatedcount > 0:
            totalreceivedcreated_ratio = float(totalreceivedcount) / float(
            totalcreatedcount)
            totalpublishedcreated_ratio = float(totalpublishedcount) / float(
            totalcreatedcount)
        totalpublishedreceived_ratio = totalreceivedcount and float(
            totalpublishedcount) / float(totalreceivedcount) or 0
        
        try:
            footline = {'Created': totalcreatedcount,
                    'Received': totalreceivedcount,
                    'Published': totalpublishedcount,
                    'ReceivedCreatedRatio': totalreceivedcreated_ratio,
                    'ReceivedCreatedRatioPercentage': ('{0:.0f}'.format(
                        totalreceivedcreated_ratio * 100)) + "%",
                    'PublishedCreatedRatio': totalpublishedcreated_ratio,
                    'PublishedCreatedRatioPercentage': ('{0:.0f}'.format(
                        totalpublishedcreated_ratio * 100)) + "%",
                    'PublishedReceivedRatio': totalpublishedreceived_ratio,
                    'PublishedReceivedRatioPercentage': ('{0:.0f}'.format(
                        totalpublishedreceived_ratio * 100)) + "%",
                    'AvgReceptionLag': (
                    '{0:.1f}'.format(totalreceptionlag / totalcreatedcount)),
                    'AvgPublicationLag': (
                    '{0:.1f}'.format(totalpublicationlag / totalcreatedcount)),
                    'AvgTotalLag': ('{0:.1f}'.format((
                                                     totalreceptionlag + totalpublicationlag) / totalcreatedcount)),
                    'NumAnalyses': totalanlcount
        }
        except:
            footline = {'Created': totalcreatedcount,
                    'Received': totalreceivedcount,
                    'Published': totalpublishedcount,
                    'ReceivedCreatedRatio': totalreceivedcreated_ratio,
                    'ReceivedCreatedRatioPercentage': ('{0:.0f}'.format(
                        totalreceivedcreated_ratio * 100)) + "%",
                    'PublishedCreatedRatio': totalpublishedcreated_ratio,
                    'PublishedCreatedRatioPercentage': ('{0:.0f}'.format(
                        totalpublishedcreated_ratio * 100)) + "%",
                    'PublishedReceivedRatio': totalpublishedreceived_ratio,
                    'PublishedReceivedRatioPercentage': ('{0:.0f}'.format(
                        totalpublishedreceived_ratio * 100)) + "%",
                    'AvgReceptionLag': (
                    '{0:.1f}'.format(totalreceptionlag / 1)),
                    'AvgPublicationLag': (
                    '{0:.1f}'.format(totalpublicationlag / 1)),
                    'AvgTotalLag': ('{0:.1f}'.format((
                                                     totalreceptionlag + totalpublicationlag) / 1)),
                    'NumAnalyses': totalanlcount}

        footlines['Total'] = footline
        return datalines, footlines
