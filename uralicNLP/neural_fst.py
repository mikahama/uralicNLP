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
	
	def analyze(self, word):
		if len(word) == 0:
			return []
		model_a = os.path.join(self.model_path, "analyzer.pt")
		model_l = os.path.join(self.model_path, "lemmatizer.pt")
		tags = call_onmt([" ".join(word)] ,model_a,n_best=1)[0][0].replace(" ", "+")
		lemma = call_onmt([" ".join(word)], model_l,n_best=1)[0][0].replace(" ", "")
		return [(lemma + "+" + tags, 0.0)]

	def generate(self, word):
		if len(word) ==0:
			return []
		model_g = os.path.join(self.model_path, "generator.pt")
		parts = word.split("+")
		parts[0] = " ".join(parts[0])
		form =  call_onmt([" ".join(parts)] ,model_g, n_best=1)[0][0].replace(" ", "")
		return [(form, 0.0)]