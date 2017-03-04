'''
Implements authentication for social accounts on Android.

Currently this just calls the linux facade as it is pure python
and should work everywhere.
'''

from plyer.platforms.linux.libs.social.request_handler import AuthHandler
import webbrowser

import ios

def _webopen(*args, **kwargs):
    ioswv = ios.IOSWebView()
    ioswv.open(args[0])
    return True

webbrowser.open = _webopen

from plyer.platforms.linux.social import Authorize as LinuxAuthorize

class Authorize(LinuxAuthorize):

    def _authenticate(self, *args, **kwargs):
        try:
            import requests
            super(Authorize, self)._authenticate(*args, **kwargs)
        except requests.exceptions.RequestException:
            activity.toastError('Limited Connectivity!')

def instance():
    return Authorize()
