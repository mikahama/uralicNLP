import requests
from collections import defaultdict
from uralicNLP.dependency import LanguageNotSupported


class Traslator(object):
	"""docstring for Traslator"""
	def __init__(self):
		super(Traslator, self).__init__()
		self.languages = None

	def translate(self, text, source, target):
		self._get_languages()
		if source not in self.languages:
			raise LanguageNotSupported(source + " is not a supported language")
		if target not in self.languages[source]:
			raise LanguageNotSupported(source + "-" + target + " is not a supported pair")
		return self._translate(text, source, target)


	def get_languages(self, force_refresh=False):
		if self.languages == None or force_refresh:
			self._get_languages()
		return self.languages


class ApertiumTranslator(Traslator):
	"""docstring for ApertiumTranslator"""
	def __init__(self, url):
		super(ApertiumTranslator, self).__init__()
		self.url = url

	def _get_languages(self):
		r = requests.get(self.url + "list?q=pairs")
		data = r.json()
		languages = defaultdict(list)
		for item in data["responseData"]:
			languages[item["sourceLanguage"]].append(item["targetLanguage"])
		self.languages = languages

	def _translate(self, text, source, target):
		r = requests.post(self.url + "translate", {"langpair": source + "|" + target,"q": text})
		data = r.json()
		return data["responseData"]["translatedText"]


		
class YandexTranslator(Traslator):
	"""docstring for YandexTranslator"""
	def __init__(self, api_key):
		super(YandexTranslator, self).__init__()
		self.api_key = api_key

	def _get_languages(self):
		r = requests.get("https://translate.yandex.net/api/v1.5/tr.json/getLangs", {"key": self.api_key, "ui":"en"})
		data = r.json()
		langs = defaultdict(list)
		for item in data["dirs"]:
			s, t = item.split("-")
			langs[s].append(t)
		self.languages = langs

	def _translate(self, text, source, target):
		r = requests.post("https://translate.yandex.net/api/v1.5/tr.json/translate", {"key": self.api_key, "text":text, "lang": source + "-" + target})
		data = r.json()
		return data["text"][0]

	

def ApertiumBetaTranslator():
	return ApertiumTranslator("http://beta.apertium.org/apy/")

def ApertiumStableTranslator():
	return ApertiumTranslator("https://www.apertium.org/apy/")

def ApertiumGiellateknoTranslator():
	return ApertiumTranslator("https://gtweb.uit.no/apy/")

def ApertiumJorgalTranslator():
	return ApertiumTranslator("http://gtweb.uit.no/jorgal/apy/")

def ApertiumLocalhostTranslator():
	return ApertiumTranslator("http://localhost:2737/")


