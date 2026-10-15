try:
	from onmt_runner import Translator
except:
	Translator = None
import os
class NatasNotInstalled(Exception):
	pass

class NeuralFST(object):
	"""docstring for NeuralFST"""
	def __init__(self, model_path):
		if Translator is None:
			raise NatasNotInstalled("onmt-runner is needed for neural models, run:\n\npip install onmt-runner")
		
		self.model_path = model_path
		self.models = {}
	
	def analyze(self, word, n_best=1):
		if len(word) == 0:
			return []
		model_a = os.path.join(self.model_path, "analyzer.pt")
		model_l = os.path.join(self.model_path, "lemmatizer.pt")
		tags = self.call_onmt([" ".join(word)] ,model_a,n_best=n_best,return_scores=True)[0]
		lemma = self.call_onmt([" ".join(word)], model_l,n_best=n_best,return_scores=True)[0]
		lem_tags = zip(tags, lemma)
		return [(l[0].replace(" ","") + "+" + t[0].replace(" ","+"), l[1] + t[1]) for t,l in lem_tags ]

	def generate(self, word, n_best=1):
		if len(word) ==0:
			return []
		model_g = os.path.join(self.model_path, "generator.pt")
		parts = word.split("+")
		parts[0] = " ".join(parts[0])
		forms =  self.call_onmt([" ".join(parts)] ,model_g, n_best=n_best,return_scores=True)[0]
		return [(form.replace(" ", ""), score) for form, score in forms]

	def _load_model(self, model_path):
		m = Translator.load(model_path)
		self.models[model_path] = m

	def _give_model(self, name):
		if name not in self.models:
			self._load_model(name)
		return self.models[name]

	def _split_words(self, words):
		return [" ".join(x.lower()) for x in words]

	def call_onmt(self, words, model_name, n_best=10, return_scores=False):
		model = self._give_model(model_name)
		tss = model.translate_many(words, n_best=n_best, return_scores=return_scores)
		res = []
		for ts in tss:
			if not isinstance(ts, list):
				ts = [ts]
			if return_scores is True:
				res.append([[t.text, t.score] for t in ts])
			else:
				res.append(ts)
		return res
