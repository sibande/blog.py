import os, sys

ROOT_PATH = os.path.dirname(__file__)

sys.path = [ROOT_PATH, '%s/lib' % os.path.dirname(ROOT_PATH),] + sys.path

import web
from web import form

from google.appengine.api import users

from utils.template import render_template
from utils.decorators import admin_perm_required

from models import Post, Comment, Static


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

static_form = form.Form(
    form.Textbox('position',
                 form.notnull,
                 form.regexp('\d+', 'Must be a digit'),
                 class_='text',
                 description='Position number'),
    form.Textbox('name',
                 form.notnull,
                 class_='text',
                 description='Name (absolute page path)'),
    form.Textbox('label',
                 form.notnull,
                 class_='text',
                 description='Link label'),
    form.Textbox('title',
                 class_='text',
                 description='Full page label'),
    form.Textarea('content',
                 form.notnull,
                 class_='text',
                 description='Content'),
    form.Checkbox('active', description='Active'),
    form.Button('Post'),
)


class index:
    def GET(self):
        context['posts'] = Post.all().filter('active =', True).order('-datetime')

        return render_template('index.html', **context)
    def POST(self):
        page = web.input().get('page')
        if page:
            return web.seeother(page, absolute=True)
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
        self.init_data(post_id, 'update') #switch to "update" and lose "edit" state
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

class feed_server:

    def GET(self):
        posts = Post.all().filter('active =', True).order('-datetime')
        web.header('Content-type','text/xml')
        data = '<rss version="2.0">'
        data += '<channel>'
        data += '<title>Sibande\'s Thoughts</title>'
        data += '<link>http://www.sibande.com/</link>'
        data += '<description>Random thoughs by Sibande_</description>'
        for post in posts:
            data += '<item>'
            data += '<title>'+post.title+'</title>'
            data += '<link>'+'http://www.sibande.com/post/'+post.slug+'-'+str(post.key().id())+'</link>'
            data += '<description>'+post.body.split('\n')[0]+'</description>'
            data += '<pubDate>'+str(post.datetime)+'</pubDate>'
            data += '</item>'
        data += '</channel>'
        data += '</rss>'
        return data
    def POST(self):
        return web.seeother('/', absolute=True)
        

class static_content:

    def init_data(self, name, action):
        self.content = Static.all().filter('name =', name).get()
        self.form_class = static_form
        form = self.form_class()
        if not self.content or action == 'edit':
            if not context['google_accounts'].get_current_user():
                raise web.notfound()
            context['form'] = form()
            context['add_or_edit'] = True
        else:
            context['add_or_edit'] = False
            context['content'] = self.content
        context['page_path'] = '/'+name
        if action == 'edit':
            form = form()
            form.get('position').value = self.content.position
            form.get('name').value = self.content.name
            form.get('label').value = self.content.label
            form.get('title').value = self.content.title
            form.get('content').value = self.content.content
            form.get('active').value=self.content.active
            context['form'] = form

    def GET(self, name, action='view'):
        self.init_data(name, action)
        return render_template('static_content.html', **context)
    @admin_perm_required
    def POST(self, name, action='view'):
        self.init_data(name, action)
        form = self.form_class()
        if form.validates():
            active = True if form.get('active').value else False
            static_data = Static(position=int(form.get('position').value),
                                 name=form.get('name').value.lstrip('/'),
                                 label=form.get('label').value,
                                 title=form.get('title').value,
                                 content=form.get('content').value,
                                 active=active,)
            static_data.put()
            return web.seeother('/'+static_data.name, absolute=True)
        context['form'] = form
        return render_template('static_content.html', **context)

#urls
mapper = ('/', 'index',
          '/post/add', 'add_edit',
          '/post/(.*)-(\d+)', 'view',
          '/post/.*-(\d+)/(edit)', 'add_edit',
          '/blog/feeds', 'feed_server',
          '/(\w+)/(edit)', 'static_content',
          '/(\w+)', 'static_content',)
    
def default_loadhook():
    from utils.track_request import TrackRequest
    
    TrackRequest(web)
    web.google_accounts = users
    context['google_accounts'] = users
    
    context['static_pages'] = Static.all().filter('position <', 15)\
        .filter('active =', True).order('position')

app = web.application(mapper, globals())
app.add_processor(web.loadhook(default_loadhook))

if __name__ == "__main__":
    main = app.cgirun()
    
