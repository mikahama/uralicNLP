from tinydb import TinyDB, Query
import argparse
import os

try:
	from pymongo import MongoClient
except:
	pass

class EmptyDatabaseException(Exception):
    """Base class for exceptions in this module."""
    pass

class DictionaryInterface(object):
	"""docstring for DictionaryInterface"""
	def __init__(self, path, language):
		self.path = path
		self.language = language

	def find(self, word, lemmas):
		results = {"lemmatized":[]}
		results['exact_match'] = self._lemma_query(word)
		for lemma in lemmas:
			results["lemmatized"].append(self._lemma_query(lemma))
		results["other_languages"] = self._lang_query(word)
		return results

	def lemmas(self, group_by_pos=False):
		if group_by_pos:
			return self._list_lemmas_by_pos()
		else:
			return self._list_lemmas()

	def _list_lemmas(self):
		data = self._get_all()
		lems = []
		for l in data:
			try:
				lem = l["lg"]["l"]["#text"]
				lems.append(lem)
			except:
				pass
		return list(set(lems))

	def _list_lemmas_by_pos(self):
		data = self._get_all()
		lems = {}
		for l in data:
			try:
				lem = l["lg"]["l"]["#text"]
				pos = l["lg"]["l"]["@pos"]
				if pos not in lems:
					lems[pos] = []
				lems[pos].append(lem)
			except:
				pass
		for k in list(lems.keys()):
			lems[k] = list(set(lems[k]))
		return lems

	def _lemma_query(self, lemma):
		return []

	def _lang_query(self, lemma):
		return []

	def _get_all(self):
		return []

	def import_data(self):
		pass

class TinyDictionary(DictionaryInterface):
	"""docstring for TinyDictionary"""
	def __init__(self, path, language):
		if not os.path.isfile(path):
			raise EmptyDatabaseException("No dictionary.json available in " + path +"\nRunning uralicApi.download('"+language+"') may fix this if there is a dictionary available")
		self.db = TinyDB(path)

		if len(self.db) == 0:
			raise EmptyDatabaseException("The dictionary is empty for " + language + " in path " + path)
		super(TinyDictionary, self).__init__(path, language)

	def _get_all(self):
		return self.db.all()


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


class MongoDictionary(DictionaryInterface):
	"""docstring for MongoDictionary"""
	def __init__(self, path, language):
		client = MongoClient()
		self.db = client['uralicNLP_dicts']
		self.collection = self.db[language]
		self.empty = self.collection.count_documents({}) == 0
		super(MongoDictionary, self).__init__(path, language)

	def _get_all(self):
		self._check_empty()
		return self.collection.find()


	def _lemma_query(self, lemma):
		self._check_empty()
		res = self.collection.find({ "lg.l.#text" : lemma})
		return list(res)

	def _lang_query(self, lemma):
		self._check_empty()
		res = self.collection.find(
			{ "$or": [
		            { "mg.tg": { "$elemMatch": { "t": {"$elemMatch": {"#text": lemma }  } } } },
		            { "mg.tg.t.#text": lemma }
		        ]
		    }
		)

		return list(res)

	def _check_empty(self):
		if self.empty:
			raise EmptyDatabaseException("The dictionary database for '" + self.language + "' is empty.\nRun uralicApi.import_dictionary_to_db('" + self.language + "') first")


	def import_data(self):
		if not self.empty:
			self.collection.drop()
			self.collection = self.db[self.language]
		tiny = TinyDictionary(self.path, self.language)
		data = tiny._get_all()
		self.collection.insert_many(data)
		self.empty = self.collection.count_documents({}) == 0





