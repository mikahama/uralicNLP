import requests, os
import ssl


try:
    # For Python 3.0 and later
    from urllib.request import urlopen
    new_python = True
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    new_python = False
import hfst

api_url = "https://akusanat.com/smsxml/"

class ModelNotFound(Exception):
    pass

class UnsupportedModel(Exception):
	pass

def __model_base_folders():
	a = os.path.join(os.path.dirname(__file__), "models")
	b = os.path.join(os.path.expanduser("~"), ".uralicnlp")
	return a, b

def __find_writable_folder(folders):
	for folder in folders:
		try:
			if not os.path.exists(folder):
				os.makedirs(folder)
			if os.access(folder, os.W_OK):
				return folder
		except:
			pass
	return None

def _Cg3__where_models(language, safe=False):
	return __where_models(language, safe)

def is_language_installed(language):
	path = __where_models(language, True)
	if path is None:
		return False
	return True

def __where_models(language, safe=False):
	paths = __model_base_folders()
	for path in paths:
		path = os.path.join(path, language)
		e = os.path.exists(path)
		if e:
			return path
	if safe:
		return None
	raise ModelNotFound("Models for " + language + " were not in " + " or ".join(paths) + ". Use uralicApi.download(\""+ language+"\") to download models.")

def download(language):
	model_types = ["analyser","analyser-norm","generator-desc","generator-norm", "generator", "cg"]
	download_to = os.path.join(__find_writable_folder(__model_base_folders()), language)
	ssl._create_default_https_context = ssl._create_unverified_context
	if not os.path.exists(download_to):
		os.makedirs(download_to)
	for model_type in model_types:
		try:
			model_file = urlopen(api_url + "downloadModel/?language=" + language + "&type=" + model_type)
			with open(os.path.join(download_to, model_type) ,'wb') as output:
				output.write(model_file.read())
			print("Model " + model_type + " for " + language + " was downloaded")
		except:
			print("Couldn't download " + model_type + " for " + language + ". It might be that the model for the language is not supported yet.")

generator_cache = {}
analyzer_cache = {}

def __generator_model_name(descrpitive, dictionary_forms):
	if not descrpitive and dictionary_forms:
		return "generator"
	elif descrpitive:
		return "generator-desc"
	else:
		return "generator-norm"

def __generate_locally(query, language, cache=True, descrpitive=False, dictionary_forms=True):
	if cache and language + str(descrpitive) + str(dictionary_forms) in generator_cache:
		generator = generator_cache[language + str(descrpitive) + str(dictionary_forms)]
	else:
		filename = os.path.join(__where_models(language), __generator_model_name(descrpitive, dictionary_forms))
		input_stream = hfst.HfstInputStream(filename)
		generator = input_stream.read()
		generator_cache[language+ str(descrpitive) + str(dictionary_forms)] = generator
	r = generator.lookup(query)
	return r

def __analyzer_model_name(descrpitive):
	if descrpitive:
		return "analyser"
	else:
		return "analyser-norm"

def __analyze_locally(query, language, cache=True, descrpitive=True):
	if cache and language + str(descrpitive) in analyzer_cache:
		generator = analyzer_cache[language+ str(descrpitive)]
	else:
		filename = os.path.join(__where_models(language), __analyzer_model_name(descrpitive))
		input_stream = hfst.HfstInputStream(filename)
		generator = input_stream.read()
		analyzer_cache[language+ str(descrpitive)] = generator
	r = generator.lookup(query)
	return r

def __encode_query(query):
	if not new_python and type(query) is unicode:
		query = query.encode('utf-8')
	return query

def generate(query, language, force_local=False, descrpitive=False, dictionary_forms=True):
	if force_local or __where_models(language, safe=True):
		return __generate_locally(__encode_query(query), language, descrpitive=descrpitive, dictionary_forms=dictionary_forms)
	else:
		return __api_generate(query, language, descrpitive=descrpitive, dictionary_forms=dictionary_forms)

def analyze(query, language, force_local=False, descrpitive=True):
	if force_local or __where_models(language, safe=True):
		return __analyze_locally(__encode_query(query), language,descrpitive=descrpitive)
	else:
		return __api_analyze(query, language,descrpitive=descrpitive)

def lemmatize(word, language, force_local=False, descrpitive=True):
    analysis = analyze(word, language, force_local, descrpitive=descrpitive)
    lemmas = []
    for tupla in analysis:
        an = tupla[0]
        if "@" in an:
            lemma = an.split("@")[0]
        else:
            lemma = an
        if "+" in lemma:
            lemmas.append(lemma.split("+")[0])
    lemmas = list(set(lemmas))
    return lemmas

def supported_languages():
	return __send_request("listLanguages/", {"user": "uralicApi"})

def __api_analyze(word, language,descrpitive=True):
	if not descrpitive:
		raise UnsupportedModel("Server only supports descrpitive analysis. Please download the models and analyze locally")
	return __send_request("analyze/", {"word": word, "language": language})["analysis"]

def __api_generate(query, language, descrpitive=False, dictionary_forms=True):
	if descrpitive or not dictionary_forms:
		raise UnsupportedModel("Server only supports normative dictionary forms. Please download the models and generate locally")
	return __send_request("generate/", {"query": query, "language": language})["analysis"]

def dictionary_search(word, language):
	return __send_request("search/", {"word": word, "language": language})

def __send_request(url, data):
	r = requests.get(api_url + url, params=data)
	return r.json()