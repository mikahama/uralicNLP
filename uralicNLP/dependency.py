from uralicNLP.ud_tools import UD_collection
import urllib, requests

class LanguageNotSupported(Exception):
    pass

class BackendNotOnline(Exception):
    pass

def parse_text(sentence, language, **kwargs):
	if language is not "fin":
		raise LanguageNotSupported("Language is not supported")
	return _turku_dependencies(sentence, **kwargs)


def _turku_dependencies(text, url="http://localhost:9876"):
	#r_url = url + "/?text=" + urllib.quote(text.encode('utf8'))
	#r = requests.get(r_url)
	r = requests.post(url, data=text, headers={'content-type':'text/plain'})
	if r.status_code != 200:
		raise BackendNotOnline("Couldn't connect to the docker server (code "+ str(r.status_code) +") at " + url + "\n Download the docker container on https://hub.docker.com/r/kazhar/finnish-dep-parser/ and make sure it is running.")
	conl = r.text
	sent = UD_collection(conl.split("\n"))
	return sent