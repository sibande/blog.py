import web


def admin_perm_required(f):
    def deco(self, *args, **kw):
        if not web.google_accounts.is_current_user_admin():
            return web.seeother('/', absolute=True)
        return f(self, *args, **kw)
    return deco
