#encoding: utf-8
from .uralicApi import analyze as uralic_api_analyze
from .uralicApi import __where_models as where_models
import os, sys
from subprocess import Popen, PIPE

def _Cg3__parse_sentence(words, language, morphology_ignore_after=None):
	sentence = []
	for word in words:
		analysis = __hfst_format(word, language, morphology_ignore_after)
		sentence.extend(analysis)
	hfst_result_string = "\n".join(sentence)
	return hfst_result_string

def __hfst_format(word, language, morphology_ignore_after=None):
	analysis = uralic_api_analyze(word, language)
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
	def __init__(self, language):
		model_path = where_models(language)
		cg_path = os.path.join(model_path, "cg")
		self.cg_path = cg_path
		self.language = language

	def disambiguate(self, words, morphology_ignore_after="@"):
		hfst_output = __parse_sentence(words + [""], self.language, morphology_ignore_after)
		p1 = Popen(["echo", hfst_output], stdout=PIPE)
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
		
		
		

