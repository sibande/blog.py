# -*- coding: utf-8 -*-

def admin_perm_required(f):
    import web

    def deco(self, *args, **kw):
        if not web.google_accounts.is_current_user_admin():
            return web.seeother('/', absolute=True)
        return f(self, *args, **kw)
    return deco


def markdown(content, safe="unsafe"):
    """Format and highlight text"""
    from markdown import markdown

    if safe == "unsafe":
        safe = False
    else:
        safe = 'escape'
    content = markdown(content, ['codehilite',], safe,)
    return content
    
def datetimeformat(value, format='%d %B, %Y at %H:%M%p'):
    return value.strftime(format)



def render_template(template_name, **context):

    import os
    import datetime
    from jinja2 import Environment,FileSystemLoader

    template_tags = {
        'markdown': markdown,
        'datetimeformat': datetimeformat,
    }

    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(
                    os.path.dirname(__file__)), 'templates')),
            extensions=['jinja2.ext.autoescape'],
            )
    for v, k in template_tags.iteritems():
        jinja_env.filters[v] = k

    jinja_env.globals.update(globals)

    #jinja_env.update_template_context(context)
    return jinja_env.get_template(template_name).render(context)
