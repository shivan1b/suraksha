from jnius import autoclass
from plyer.facades import NetCheck
from android.runnable import run_on_ui_thread

activity = autoclass('org.renpy.android.PythonActivity').mActivity

import os

class AndroidNetCheck(NetCheck):

    #@run_on_ui_thread
    def _isconnected(self):
        Context = autoclass('android.content.Context')
        #ConnectivityManager = autoclass('android.net.ConnectivityManager')
        ConnectivityManager = activity.getSystemService(Context.CONNECTIVITY_SERVICE)
        #NetworkInfo = autoclass('android.net.NetworkInfo')
        ActiveNetworkInfo = ConnectivityManager.getActiveNetworkInfo()
        vard = ActiveNetworkInfo is not None
        if vard:
            vard = ActiveNetworkInfo.isConnectedOrConnecting()
        
    #internet = check_internet()
    #print internet, "m"*80

        if not vard:
            print "No internet", "*"*50
            activity.toastError('No Internet!')
        print 'returning', vard

        return vard

def instance():
    return AndroidNetCheck()