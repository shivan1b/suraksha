'''
Social
======

The :class: `Social` provides access to authorize the social accounts
namely, Facebook, Google and Twitter.

Examples
--------

To authenticate a social account::

    >>> from plyer import social
    >>> social.authenticate(social='Facebook',
    ...     client_id=<client_id>,
    ...     client_secret=<client_secret>,
    ...     token_dir=<token_dir>,
    ...     callback=<callback_func>)
'''


class Social(object):
    '''
    Social facade.
    '''

    def authenticate(self, social='', client_id='', client_secret='',
        token_dir='./', callback=None):
        '''
        Authenticate the social provider
        Args::
            social:
                Contains the name of social provider
                plyer.platforms.common.socialproviders
                Type: String

            client_id:
                Client ID for app corresponding to social provider
                Type: String

            client_secret:
                Client secret for app generated alongwith Client ID
                Type: String

            token_dir:
                Directory where the access tokens are to be stored
                Type: String
        '''
        return self._authenticate(social=social, client_id=client_id,
            client_secret=client_secret, token_dir=token_dir, callback=callback)

    def _authenticate(self, social, client_id, client_secret, token_dir,
        callback):
        raise NotImplementedError()

    def is_authenticated(self, token_dir):
        '''
        Check if the app has already been authenticated.
        This is irrespective of the social account with which the app
        was authenticated. 
        '''
        return self._is_authenticated(token_dir)

    def _is_authenticated(self, token_dir):
        raise NotImplementedError()

    def logout(self):
        return self._logout()

    def _logout(self):
        raise NotImplementedError()
