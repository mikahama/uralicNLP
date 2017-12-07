import requests

api_url = "http://sanat.csc.fi:8000/smsxml/"

def supported_languages():
	return __send_request("listLanguages/", {"user": "uralicApi"})

def analyze(word, language):
	return __send_request("analyze/", {"word": word, "language": language})

def generate(query, language):
	return __send_request("generate/", {"query": query, "language": language})

def dictionary_search(word, language):
	return __send_request("search/", {"word": word, "language": language})

def lemmatize(word, language):
	return __send_request("lemmatize/", {"word": word, "language": language})

def __send_request(url, data):
	r = requests.get(api_url + url, params=data)
	return r.json()