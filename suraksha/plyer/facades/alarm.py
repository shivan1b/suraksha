'''
Alarm
=====

The :class: `Alarm` provides access to public methods to use alarm of the device.


Examples
--------

To set the alarm::
    
    >>> from plyer import alarm
    >>> alarm.set()
'''


class Alarm(object):
    """
    Alarm facade.
    """

    def set(self):
        """
        Set the Alarm
        """
        self._set()

    # private

    def _set(self):
        raise NotImplementedError()
