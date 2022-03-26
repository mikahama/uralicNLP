import re
import mikatools
from . import uralicApi
from . import string_processing

preps = list(set("كبولف"))
al = "ال"

sentence_end = set("!?。……‥！？。⋯…؟჻!…")
word_end_puct = set(",;:”’'\"»」)]}،؛》』〕｠〉》】〗〙〛–—")
word_start_punct = set("'\"¡¿「«“”‘({[《『〔｟〈《【〖〘〚–—”")
numbers = set("0123456789١٢٣٤٥٦٧٨٩٠")
_custom_punctuation = set('!"#$%&\'()*+,-.:;<=>?@[]^_`{|}~')

abrvs = mikatools.json_load(mikatools.script_path("abrvs.json"))
abrv_regex = re.compile(r"(^|\s)(" + "|".join([re.escape(a) for a in abrvs]) + ")$")

def _ends_in_abrv(text):
	return abrv_regex.search(text.lower()) is not None

def _remove_preps(word):
	for p in preps:
		if word.startswith(p):
			word = word[1:]
			return word, p
	return word, None

def tokenize_arabic(text):
	toksut = sentences(text)
	#print(toksut)
	output = []
	for sentence in toksut:
		o_sentence = []
		for w in words(sentence):
			#print(o_sentence)
			#print(w)
			word = w
			lemmas = uralicApi.lemmatize(word, "ara",word_boundaries=True)
			preppu = None
			alli = None
			high_count = 0
			long_len = 0
			stop =False
			for l in lemmas:
				if "|" in l:
					c = l.count("|")
					if c > high_count:
						high_count = c
						long_len = len(l)
						stop = l
					elif high_count == c:
						if len(l) > long_len:
							stop = l
							long_len = len(l)
			if high_count > 0:
				o_sentence.extend([x for x in stop.split("|") if len(string_processing.remove_arabic_diacritics(x)) >0])
				continue

			if len(lemmas) == 0:
				word, preppu = _remove_preps(word)
				lemmas = uralicApi.lemmatize(word, "ara")
			if len(lemmas) == 0 and word.startswith(al):
				word = word[2:]
				alli = al
				lemmas = uralicApi.lemmatize(word, "ara")
			if len(lemmas) == 0:
				o_sentence.append(w)
			else:
				parttusan = [preppu, alli, lemmas[0]]
				#print(parttusan)
				o_sentence.extend([x for x in parttusan if x is not None])
		output.append(o_sentence)
	return output

def sentences(text):
	parts = []
	current_s = ""
	previous_break = False
	for i, c in enumerate(text):
		if c in sentence_end:
			#End of a sentence, not a dot
			if len(current_s) > 0:
				#There is a current sentence, apped it and clear it
				parts.append(current_s + c)
				current_s = ""
			elif len(parts) > 0:
				#No current sentence, add to a previous sentence
				parts[len(parts)-1] += c
			else:
				#Make it a current sentence
				current_s = c
		elif c == ".":
			#A dot
			if len(current_s) == 0:
				#no current sentence
				if len(parts) > 0:
					#append
					parts[len(parts)-1] += c
				else:
					current_s = c
			elif len(current_s) > 0 and current_s[-1] in numbers:
				#previous is a number
				current_s += c
			elif _ends_in_abrv(current_s):
				#abreviation
				current_s += c
			elif len(text) > i+1 and len(text[i+1].strip()) != 0:
				#dot is not followed by a space
				current_s += c
			else:
				#dot ending a sentence
				parts.append(current_s + c)
				current_s = ""
		elif c == "\n":
			#line break
			if previous_break and len(current_s) > 0:
				parts.append(current_s)
				current_s = ""
			if not previous_break and len(current_s) > 0:
				current_s += c
			previous_break = True
			continue
		elif c == "\r":
			#Windows line break
			continue
		else:
			#Any other character
			current_s += c
		previous_break = False
	if len(current_s) > 0:
		parts.append(current_s)
	space_regex = re.compile(r"\s+")
	parts = [space_regex.sub(" ", part).strip() for part in parts]
	parts = [part for part in parts if len(part) > 0]
	return parts


def words(text):
	multidot = re.compile(r"(\.{2,})$")
	space_regex = re.compile(r"\s+")
	for sentence_end_p in sentence_end:
		text = text.replace(sentence_end_p, " " + sentence_end_p)
	text = space_regex.sub(" ", text).strip()
	whitespace_tokens = text.split(" ")
	tokens = []
	for t in whitespace_tokens:
		first_tok = []
		last_tok = []
		cont_first = True
		while cont_first:
			cont_first = False
			if len(t) > 0 and t[0] in word_start_punct:
				cont_first = True
				first_tok.append(t[0])
				t = t[1:]
		cont_last = True
		while cont_last:
			cont_last = False
			if len(t) > 0 and t[-1] in word_end_puct:
				cont_last = True
				last_tok.insert(0,t[-1])
				t = t[:-1]
			elif len(t)>1 and t[-1] == "." and t[-2] in word_end_puct:
				cont_last = True
				last_tok.insert(0,t[-1])
				last_tok.insert(0,t[-2])
				t = t[:-2]
		dots = multidot.search(t)
		if dots is not None:
			#Make .. or ... or whaterver its own token
			dots = dots.groups()[0]
			last_tok.insert(0, dots)
			t = t[:-len(dots)]
		elif len(t) >0 and t[-1] == ".":
			if not _ends_in_abrv(t[:-1]):
				t = t[:-1]
				last_tok.insert(0, ".")

		if ("/" in t or "\\" in t) and not any((x in _custom_punctuation for x in t)):
			#not a link
			t = t.replace("/", " /").replace("\\", " \\")
			t = t.split(" ")
		else:
			t = [t]
		t = [x for x in t if len(x) > 0]

		first_tok.extend(t)
		first_tok.extend(last_tok)
		tokens.extend(first_tok)

	tokens = [tok for tok in tokens if len(tok) > 0]
	return tokens

	

def tokenize(text):
	sents = sentences(text)
	return [words(s) for s in sents]