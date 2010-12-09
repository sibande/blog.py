import os, sys

ROOT_PATH = os.path.dirname(__file__)

sys.path = [ROOT_PATH, '%s/lib' % os.path.dirname(ROOT_PATH),] + sys.path

import web
import urls
from web import form

from google.appengine.api import users

from utils.template import render_template
from utils.sessionLib import ManageClientSession
from utils.decorators import admin_perm_required

from models import Post, Comment


context = dict()

post_form = form.Form(
    form.Textbox('title',
                 form.notnull,
                 class_='title',
                 description='Title'), 
    form.Textarea('body',
                  form.notnull,
                  class_="post",
                  description='Body'),
    form.Checkbox('active', description='Active'),
    form.Button('Post'),
)

comment_form = form.Form(
    form.Textbox('name',
                 form.notnull,
                 class_='text',
                 description='Name'), 
    form.Textbox('url',
                 class_='text',
                 description='Website (optional, eg: http://sibande.com)'), 
    form.Textbox('email',
                 form.notnull,
                 class_='text',
                 description='E-mail'), 
    form.Textarea('body',
                  form.notnull,
                  description='Body'),
    form.Button('Comment'),
)

class index:
    def GET(self):
        posts = Post.all().filter('active =', True).order('-datetime')
        context['posts'] = posts
        return render_template('index.html', **context)
    def POST(self):
        return web.seeother('/')


class add_edit:

    def __init__(self):
        self.form_class = post_form
    def init_data(self, post_id, action):
        try:
            self.post_id = int(post_id)
            self.post = Post.get_by_id(self.post_id)
            context['page_path'] = '/post/'+self.post.slug+'-'+str(self.post.key().id())+'/edit'
        except TypeError:
            self.post_id = 0
            context['page_path'] = '/post/add'
        self.form = self.form_class()
        if action == 'edit':
            self.form.get('title').value = self.post.title
            self.form.get('body').value = self.post.body
            self.form.get('active').value = self.post.active            
    @admin_perm_required
    def GET(self, post_id=None, action='add'):
        self.init_data(post_id, action)
        context['form'] = self.form
        return render_template('add.html', **context)
    @admin_perm_required
    def POST(self, post_id=None, action='add'):
        self.init_data(post_id, 'update') #switch to "update" and loose "edit" state
        form = self.form_class()
        if form.validates():
            active = True if form.get('active').value else False
            title = form.get('title').value
            body = form.get('body').value
            if action == 'edit':
                post_data = self.post
                post_data.title=title
                post_data.body=body
            else:
                post_data = Post(title=title,
                                 body=body,)
            post_data.active=active
            post_data.put()

            return web.seeother('/post/'+post_data.slug+'-'+str(post_data.key().id()), absolute=True)

        context['form'] = form
        return render_template('add.html', **context)


class view:

    def __init__(self):
        self.form_class = comment_form
    def init_data(self, slug, post_id):
        try:
            self.post_id = int(post_id)
        except TypeError:
            self.post_id = 0
        self.post = Post.get_by_id(self.post_id)
        context['comments'] = Comment.all().filter('post =', self.post).order('-datetime')
        context['post'] = self.post
    def GET(self, slug, post_id):
        self.init_data(slug, post_id)
        
        context['form'] = self.form_class()
        return render_template('view.html', **context)
    def POST(self, slug, post_id):
        self.init_data(slug, post_id)
        form = self.form_class()
        if form.validates():
            comment_data = Comment(post=self.post,
                                   name=form.get('name').value,
                                   url=form.get('url').value,
                                   email=form.get('email').value,
                                   body=form.get('body').value,
                                   active=True,)
            comment_data.put()
            return web.seeother('/post/'+self.post.slug+'-'+str(self.post.key().id()), absolute=True)
        context['form'] = form
        return render_template('view.html', **context)

#urls
mapper = ('/', 'index',
          '/post/add', 'add_edit',
          '/post/(.*)-(\d+)', 'view',
          '/post/.*-(\d+)/(edit)', 'add_edit',)
    
def session_loadhook():
    web.user = ManageClientSession(web)
    web.google_accounts = users
    context['google_accounts'] = users

app = web.application(mapper, globals())
app.add_processor(web.loadhook(session_loadhook))

if __name__ == "__main__":
    main = app.cgirun()
    
