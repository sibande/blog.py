from google.appengine.ext import db

class Tracker(db.Model):
    """Used to log every request to the application"""
    path = db.StringProperty()
    referer = db.StringProperty()
    user_agent = db.StringProperty()
    user_agent_opera = db.StringProperty()
    user_ip = db.StringProperty()
    datetime = db.DateTimeProperty(auto_now_add=True)
