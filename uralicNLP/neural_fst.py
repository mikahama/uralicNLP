try:
	from natas.normalize import call_onmt
except:
	call_onmt = None
import os
class NatasNotInstalled(Exception):
	pass

class NeuralFST(object):
	"""docstring for NeuralFST"""
	def __init__(self, model_path):
		if call_onmt is None:
			raise NatasNotInstalled("Natas is needed for neural models, run:\n\npip install natas")
		
		self.model_path = model_path
	
	def analyze(self, word, n_best=1):
		if len(word) == 0:
			return []
		model_a = os.path.join(self.model_path, "analyzer.pt")
		model_l = os.path.join(self.model_path, "lemmatizer.pt")
		tags = call_onmt([" ".join(word)] ,model_a,n_best=n_best,return_scores=True)[0]
		lemma = call_onmt([" ".join(word)], model_l,n_best=n_best,return_scores=True)[0]
		lem_tags = zip(tags, lemma)
		return [(l[0].replace(" ","") + "+" + t[0].replace(" ","+"), l[1] + t[1]) for t,l in lem_tags ]

	def generate(self, word, n_best=1):
		if len(word) ==0:
			return []
		model_g = os.path.join(self.model_path, "generator.pt")
		parts = word.split("+")
		parts[0] = " ".join(parts[0])
		forms =  call_onmt([" ".join(parts)] ,model_g, n_best=n_best,return_scores=True)[0]
		return [(form.replace(" ", ""), score) for form, score in forms]

