# -*- coding: utf-8 -*-
from openerp import http
import openerp
from werkzeug.utils import redirect
import functools
from HTMLParser import HTMLParser
from openerp import models, fields, api
from StringIO import StringIO
from openerp.http import request
from openerp.addons.web.controllers.main import serialize_exception,content_disposition
import base64
import StringIO

import pdb
from openerp.addons.web.http import Controller, route
from openerp.addons.report.controllers.main import ReportController
from openerp.addons.web.controllers.main import _serialize_exception, content_disposition
from openerp.osv import osv
from openerp import http
import simplejson
import time
import logging
from werkzeug import exceptions, url_decode
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse
from werkzeug.datastructures import Headers
import openerp.tools as tools
import openerp.addons.decimal_precision as dp
from openerp.tools import html_escape
import re


class Binary(http.Controller):
    @http.route('/web/binary/download_document', type='http', auth="public")
    @serialize_exception
    def download_document(self, model, field, id, filename=None, **kw):
        """ Download link for files stored as binary fields.
        :param str model: name of the model to fetch the binary from
        :param str field: binary field
        :param str id: id of the record from which to fetch the binary
        :param str filename: field holding the file's name, if any
        :returns: :class:`werkzeug.wrappers.Response`
        """
        Model = request.registry['labpal.experiment']
        cr, uid, context = request.cr, request.uid, request.context
        fields = [field]
        res = Model.read(cr, uid, [int(id)], fields, context)[0]
        csv_file = StringIO()
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["1", "a", "b", "c"])
        filecontent = base64.b64decode(csv_file)

        if not filecontent:
            return request.not_found()
        else:
            if not filename:
                filename = '%s_%s' % (model.replace('.', '_'), id)
                return request.make_response(filecontent,
                                             [('Content-Type', 'application/octet-stream'),
                                              ('Content-Disposition', content_disposition(filename))])


class Labpal(http.Controller):

    def serialize_exception(f):
        @functools.wraps(f)
        def wrap(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception, e:
                _logger.exception("An exception occured during an http request")
                se = _serialize_exception(e)
                error = {
                    'code': 200,
                    'message': "Odoo Server Error",
                    'data': se
                }
                return werkzeug.exceptions.InternalServerError(json.dumps(error))
        return wrap

    @http.route('/experiment/new/', auth='public', website=True)
    def index(self, **kw):
        return http.request.render( "olims.listing", {})


class NewReportController(ReportController):
    @route(['/report/download'], type='http', auth="user")
    def report_download(self, data, token):
        """This function is used by 'qwebactionmanager.js' in order to trigger the download of
        a pdf/controller report.

        :param data: a javascript array JSON.stringified containg report internal url ([0]) and
        type [1]
        :returns: Response with a filetoken cookie and an attachment header
        """
        requestcontent = simplejson.loads(data)
        url, type = requestcontent[0], requestcontent[1]
        try:

            if type == 'qweb-pdf':
                reportname = url.split('/report/pdf/')[1].split('?')[0]
                cr, uid, context = request.cr, request.uid, request.context
                report_file = reportname.split('/')[0]
                report = request.registry['report']._get_report_from_name(cr, uid, report_file)
                filename = "%s.%s" % (report.name, "pdf")
                docids = None

                if '/' in reportname:
                    reportname, docids = reportname.split('/')
                    print 'doc ids',docids
                if docids:
                    # Generic report:
                    response = self.report_routes(reportname, docids=docids, converter='pdf')
                    # switch reportname with the evaluated attachment attribute of the action if available
                    docids = [int(i) for i in docids.split(',')]
                    if reportname == 'olims.report_certificate_of_analysis' and len(docids) == 1:
                        report_obj = request.registry['report']
                        obj = report_obj.pool[report.model].browse(cr, uid, docids[0])

                        if obj.ClientReference and not obj.LotID:
                            reportname = obj.ClientReference

                        elif obj.LotID and not obj.ClientReference:
                            reportname = obj.LotID

                        elif obj.LotID and  obj.ClientReference:
                            reportname = obj.LotID +'-'+ obj.ClientReference

                        else:
                            reportname = "COA"

                        filename = "%s.%s" % (reportname, "pdf")

                else:
                    # Particular report:
                    data = url_decode(url.split('?')[1]).items()  # decoding the args represented in JSON
                    response = self.report_routes(reportname, converter='pdf', **dict(data))
                response.headers.add('Content-Disposition', content_disposition(filename))
                response.set_cookie('fileToken', token)
                return response

            elif type == 'controller':
                reqheaders = Headers(request.httprequest.headers)
                response = Client(request.httprequest.app, BaseResponse).get(url, headers=reqheaders, follow_redirects=True)
                response.set_cookie('fileToken', token)
                return response

            else:
                return

        except Exception, e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return request.make_response(html_escape(simplejson.dumps(error)))
