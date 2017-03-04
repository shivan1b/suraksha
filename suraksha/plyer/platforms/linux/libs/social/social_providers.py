'''
Lists the different social providers supported by the auth module currently.

Supported social providers:
--------------------------
1. Facebook - OAuth 2
2. Google   - OAuth 2
3. Twitter  - OAuth 1

Fields common to all classes:
----------------------------
redirect_uri           : where service should redirected after getting auth code
base_authorization_url : authorization URL corresponding to the social platform
access_token_url       : URL to retrieve the access token from provider
'''

__all__ = ['Facebook', 'Google', 'Twitter']


class Facebook():
    '''
    Facebook 
    '''
    redirect_uri = 'http://localhost:8080/login/facebook'
    base_authorization_url = 'https://www.facebook.com/dialog/oauth'
    access_token_url = 'https://graph.facebook.com/oauth/access_token'


class Google():
    '''
    Google
    '''
    redirect_uri = 'http://localhost:8080/login/google'
    scope = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"
            ]
    base_authorization_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    access_token_url = 'https://www.googleapis.com/oauth2/v4/token'


class Twitter():
    '''
    Twitter
    '''
    redirect_uri = 'http://localhost:8080/login/twitter'
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    access_token_url = 'https://api.twitter.com/oauth/access_token'


#If adding a new provider, please update the list below else the code would fail
providers = ['Facebook', 'Google', 'Twitter']


