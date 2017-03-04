'''Pure pytohn impl of social authentication'''

from plyer.facades import Social
from plyer import netcheck
from .libs.social import social_providers
import os.path
from .libs.social.request_handler import AuthHandler
import webbrowser

class Authorize(Social):
    '''
    Authenticates the user based on the choice of social accounts.
    OAuth 1 is being used by Twitter.
    OAuth 2 is used by Google and Facebook.
    '''

    def __init__(self, **kwargs):
        '''
        Local variable initialization
        '''
        self.server = None

        self.social = ''
        '''This variable can be one of the providers from
        plyer.platforms.common.socialproviders.providers`

        Type: String
        Default value: ''
        '''
        self.oauth = None
        '''Stores the session for Twitter
        '''
        self.client_id = ''
        '''This has to be the Client ID generated for app on
        particular social platform.

        Type: String
        Default value: ''
        '''
        self.client_secret = ''
        '''The Client secret which is generated alongwith Client ID.

        Type: String
        Default value: ''
        '''

        self.token_dir = './'
        '''Directory where token needs to be saved.

        Type: String
        Default value: './'
        '''
        
        super(Authorize, self).__init__()

    
    def _authenticate(self, social='', client_id='', client_secret='',
        token_dir='./', callback=None):
        '''
        Call the appropriate authorization method based
        on the social account required.

        Parameters::
            social:
                Type: String
                Function: social contains the value of social account to be
                          authenticated
            client_id:
                Type: String
                Function: Client ID is needed by the social auth end to identify
                          the application
            client_secret:
                Type: String
                Function: Client secret is required for successful
                          identification of the app
            token_dir:
                Type: String
                Function: Should have the path where access tokens are to be
                          stored

        '''

        self.social = getattr(social_providers, social)
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_dir = token_dir
        self.callback = callback

        # Check if the token directory and hence the token already exists
        if self._is_authenticated(self.token_dir):
            return

        # Twitter is still using OAuth 1
        if not netcheck.isconnected():
            return

        if social == 'Twitter':
            self.Social_OAuth1()
        else:
            self.Social_OAuth2()



    def Social_OAuth1(self):
        '''
        Authenticates Twitter using OAuth 1.0
        '''
        from requests_oauthlib import OAuth1Session

        oauth = OAuth1Session(
            client_key=self.client_id,
            client_secret=self.client_secret)
        fetch_response = oauth.fetch_request_token(
            self.social.request_token_url)
        resource_owner_key = fetch_response.get('oauth_token')
        resource_owner_secret = fetch_response.get('oauth_token_secret')

        authorization_url = oauth.authorization_url(
            self.social.base_authorization_url)
        self.get_response(authorization_url, oauth)

    
    def Social_OAuth2(self):
        '''
        Authenticates Google and Facebook using OAuth 2
        '''

        from requests_oauthlib import OAuth2Session
        if self.social.__name__ == 'Google':
            session = OAuth2Session(
                self.client_id,
                scope=self.social.scope, 
                redirect_uri=self.social.redirect_uri)
        elif self.social.__name__ == 'Facebook':
            from requests_oauthlib.compliance_fixes import facebook_compliance_fix

            session = OAuth2Session(
                self.client_id, 
                redirect_uri=self.social.redirect_uri)
            session = facebook_compliance_fix(session)

        authorization_url, state = session.authorization_url(
            self.social.base_authorization_url)     
        self.get_response(authorization_url, session)

        
    def _is_authenticated(self, token_dir):
        '''
        Returns True if the social account is already authenticated,
        False otherwise.
        '''
        self.token_dir = token_dir
        if os.path.exists(token_dir + '/.token.json'):
            return True
            
        return False


    def _logout(self):
        if not netcheck.isconnected():
            return
        if not self._is_authenticated(self.token_dir):
            return
        os.unlink(self.token_dir + '/.token.json')


    def get_response(self, auth_url, sess):
        '''
        Gets the response from the social account after having provided the
        bearer token.
        The request and response are handled by plyer.platforms.common.handler
        '''
        import BaseHTTPServer
        from BaseHTTPServer import BaseHTTPRequestHandler

        AuthHandler.TOKEN_FILE = self.token_dir

        if self.social.__name__ == 'Twitter':
            AuthHandler.session = sess
            AuthHandler.client_id = self.client_id
        else:
            AuthHandler.session = sess
            AuthHandler.client_secret = self.client_secret

        webbrowser.open(auth_url) # Monkey patched webbrowser
        # Server is going to listen on localhost port 8080
        print "Going to server", "s"*90
        print "server val", self.server, "l"*90
        if self.server:
            return 

        self.server = BaseHTTPServer.HTTPServer(('', 8080), AuthHandler)
        print "Server started", "0"*90
        # Server should be run on a different thread
        import threading            

        def serve_till(*args):
            import requests.packages.urllib3
            requests.packages.urllib3.disable_warnings()
            try:
                AuthHandler.stop_serving = False 
                while not AuthHandler.stop_serving:
                    self.server.handle_request()
            except Exception as err:
                print err
            print 'callback....'
            self.callback()
            import jnius
            print 'calling detach....'
            # Setting server to None to avoid binding of server 
            # in current thread to port 8080 and hence avoid socket error
            self.server = None
            jnius.detach()
        thread = threading.Thread(target=serve_till)
        thread.daemon = True
        thread.start()


def instance():
    return Authorize()

