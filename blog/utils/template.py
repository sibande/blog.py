import datetime

def markdown(content, safe="unsafe"):
    """Format and highlight text"""
    from markdown import markdown
    if safe == "unsafe":
        safe = False
    else:
        safe = True
    return markdown(content, ['codehilite',], safe,)


template_tags = {'markdown': markdown}

def render_template(template_name, **context):

    import os
    from jinja2 import Environment,FileSystemLoader

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
