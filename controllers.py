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

##print "Work"
#csv = request.session.model('labpal.experiment').get_csv_old()
#print "CSV CSV", csv.getvalue()



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



    #@http.route('/web/dataset/call_kw/labpal.experiment/write', type='json', auth="user", website = "True")
    #@serialize_exception
    #def get_csv_one(self,**kw):
        #web.header('Content-Type','text/csv')
        #web.header('Content-disposition', 'attachment; filename=yourfilename.csv')
     #   return "Hello World"
      #  csv = request.session.model('labpal.experiment').get_csv_old()
       # print csv.getvalue()
        #return csv.getvalue()

    @http.route('/experiment/new/', auth='public', website=True)
    def index(self, **kw):
        return http.request.render( "labpal.listing", {})

    @http.route('/experiments', auth='public', website=True)
    def list(self, **kw):
        return http.request.render('labpal.experiment_list', {
            'objects': http.request.env['labpal.experiment'].search([]),
        })

    @http.route('/experiments/<model("labpal.experiment"):obj>/view/', website=True)
    def view(self, obj):
        return http.request.render('labpal.exp_view',
                              {'obj': obj})

    @http.route('/experiments/<model("labpal.experiment"):obj>/edit/', website=True)
    def edit(self, obj):
        # form = PostsNewForm(request.httprequest.form)
        # if request.httprequest.method == 'POST' and form.validate():
        #     post.write({
        #         'title': form_data.get('title', ''),
        #         'content': form_data.get('content', ''),
        #     })
        #     return redirect("/posts/%s/view" % slug(post))
        # form.title.data = post.title
        # form.content.data = post.content
        return http.request.render('labpal.exp_edit',
                              {'obj': obj})

    @http.route('/labpal/experiment/', auth='public', methods=['POST'], csrf=False, website=True)
    def object(self, **post):
    	print post.get('tag')
    	db_name = http.request.session._db
    	print db_name
    	experiment_model = http.request.session.model('labpal.experiment')
    	values = {'exp_tags':'asdf',
    		'exp_date': post.get('date'),
    		'status_visibility': post.get('visibility'),
    		'description':'asdf',
    		'exp_title': 'asdf',
    		'exp_formula':post.get('formulafile')
    	}
    	experiment_model.create(values)
    	experiment_obj = experiment_model.search([('id', '=', 1)])
    	print experiment_obj
    	# cr = openerp.pooler.get_db(db_name).cursor() 
     # 	pool = openerp.pooler.get_pool(db_name)
     # 	experiment_model = pool.get('labpal.experiment')
        # return http.request.render('labpal.object', {
        #     'object': obj
        # })
# class Posts(http.Controller):

#     @http.route('/posts/', website=True)
#     def list(self):
#         posts = http.request.env['blog.post']
#         posts = posts.search([])
#         return http.request.render('labpal.posts_list',
#                               {'posts': posts})

#     @http.route('/posts/new/', website=True, csrf=False)
#     def new(self, **form_data):
# 		form = PostsNewForm(http.request.httprequest.form)
# 		if http.request.httprequest.method == 'POST' and form.validate():
# 			posts = http.request.env['blog.post']
# 			posts.create({
# 				'title': form_data.get('title', ''),
# 				'content': form_data.get('content', ''),
# 				})
# 			return redirect("/posts/")
# 		return http.request.render('labpal.posts_new', {'form': form})


# from wtforms import Form, StringField, TextAreaField, validators


# class PostsNewForm(Form):
#     title = StringField('Title', [validators.Required()])
#     content = TextAreaField('Content', [validators.Required()])