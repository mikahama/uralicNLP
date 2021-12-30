from glob import glob
from uralicNLP.ud_tools import UD_collection
from mikatools import *
from tqdm import tqdm

def has_numbers(inputString):
	return any(char.isdigit() for char in inputString)

def get_abreviations():
	uds = glob("../Downloads/Universal Dependencies 2.9/ud-treebanks-v2.9/*/*.conllu")
	abrvs = []
	for ud in tqdm(uds):
		udc = UD_collection(codecs.open(ud, encoding="utf-8"))
		for sentence in udc:
			for word in sentence:
				if word.pos == "PUNCT":
					continue
				if "." in word.lemma:
					abrvs.append(word.lemma)
	abrvs = list(set(abrvs))
	json_dump(abrvs, "abrvs.json")

def filter_abreviations():
	abrvs = json_load("abrvs.json")
	json_dump(list(set([abrv.replace("...", ".").lower() for abrv in abrvs if abrv[-1] == "." and not has_numbers(abrv)])), "abrvs.json")

def remove_dot():
	abrvs = json_load("abrvs.json")
	json_dump([abrv[:-1] for abrv in abrvs], "abrvs.json")


#get_abreviations()
#filter_abreviations()
#remove_dot()