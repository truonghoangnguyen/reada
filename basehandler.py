# *-* coding: UTF-8 *-*

# standard library imports
import logging
# related third party imports
import webapp2
from webapp2_extras import jinja2
from webapp2_extras import auth
from webapp2_extras import sessions



def generate_csrf_token():
    session = sessions.get_store().get_session()
    if '_csrf_token' not in session:
        session['_csrf_token'] = utils.random_string()
    return session['_csrf_token']


def jinja2_factory(app):
    j = jinja2.Jinja2(app)
    j.environment.filters.update({
        # Set filters.
        # ...
    })
    j.environment.globals.update({
        # Set global variables.
        'csrf_token': generate_csrf_token,
        'uri_for': webapp2.uri_for,
        'getattr': getattr,
        'str': str,
    })
    j.environment.tests.update({
        # Set test.
        # ...
    })
    return j




class BaseHandler(webapp2.RequestHandler):
    """
        BaseHandler for all requests

        Holds the auth and session properties so they
        are reachable for all requests
    """

    def __init__(self, request, response):
        """ Override the initialiser in order to set the language.
        """
        self.initialize(request, response)
        #self.locale = i18n.set_locale(self)
        #self.view = ViewClass()

    def dispatch(self):
        """
            Get a session store for this request.
        """
        self.session_store = sessions.get_store(request=self.request)

        try:
            # csrf protection
            if self.request.method == "POST" and not self.request.path.startswith('/taskqueue'):
                token = self.session.get('_csrf_token')
                if not token or token != self.request.get('_csrf_token'):
                    self.abort(403)

            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()

    @webapp2.cached_property
    def session_store(self):
        return sessions.get_store(request=self.request)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    @webapp2.cached_property
    def messages(self):
        return self.session.get_flashes(key='_messages')

    def add_message(self, message, level=None):
        self.session.add_flash(message, level, key='_messages')

    @webapp2.cached_property
    def auth_config(self):
        """
              Dict to hold urls for login/logout
        """
        return {
            'login_url': self.uri_for('login'),
            'logout_url': self.uri_for('logout')
        }

    @webapp2.cached_property
    def language(self):
        return str(Locale.parse(self.locale).language)

    @webapp2.cached_property
    def user(self):
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user_id(self):
        return str(self.user['user_id']) if self.user else None

    @webapp2.cached_property
    def user_key(self):
        if self.user:
            user_info = models.User.get_by_id(long(self.user_id))
            return user_info.key
        return None

    @webapp2.cached_property
    def username(self):
        if self.user:
            try:
                user_info = models.User.get_by_id(long(self.user_id))
                if not user_info.activated:
                    self.auth.unset_session()
                    self.redirect_to('home')
                else:
                    return str(user_info.username)
            except AttributeError, e:
                # avoid AttributeError when the session was delete from the server
                logging.error(e)
                self.auth.unset_session()
                self.redirect_to('home')
        return None

   

    @webapp2.cached_property
    def current_user(self):
        user = self.auth.get_user_by_session()
        if user:
            return models.User.get_by_id(user['user_id'])
        return None

    @webapp2.cached_property
    def is_mobile(self):
        return utils.set_device_cookie_and_return_bool(self)

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(factory=jinja2_factory, app=self.app)

   
    def render_template(self, filename, **kwargs):              
        self.response.headers.add_header('X-UA-Compatible', 'IE=Edge,chrome=1')
        self.response.write(self.jinja2.render_template(filename, **kwargs))