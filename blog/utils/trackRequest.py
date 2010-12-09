from utils.models import Tracker


class TrackRequest:
    """
    Tracks requests to the application
    """
    def __init__(self, web):
        #just populating the object with the request client's info
        self.user_ip =  web.ctx.env['REMOTE_ADDR']
        self.user_agent = unicode(web.ctx.env.get('HTTP_USER_AGENT'), 'utf-8')
        self.user_agent_opera = unicode(web.ctx.env.get('HTTP_X_OPERAMINI_PHONE_UA', ''), 'utf-8')
        self.path =   unicode(web.ctx.env.get('PATH_INFO', 'unknown'), 'utf-8')
        self.referer = unicode(web.ctx.env.get('HTTP_REFERER', 'unknown'), 'utf-8')
        
        self._log_request()
        
    def _log_request(self):
        """Stores the some information about the request"""
        session_log = Tracker(path=self.path,
                              referer=self.referer,
                              user_agent=self.user_agent,
                              user_agent_opera=self.user_agent_opera,
                              user_ip=self.user_ip,)
        session_log.put()
