'''
Implements authentication for social accounts on Android.

Currently this just calls the linux facade as it is pure python
and should work everywhere.
'''

from plyer.platforms.linux.libs.social.request_handler import AuthHandler
import webbrowser
from jnius import autoclass
from android.runnable import run_on_ui_thread

WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.renpy.android.PythonActivity').mActivity

import os

@run_on_ui_thread
def initiate_webview():
    webview = WebView(activity)
    webbrowser._webview = webview
    webbrowser._view_cached = activity.getCurrentFocus()
    settings = webbrowser._webview.getSettings()
    settings.setJavaScriptEnabled(True)
    settings.setUseWideViewPort(True) # enables viewport html meta tags
    settings.setLoadWithOverviewMode(True) # uses viewport
    settings.setSupportZoom(True) # enables zoom
    settings.setBuiltInZoomControls(True) # enables zoom controls
    wvc = WebViewClient()
    webbrowser._webview.setWebViewClient(wvc)
        
initiate_webview()

def _webopen(*args, **kwargs):
    #print '9'*90
    @run_on_ui_thread
    def webopen(*args, **kwargs):
        # open webview here
        url = args[0]
        webview = webbrowser._webview
        webview.resumeTimers()
        webview.clearHistory()
        webview.loadUrl("about:blank")
        webview.clearCache(True)
        webview.freeMemory()
        activity.setContentView(webview)
        webbrowser._webview.loadUrl('{}'.format(url))
        webbrowser._opened = True   

    webopen(*args, **kwargs)
    return True

@run_on_ui_thread
def close(*args):
    if not webbrowser._webview:
        print "no_webview"*20
        return

    wv = webbrowser._webview
    wv.clearHistory()
    wv.clearCache(True)
    wv.loadUrl("about:blank")
    print 'abt bank'*3
    wv.freeMemory()
    print 'free mem'*3
    wv.pauseTimers()
    print 'pause timers'*3
    activity.setContentView(webbrowser._view_cached)
    webbrowser._opened = False
    print 'opened false'*3
    AuthHandler.stop_serving = True
    print 'out'*7


webbrowser.open = _webopen
webbrowser.close = close


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
