from google.appengine.ext import db


class Post(db.Model):
    """Stores all blog posts"""
    title = db.StringProperty(required=True)
    slug = db.StringProperty()
    body = db.TextProperty(required=True)
    active = db.BooleanProperty()
    udatetime = db.DateTimeProperty(auto_now=True)
    datetime = db.DateTimeProperty(auto_now_add=True)

    def before_put(self):
        """Flask.pocoo Slug code snippet"""
        import re
        from unicodedata import normalize

        _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
        
        def slugify(text, delim=u'-'):
            """Generates an slightly worse ASCII-only slug."""
            result = []
            for word in _punct_re.split(text.lower()):
                word = normalize('NFKD', word).encode('ascii', 'ignore')
                if word:
                    result.append(word)
            return unicode(delim.join(result))
        self.slug = slugify(self.title)

    def put(self, **kwargs):
        self.before_put()
        super(Post, self).put(**kwargs)

class Comment(db.Model):
    """Comments model"""
    post = db. ReferenceProperty(Post)
    name = db.StringProperty(required=True)
    url = db.StringProperty()
    email = db.StringProperty(required=True)
    active = db.BooleanProperty()
    body = db.TextProperty(required=True)
    datetime = db.DateTimeProperty(auto_now_add=True)


class Static(db.Model):
    position = db.IntegerProperty()
    name = db.StringProperty(required=True)
    label = db.StringProperty()
    title = db.StringProperty()
    content = db.TextProperty(required=True)
    active = db.BooleanProperty()
    datetime = db.DateTimeProperty(auto_now_add=True)
