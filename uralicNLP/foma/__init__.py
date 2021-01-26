try:
	from . import foma
except:
	foma = None
import warnings

arabic_clitics = {"art":{"ال":["ال"]}, "prep":{"ب":["بِ"], "ل":["لِ","لَ"], "ت": ["تَ"], "ك":["كَ"], "س":["سَ"]}, "conj":{"ف":["فَ"], "و":["وَ"]}}

arabic_vowels = "َ"

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
		if "\"" in filename:
			s = "\""
		else:
			s = "/"
		file_split = filename.split(s)
		if len(file_split) > 2 and file_split[-2] == "ara":
			self.arab = True
		else:
			self.arab = False
			

	def generate(self, query):
		if self.arab:
			return self._arab_generate(query)
		return self._dummy_weights(self.foma.apply_down(query))

	def analyze(self, query):
		if self.arab:
			return self._arab_analyze(query)
		return self._dummy_weights(self.foma.apply_up(query))

	def _arabic_trim_vowel(self, word):
		for x in arabic_vowels:
			if word.startswith(x):
				word = word[1:]
		return word

	def _add_to_arab_results(self, results, voweled_prefixes):
		res = []
		if voweled_prefixes is None:
			return results
		for vp in voweled_prefixes:
			res.extend([vp + "#" + x[0] for x in results])
		return res
	def _arab_analyze(self, query, recurse=True):
		res = []
		if recurse:
			word = query
			set_conj = None
			set_prep = None
			for conj, voweled in arabic_clitics["conj"].items():
				if word.startswith(conj) and word is not conj:
					set_conj = voweled
					word = self._arabic_trim_vowel(word[len(conj):])
					res.extend( self._add_to_arab_results( self._arab_analyze(word, recurse=False), set_conj ) )
					break
			for prep, voweled in arabic_clitics["prep"].items():
				if word.startswith(prep) and word is not prep:
					set_prep = voweled
					word = self._arabic_trim_vowel(word[len(prep):])
					res.extend( self._add_to_arab_results(self._add_to_arab_results( self._arab_analyze(word, recurse=False), set_prep ), set_conj) )
					break
			for art, art_voweled in arabic_clitics["art"].items():
				if word.startswith(art) and art is not word:
					word = self._arabic_trim_vowel(word[len(art):])
					res.extend( self._add_to_arab_results(self._add_to_arab_results(self._add_to_arab_results( self._arab_analyze(word, recurse=False), art_voweled ), set_prep), set_conj))
					break
		res.extend(self.foma.apply_up(query))
		res = list(set(res))
		return self._dummy_weights(res)

	def _arab_generate(self, query, recurse=True):
		return self._dummy_weights(self.foma.apply_down(query))

	def _dummy_weights(self, res):
		res = list(res)
		return [(x, 0.0) for x in res]

	def convert(self, *args, **kwargs):
		warnings.warn("Conversion not supported by Foma based transducers")
