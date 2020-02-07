try:
	from . import foma
except:
	foma = None
import warnings



class FomaFSTWrapper(object):
	"""docstring for FomaFSTWrapper"""
	def __init__(self, filename, invert):
		if foma is None:
			raise Exception("Foma (libfoma) is not installed or the version is too old, please refer to https://fomafst.github.io/")
		self.foma = foma.FST.load(filename)
		if invert:
			self.lookup = self.generate
		else:
			self.lookup = self.analyze

	def generate(self, query):
		return self._dummy_weights(self.foma.apply_down(query))

	def analyze(self, query):
		return self._dummy_weights(self.foma.apply_up(query))

	def _dummy_weights(self, res):
		res = list(res)
		return [(x, 0.0) for x in res]

	def convert(self, *args, **kwargs):
		warnings.warn("Conversion not supported by Foma based transducers")
