'''
Handle the successful authentication of social accounts and their redirection.

Import:
------
from plyer.platforms.common.handler import AuthHandler

Currently handled routes:
------------------------
/               : for testing
/login/google   : for logging into Google account
/login/facebook : for logging into Facebook account
/login/twitter  : for logging into Twitter account
'''

ENCODING_UTF8 = 'utf-8'

import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from urlparse import urlparse, parse_qsl
from . import social_providers
from .social_providers import *



class AuthHandler(BaseHTTPRequestHandler):
    '''
    Class for handling authentication process for different providers
    '''

    session = None
    '''Stores the session created for authenticating the app

    Type: 
    Default value: None
    '''    

    client_id = None
    '''The Client ID generated for app on particular social platform.

    Type: String
    Default value: None
    '''
    
    client_secret = None
    '''The Client secret which is generated alongwith Client ID.

    Type: String
    Default value: None
    '''

    TOKEN_FILE = None
    '''Directory where token needs to be/ is already saved.

    Type: String
    Default value: None
    '''

    def __init__(self, *args, **kwargs):
        '''
        Intializing local variables
        '''
        
        self.provider = None
        '''Provider that we're dealing with.
        See the currently supported providers in
         libs/social_providers

        Provider is a String Defaults to None
        '''
        
        self.route_handlers = {
            '/': 'handle_root',
            '/login/google' : 'handle_google',
            '/login/facebook': 'handle_facebook',
            '/login/twitter': 'handle_twitter'
        }
        '''Dictionary containing handlers corresponding to different social
        providers.

        Type: Dictionary
        Default value: 
        '''

        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)


    def _get_token(self, provider, tokenurl):
        redirect_response = 'https:' + self.provider.redirect_uri.split(':',1)[1] + tokenurl
        token = AuthHandler.session.fetch_token(
            self.provider.access_token_url,
            client_secret=AuthHandler.client_secret,
            authorization_response=redirect_response)

        return token


    def get_token(self, provider, data):
        '''
        Method to get the access token by sending the 'code' and 'state' in data
        to the provider.
        '''
        print provider
        self.provider = getattr(social_providers, provider)
        from requests_oauthlib import OAuth1Session

        if not netcheck.isconnected():
            return
            
        if provider == 'Twitter':
            TOKEN_URL = '?oauth_token=' + data['oauth_token'] + '&oauth_verifier=' + data['oauth_verifier']
            redirect_response = 'https:' + self.provider.redirect_uri.split(':',1)[1] + TOKEN_URL
            oauth_response = self.session.parse_authorization_response(
                redirect_response)
            verifier = oauth_response.get('oauth_verifier')
            oauth = OAuth1Session(client_key=AuthHandler.client_id,
                client_secret=AuthHandler.client_secret,
                resource_owner_key=data['oauth_token'],
                resource_owner_secret=data['oauth_verifier'], verifier=verifier)
            token = oauth.fetch_access_token(self.provider.access_token_url)
        elif provider == 'Facebook':
            TOKEN_URL = '?code=' + data['code'] + '&state=' + data['state']
            token = self._get_token(provider, TOKEN_URL)     
        elif provider == 'Google':
            TOKEN_URL = '?state=' + data['state'] + '&code=' + data['code']
            token = self._get_token(provider, TOKEN_URL)
        
        return token
     

    def save_token(self, token, name):
        '''
        Method to save the access token in json format in a directory
        specified by user (stored in TOKEN_FILE).
        '''
        import os
        import json

        with open(os.path.join(AuthHandler.TOKEN_FILE, '.token.json'), 'w+') as f:
            json.dump(token, f)


    def do_GET(self):
        '''
        Method to get the appropriate handler as per the query of redirect uri
        from route_handlers.
        '''
        url = urlparse(self.path)
        print url
        if url.path in self.route_handlers:
            print url.path
            getattr(self, self.route_handlers[url.path])(
            dict(parse_qsl(url.query)))
        else:
            self.send_response(404)


    def success(func):
        '''
        Decorator for event of success.
        Send response 200 on success.
        '''
        def wrapper(self, *args, **kwargs):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.log_message(self.path)
            self.end_headers()
            return func(self, *args, **kwargs)
        return wrapper


    @success
    def handle_root(self ,data):
    	'''
        Handling root (for testing purpose)
        '''
    	self.wfile.write("You have successfully logged in. "
                         "You can close this window.")

    def close_web(self, social_provider):
        print "closing web"
        self.wfile.write(
            "You have successfully logged in to {}. ".format(social_provider)+\
            "You can close this window.")
        import webbrowser
        if hasattr(webbrowser, 'close'):
            webbrowser.close()
    
        AuthHandler.stop_serving = True


    @success
    def handle_facebook(self ,data):
        '''
        Handling Facebook
        '''
        tokenfilename = 'Facebook'
        token = self.get_token(tokenfilename, data)
        self.save_token(token, tokenfilename)
        self.close_web(tokenfilename)


    @success
    def handle_google(self ,data):
        '''
        Handling Google
        '''
        tokenfilename = 'Google'
        token = self.get_token(tokenfilename, data)
        print "Got token"
        self.save_token(token, tokenfilename)
        print "Savedd token"
        self.close_web(tokenfilename)


    @success
    def handle_twitter(self ,data):
    	'''
        Handling Twitter
        '''
        tokenfilename = 'Twitter'
        token = self.get_token(tokenfilename, data)
        self.save_token(token, tokenfilename)
        self.close_web(tokenfilename)
