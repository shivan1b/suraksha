from plyer.facades import NetCheck
import urllib2

class LinuxNetCheck(NetCheck):

    def _isconnected(self):
        for timeout in [1,3,5]:
            try:
                response=urllib2.urlopen('http://google.com',timeout=timeout)
                print response
                return True
            except urllib2.URLError as err: pass
        return False


def instance():
    return LinuxNetCheck()