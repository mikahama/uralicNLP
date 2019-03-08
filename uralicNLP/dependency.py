from uralicNLP.ud_tools import UD_collection
import urllib, requests
import sys

if (sys.version_info > (3, 0)):
	#python 3
	python_version = 3
else:
	python_version = 2

class LanguageNotSupported(Exception):
    pass

class BackendNotOnline(Exception):
    pass

def parse_text(sentence, language, **kwargs):
	if language is not "fin":
		raise LanguageNotSupported("Language is not supported")
	return _turku_dependencies(sentence, **kwargs)


def _turku_dependencies(text, url="http://localhost:9876"):
	if python_version ==2 and type(text) is str:
		pass
	else:
		text = text.encode('utf-8')
	r = requests.post(url, data=text, headers={'content-type':'text/plain; charset=utf8'})
	if r.status_code != 200:
		raise BackendNotOnline("Couldn't connect to the docker server (code "+ str(r.status_code) +") at " + url + "\n Download the docker container on https://hub.docker.com/r/kazhar/finnish-dep-parser/ and make sure it is running.")
	conl = r.text
	sent = UD_collection(conl.split("\n"))
	return sent
