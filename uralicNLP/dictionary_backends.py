from tinydb import TinyDB, Query

class TinyDictionary(object):
	"""docstring for TinyDictionary"""
	def __init__(self, path):
		self.db = TinyDB(path)

	def find(self, word, lemmas):
		results = {"lemmatized":[]}
		results['exact_match'] = self._lemma_query(word)
		for lemma in lemmas:
			results["lemmatized"].append(self._lemma_query(lemma))
		results["other_languages"] = self._lang_query(word)
		return results

	def _lemma_query(self, lemma):
		E = Query()
		res = self.db.search(E.lg.l["#text"] == lemma)
		return res

	def _lang_query(self, lemma):
		E = Query()
		T = Query()
		W = Query()
		res1 = self.db.search(E.mg.tg.any(T.t.any(W["#text"] == lemma)))
		res2 = self.db.search(E.mg.tg.any(T.t["#text"] == lemma))
		res3 = self.db.search(E.mg.tg.t["#text"] == lemma)

		return res1 + res2 +res3

				



