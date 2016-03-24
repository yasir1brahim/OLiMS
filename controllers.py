# -*- coding: utf-8 -*-
from openerp import http
import openerp
from werkzeug.utils import redirect


class Labpal(http.Controller):
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