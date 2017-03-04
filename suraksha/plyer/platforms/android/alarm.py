"""
Alarm
-----
"""

from plyer.facades import Alarm
from jnius import autoclass
from plyer.platforms.android import activity

Activity = autoclass('org.renpy.android.PythonActivity').mActivity
#Alarm = autoclass("android.app.AlarmManager")
AlarmClock = autoclass("android.provider.AlarmClock")
Intent = autoclass("android.content.Intent")
Context = autoclass("android.content.Context")
#PendingIntent = autoclass("android.app.PendingIntent")
'''from android.broadcast import BroadcastReceiver
'''
class AndroidAlarm(Alarm):
    _alarm = None

    '''def on_broadcast(*args):
        print *args, '<<<<<<'
'''
    def _set(self):

        if not self._alarm:
            return

        self._alarm = Activity.getSystemService(Context.ALARM_SERVICE)
        self._context = Activity.getApplicationContext()
        self._intent = Intent(Intent.ACTION_SET_ALARM)
        self_intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_MULTIPLE_TASK)
        self._intent.putExtra(AlarmClock.EXTRA_MESSAGE, "My Alarm"); 
        self._intent.putExtra(AlarmClock.EXTRA_HOUR, 11); 
        self._intent.putExtra(AlarmClock.EXTRA_MINUTES, 20);
        self._context.startActivity(self._intent)
        '''if not self.br:
            self.br = BroadcastReceiver(self.on_broadcast,  actions=['provider_changed',])
        br.start()
        self._pi = PendingIntent.getBroadcast(Activity, 0, self._intent, PendingIntent.FLAG_UPDATE_CURRENT)

        self._alarm.set(Alarm.RTC_WAKEUP, 5000, _pi)
        '''

def instance():
    return AndroidAlarm()
