#encoding: utf-8
from .uralicApi import analyze as uralic_api_analyze
from .uralicApi import __where_models as where_models
import copy
import re
import os
from pycg3 import Cg


class Cg3():
	def __init__(self, language, morphology_languages=None):
		if morphology_languages is None:
			self.morphology_languages = language
		else:
			if language not in morphology_languages:
				morphology_languages.append(language)
			self.morphology_languages = morphology_languages
		model_path = where_models(language)
		cg_path = os.path.join(model_path, "cg3")
		self.cg = Cg.from_files(cg_path)
		self.language = language
		self.path = cg_path

	def disambiguate(self, words, descriptive=True, neural_fallback=False):
		if self.morphology_languages is None:
			morphologies = [uralic_api_analyze(w, self.language, descriptive=descriptive, neural_fallback=neural_fallback) for w in words]
		else:
			morphologies = []
			for l in self.morphology_languages:
				morphologies.extend([uralic_api_analyze(w, l, descriptive=descriptive, neural_fallback=neural_fallback) for w in words])
		result = self.cg.disambiguate(words, morphologies)
		return result
		
class Cg3Pipe():
	def __init__(self, *args, **kwargs):
		self.cg = Cg.from_files([a.path for a in *args]) 

	def disambiguate(self, words, **kwargs):
		return self.cg(words, **kwargs)
		
		

