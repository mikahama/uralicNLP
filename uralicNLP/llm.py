try:
	from openai import OpenAI
except:
	pass
try:
	import google.generativeai as genai
except:
	pass
try:
	from transformers import pipeline
except:
	pass

try:
	from mistralai import Mistral as MistralApi
except:
	pass

from .uralicApi import lemmatize, get_translation

from .tokenizer import words as tokenize_words

from .string_processing import iso_to_name

from .dictionary_backends import TinyDictionary

from py_markdown_table.markdown_table import markdown_table

import json

class ModuleNotInstalled(Exception):
	pass

class WordNotInDictionaryException(Exception):
    pass

class NoLemmaException(Exception):
    pass

class NothingToLemmatizeException(Exception):
    pass

def get_llm(llm_name, *args, **kwargs):
	if llm_name == "chatgpt":
		return ChatGPT(*args, **kwargs)
	elif llm_name == "gemini":
		return Gemini(*args, **kwargs)
	elif llm_name == "mistral":
		return Mistral(*args, **kwargs)
	else:
		return HuggingFace(llm_name, *args, **kwargs)
		

class LLM(object):
	"""docstring for LLM"""
	def __init__(self):
		super(LLM, self).__init__()

	def prompt(text):
		pass


class ChatGPT(LLM):
	"""docstring for ChatGPT"""
	def __init__(self, api_key, model="gpt-4o"):
		super(ChatGPT, self).__init__()
		try:
			self.client = OpenAI(api_key=api_key)
		except:
			raise ModuleNotInstalled("OpenAI Python library is not installed. Run pip install openai. If you do have the library installed, check your API key.")
		self.model = model

	def prompt(self, prompt, temperature=1):
		chat_completion = self.client.chat.completions.create(
			messages=[
				{
					"role": "user",
					"content": prompt,
				}
			],
			model=self.model,
			temperature=temperature
		)
		return chat_completion.choices[0].message.content

class Gemini(LLM):
	"""docstring for Gemini"""
	def __init__(self, api_key, model="gemini-1.5-flash"):
		super(Gemini, self).__init__()
		try:
			genai.configure(api_key=api_key)
		except:
			raise ModuleNotInstalled("Google Python library is not installed. Run pip install google-generativeai. If you do have the library installed, check your API key.")
		self.model = genai.GenerativeModel(model)

	def prompt(self, prompt):
		response = self.model.generate_content(prompt)
		return response.text

class HuggingFace(LLM):
	def __init__(self, model, max_length=1000):
		super(HuggingFace, self).__init__()
		self.model = pipeline('text-generation', model = model)
		self.max_length = max_length

	def prompt(self, prompt):
		r = self.model(prompt, max_length=self.max_length)
		return " ".join([x['generated_text'] for x in r])

class Mistral(LLM):
	def __init__(self, api_key, model="mistral-small-latest"):
		super(Mistral, self).__init__()
		try:
			self.s = MistralApi(api_key=api_key)
		except:
			ModuleNotInstalled("Mistral library is not installed. Run pip install mistralai. If you do have the library installed, check your API key.")
		self.model = model

	def prompt(self, prompt):
		r = self.s.chat.complete(model=self.model, messages=[{"content": prompt,"role": "user",}])
		return r.choices[0].message.content

def _create_disambiguation_prompt(sentence,lang, dict_lang, raise_exceptions=False, backend=TinyDictionary):
	if isinstance(sentence, str):
		sentence = tokenize_words(sentence)
	prompt = "Your task is to disambiguate a sentence in " + iso_to_name(lang) + ". You will be given the sentence, a table that has all of the words of the sentence in separate rows and a comma separated list of possible lemmas. You will need to pick the correct lemma for each word so that every word will have only one lemma. To help you understand " + iso_to_name(lang) + " you will also get a second table that gives you translations of the words in "+ iso_to_name(dict_lang) + "."
	prompt += "\n\nSentence:\n" + " ".join(sentence)
	prompt += "\n\nTable of lemmas:\n"
	lemma_data = []
	lemmas = []
	max_ambiguity = 1
	for word in sentence:
		w_lemmas = lemmatize(word, lang)
		if raise_exceptions and len(w_lemmas) == 0:
			raise NoLemmaException("No lemmas for word " + word + " in " + lang)
		if len(w_lemmas) > max_ambiguity:
			max_ambiguity = len(w_lemmas)
		lemma_data.append({"Word": word, "Lemmas": ", ".join(w_lemmas)})
		lemmas.extend(w_lemmas)
	if raise_exceptions and max_ambiguity == 1:
		raise NothingToLemmatizeException("The sentence is not ambiguous")
	lemmas = lemmas
	prompt += markdown_table(lemma_data).get_markdown()
	prompt += "\n\n"+ iso_to_name(lang) + " - " + iso_to_name(dict_lang) +" vocabulary:\n"
	vocab_data = []
	for lemma in lemmas:
		trans = get_translation(lemma, lang, dict_lang,backend=backend)
		if raise_exceptions and len(trans) == 0 and lemma not in string.punctuation:
			raise WordNotInDictionaryException("Word " + lemma + " not found in the "+lang + " dictionary for " + dict_lang)
		vocab_data.append({iso_to_name(lang): lemma, iso_to_name(dict_lang):", ".join(trans)})
	prompt += markdown_table(vocab_data).get_markdown()
	prompt += "\n\nPlease write out the steps of your decision process and provide a list of lemmas in JSON format at the very end of your answer. Example: {\"lemmas\": [\"lemma 1\", \"lemma 2\", \"lemma 3\"]}"
	return prompt.replace("```", "")

def disambiguate_sentence(sentence, lang, dict_lang, llm, raise_exceptions=False, backend=TinyDictionary):
	prompt = _create_disambiguation_prompt(sentence, lang, dict_lang, raise_exceptions=raise_exceptions, backend=backend)
	res = llm.prompt(prompt)
	j = res[res.rfind("{\"lemmas\":" ):]
	j = j[:j.find("}")+1]
	try:
		d = json.loads(j)["lemmas"]
	except:
		d = []
	return d, res


		