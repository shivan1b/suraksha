



class NetCheck(object):

	def isconnected(self):
		return self._isconnected()

	def _isconnected(self):
		raise NotImplementedError()