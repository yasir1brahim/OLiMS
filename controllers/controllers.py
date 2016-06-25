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

class Binary(http.Controller):
 @http.route('/web/binary/download_document', type='http', auth="public")
 @serialize_exception
 def download_document(self,model,field,id,filename=None, **kw):
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
     csv_writer.writerow(["1","a","b","c"])
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

