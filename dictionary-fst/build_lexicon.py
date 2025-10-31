from uralicNLP import uralicApi
from tqdm import tqdm
from mikatools import *
import re
from uralicNLP.dictionary_backends import MongoDictionary

def sanitize_word(word):
	return re.sub(r'[`,:#\^\+\?\*\[\]\{\}\(\);" /\\|\.]', '', word.replace(" ", "_"))

def get_translation(lemma, lang,backend=MongoDictionary):
	res = uralicApi.dictionary_search(lemma, lang,backend=backend)
	translations = {}
	for e in res["exact_match"]:
		try:
			mgs = e["mg"]
		except:
			continue
		if not isinstance(mgs, list):
			mgs = [mgs]
		for mg in mgs:
			try:
				tgs = mg["tg"]
			except:
				continue
			if not isinstance(tgs, list):
				tgs = [tgs]
			for tg in tgs:
				for tr in tgs:
					try:
						if tr["@xml:lang"] not in translations:
							translations[tr["@xml:lang"] ] = []
					
						ts = tr["t"]
					except:
						continue
					if not isinstance(ts, list):
						ts = [ts]
					for t in ts:
						try:
							translations[tr["@xml:lang"]].append(sanitize_word(t["#text"]))
						except:
							pass
		translations = {x:list(set(y)) for x, y in translations.items()}
	return translations

w = open_write("dict.lexc")
w.write("LEXICON Root\n\n")
for lang in uralicApi.supported_languages()["dictionary"]:
	if lang in ["lav","rus","est","fin","fra","spa","esp","eng", "nob","swe"]:
		continue
	print("Processing ", lang)
	uralicApi.import_dictionary_to_db(lang)
	print(lang, "in Mongo")
	lemmas = uralicApi.dictionary_lemmas(lang,backend=MongoDictionary)
	for lemma in tqdm(lemmas):
		translations = get_translation(lemma,lang,backend=MongoDictionary)
		lemma = sanitize_word(lemma)
		for trans_lang, trans in translations.items():
			for t in trans:
				w.write(lang + "_" + lemma +":"+ trans_lang + "_" + t +" #;\n")
				w.write(trans_lang + "_" + t +":"+ lang + "_" + lemma +" #;\n")
w.close()