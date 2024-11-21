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

try:
	import anthropic
except:
	pass

try:
	import voyageai
except:
	pass

from .uralicApi import lemmatize, get_translation

from .tokenizer import words as tokenize_words

from .string_processing import iso_to_name

from .dictionary_backends import TinyDictionary

from py_markdown_table.markdown_table import markdown_table

import json

from mikatools import pickle_dump, pickle_load

class ModuleNotInstalled(Exception):
	pass

class WordNotInDictionaryException(Exception):
    pass

class NoLemmaException(Exception):
    pass

class NothingToLemmatizeException(Exception):
    pass


class NotImplementedException(Exception):
    pass

def get_llm(llm_name, *args, **kwargs):
	if llm_name == "chatgpt":
		return ChatGPT(*args, **kwargs)
	elif llm_name == "gemini":
		return Gemini(*args, **kwargs)
	elif llm_name == "mistral":
		return Mistral(*args, **kwargs)
	elif llm_name == "claude":
		return Claude(*args, **kwargs)
	elif llm_name == "voyage":
		return Voyage(*args, **kwargs)
	else:
		return HuggingFace(llm_name, *args, **kwargs)
		

class LLM(object):
	"""docstring for LLM"""
	def __init__(self):
		self.cache = False
		self._embed_cache_dict = {}
		self._prompt_cache_dict = {}
		super(LLM, self).__init__()


	def _embed_cache(func):
		def inner(*args, **kwargs):
			self = args[0]
			if self.cache and "_".join(args[1:]) in self._embed_cache_dict:
				return self._embed_cache_dict["_".join(args[1:])]
			else:
				r = func(*args, **kwargs)
				if self.cache:
					self._embed_cache_dict["_".join(args[1:])] = r
				return r
		return inner

	def _prompt_cache(func):
		def inner(*args, **kwargs):
			self = args[0]
			if self.cache and "_".join(args[1:]) in self._prompt_cache_dict:
				return self._prompt_cache_dict["_".join(args[1:])]
			else:
				r = func(*args, **kwargs)
				if self.cache:
					self._prompt_cache_dict["_".join(args[1:])] = r
				return r
		return inner


	@_prompt_cache
	def prompt(self, text):
		return self._prompt(text)

	def _prompt(self, text):
		raise NotImplementedException("LLM does not support prompting")

	@_embed_cache
	def embed(self, text):
		return self._embed(text)

	def _embed(self, text):
		raise NotImplementedException("LLM does not support embeddings")

	@_embed_cache
	def embed_endangered(self, text, lang, dict_lang,backend=TinyDictionary):
		r = []
		for word in tokenize_words(text):
			lemmas = lemmatize(word, lang)
			if len(lemmas) == 0:
				r.append(word)
				continue
			lemma = lemmas[0]
			t = get_translation(lemma, lang, dict_lang,backend=backend)
			if len(t) == 0:
				r.append(lemma)
				continue
			r.append(t[0])
		text = " ".join(r)
		return self.embed(text)

	def save_cache(self, file, *args, **kwargs):
		pickle_dump([self._embed_cache_dict, self._prompt_cache_dict], file, *args, **kwargs )

	def load_cache(self, file, *args, **kwargs):
		self.cache = True
		self._embed_cache_dict, self._prompt_cache_dict = pickle_load(file, *args, **kwargs)


class ChatGPT(LLM):
	"""docstring for ChatGPT"""
	def __init__(self, api_key, model="gpt-4o"):
		super(ChatGPT, self).__init__()
		try:
			self.client = OpenAI(api_key=api_key)
		except:
			raise ModuleNotInstalled("OpenAI Python library is not installed. Run pip install openai. If you do have the library installed, check your API key.")
		self.model = model

	def _prompt(self, prompt, temperature=1):
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

	def _embed(self, text):
		response = self.client.embeddings.create(input=text, model=self.model)
		return response.data[0].embedding

class Gemini(LLM):
	"""docstring for Gemini"""
	def __init__(self, api_key, model="gemini-1.5-flash", task_type="retrieval_document"):
		super(Gemini, self).__init__()
		try:
			genai.configure(api_key=api_key)
		except:
			raise ModuleNotInstalled("Google Python library is not installed. Run pip install google-generativeai. If you do have the library installed, check your API key.")
		self.model = genai.GenerativeModel(model)
		self.model_name = model
		self.task_type = task_type

	def _prompt(self, prompt):
		response = self.model.generate_content(prompt)
		return response.text

	def _embed(self, text):
		result = genai.embed_content(model=self.model_name, content=text, task_type=self.task_type)
		return result['embedding']

class HuggingFace(LLM):
	def __init__(self, model, max_length=1000, device=-1):
		super(HuggingFace, self).__init__()
		self.max_length = max_length
		self.model_name = model
		self.model = None
		self.embedder = None
		self.device = device

	def _prompt(self, prompt):
		if self.model is None:
			self.model = pipeline('text-generation', model = self.model_name, device = self.device)
		r = self.model(prompt, max_length=self.max_length, truncation=True)
		return " ".join([x['generated_text'] for x in r])

	def _embed(self, text):
		if self.embedder is None:
			self.embedder = pipeline('feature-extraction', model=self.model_name,device = self.device)
		r = self.embedder(text, return_tensors="pt")[0].numpy().mean(axis=0)
		return list(r)

class Mistral(LLM):
	def __init__(self, api_key, model="mistral-small-latest"):
		super(Mistral, self).__init__()
		try:
			self.s = MistralApi(api_key=api_key)
		except:
			raise ModuleNotInstalled("Mistral library is not installed. Run pip install mistralai. If you do have the library installed, check your API key.")
		self.model = model

	def _prompt(self, prompt):
		r = self.s.chat.complete(model=self.model, messages=[{"content": prompt,"role": "user",}])
		return r.choices[0].message.content

	def _embed(self, text):
		embeddings_batch_response = self.s.embeddings.create(model=self.model, inputs=[text])
		return embeddings_batch_response.data[0].embedding


class Claude(LLM):
	"""docstring for ChatGPT"""
	def __init__(self, api_key, model="claude-3-5-sonnet-latest", max_length=1024):
		super(Claude, self).__init__()
		try:
			self.client = anthropic.Anthropic(api_key=api_key)
		except:
			raise ModuleNotInstalled("Anthropic Python library is not installed. Run pip install anthropic. If you do have the library installed, check your API key.")
		self.model = model
		self.max_length = max_length

	def _prompt(self, prompt, temperature=1):
		chat_completion = self.client.messages.create(model=self.model,messages=[{"role": "user", "content": prompt}], max_tokens=self.max_length)
		return " ".join([x.text for x in chat_completion.content])


class Voyage(LLM):
	"""docstring for LLM"""
	def __init__(self, api_key, model="voyage-3"):
		super(Voyage, self).__init__()
		try:
			self.vo = voyageai.Client(api_key=api_key)
		except:
			raise ModuleNotInstalled("Voyage Python library is not installed. Run pip install voyageai. If you do have the library installed, check your API key.")
		self.model = model

	def _embed(self, text):
		result = self.vo.embed([text], model=self.model, input_type="document")
		return result.embeddings[0]

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


		