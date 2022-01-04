#encoding: utf-8
from .uralicApi import analyze as uralic_api_analyze
from .uralicApi import __where_models as where_models
import os, sys
from subprocess import Popen, PIPE
from mikatools import open_write
import copy
import re

def _Cg3__parse_sentence(words, language, morphology_ignore_after=None, descriptive=True,remove_symbols=True, language_flags=False, words_analysis=None,neural_fallback=False):
	sentence = []
	if words_analysis is not None and len(words_analysis) < len(words):
		words_analysis = words_analysis + [[]]
	for i, word in enumerate(words):
		existing_analysis = None
		if words_analysis is not None:
			existing_analysis = words_analysis[i]
		analysis = __hfst_format(word, language, morphology_ignore_after,descriptive=descriptive, remove_symbols=remove_symbols, language_flags=language_flags, analysis=existing_analysis,neural_fallback=neural_fallback)
		sentence.extend(analysis)
	hfst_result_string = "\n".join(sentence)
	return hfst_result_string

def __hfst_format(word, language, morphology_ignore_after=None, descriptive=True,remove_symbols=True, language_flags=False, analysis=None,neural_fallback=False):
	if analysis is None:
		analysis = uralic_api_analyze(word, language,descriptive=descriptive,remove_symbols=remove_symbols, language_flags=language_flags,neural_fallback=neural_fallback)
	hfsts = []
	if len(analysis) == 0:
		hfsts.append(word + "\t" +word + "+?\tinf")
	for analys in analysis:
		if morphology_ignore_after is None:
			a = analys[0]
		else:
			a = analys[0].split(morphology_ignore_after)[0]
		hfsts.append(word + "\t" + a + "\t" + str(analys[1]))
	hfsts.append("")
	return hfsts

class Cg3():
	def __init__(self, language, morphology_languages=None):
		if morphology_languages is None:
			self.morphology_languages = language
		else:
			self.morphology_languages = morphology_languages
		model_path = where_models(language)
		cg_path = os.path.join(model_path, "cg")
		self.cg_path = cg_path
		self.language = language

	def disambiguate(self, words, morphology_ignore_after=None,descriptive=True,remove_symbols=True, temp_file=None, language_flags=False, morphologies=None, neural_fallback=False):
		hfst_output = __parse_sentence(words + [""], self.morphology_languages, morphology_ignore_after, descriptive=descriptive,remove_symbols=remove_symbols, language_flags=language_flags, words_analysis=morphologies, neural_fallback=neural_fallback)
		if temp_file is None:
			p1 = Popen(["echo", hfst_output], stdout=PIPE)
		else:
			f = open_write(temp_file)
			f.write(hfst_output)
			f.close()
			p1 = Popen(["cat", temp_file], stdout=PIPE)
		cg_conv = Popen(["cg-conv" ,"-f"], stdout=PIPE, stdin=p1.stdout)
		vislcg3 = Popen(['vislcg3', '--grammar', self.cg_path], stdout=PIPE, stdin=cg_conv.stdout)
		cg_results, error = vislcg3.communicate()
		return self.__parse_cg_results(cg_results)

	def __parse_cg_results(self, cg_results):
		if type(cg_results) is bytes:
			cg_results = cg_results.decode(sys.stdout.encoding)
		lines = cg_results.split("\n")
		results = []
		current_word = None
		current_list = []
		for line in lines:
			if line.startswith("\"<"):
				if current_word is not None:
					results.append((current_word, current_list))
				current_word = line[2:-2]
				current_list = []
			elif line.startswith("\t"):
				line = line[2:]
				parts = line.split("\" ", 1)
				if len(parts) < 2:
					continue
				w = Cg3Word(current_word, parts[0], parts[1].split(" "))
				current_list.append(w)
		return results
		
class Cg3Word():
	def __init__(self, form, lemma, morphology):
		self.form = form
		self.lemma = lemma
		self.morphology = morphology

	def __repr__(self):
		o = "<" + self.lemma + " - " + ", ".join(self.morphology) + ">"
		if type(o) is str:
			return o
		return o.encode("utf-8")

class Cg3Disambiguation():
	def __init__(self):
		self.arg = arg
		
class Cg3Pipe():
	def __init__(self, *args, **kwargs):
		self.cgs = args

	def _find_weight(self, cg_morphologies):
		for i, m in enumerate(cg_morphologies):
			if re.search(r"^\<W\:\d\.?\d+\>$",m):
				return i

	def _convert_morphologies(self, cg_results):
		analysis = []
		cg_results = copy.deepcopy(cg_results)
		for disambiguation in cg_results:
			possible_words = disambiguation[1]
			word_analysis = []
			for possible_word in possible_words:
				w = "".join(re.findall(r"\d+|\.", possible_word.morphology.pop(self._find_weight(possible_word.morphology))))
				w = float(w)
				r = [possible_word.lemma + "+" + "+".join(possible_word.morphology), w]
				word_analysis.append(r)
			analysis.append(word_analysis)
		return analysis

	def disambiguate(self, words, **kwargs):
		morphologies = None
		for cg in self.cgs:
			res = cg.disambiguate(words, morphologies=morphologies, **kwargs)
			morphologies = self._convert_morphologies(res)
		return res
		
		

