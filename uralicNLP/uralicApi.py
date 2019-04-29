import requests, os
import ssl
import copy
import re
import mikatools


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

def model_info(language):
	filename = os.path.join(__where_models(language), "metadata.json")
	d = mikatools.json_load(filename)
	mikatools.print_json_help(d)

def download(language, show_progress=True):
	model_types = ["analyser","analyser-norm","generator-desc","generator-norm", "generator", "cg", "metadata.json"]
	download_to = os.path.join(__find_writable_folder(__model_base_folders()), language)
	ssl._create_default_https_context = ssl._create_unverified_context
	if not os.path.exists(download_to):
		os.makedirs(download_to)
	for model_type in model_types:
		try:
			print("Downloading " + model_type + " for " + language)
			url = api_url + "downloadModel/?language=" + language + "&type=" + model_type
			save_to = os.path.join(download_to, model_type)
			mikatools.download_file(url, save_to, show_progress)
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
	generator = get_transducer(language,cache=cache, analyzer=False, descrpitive=descrpitive, dictionary_forms=dictionary_forms)
	r = generator.lookup(query)
	return r

def get_transducer(language, cache=True, analyzer=True, descrpitive=True, dictionary_forms=True, convert_to_openfst=False):
	conversion_type = hfst.ImplementationType.TROPICAL_OPENFST_TYPE
	if not analyzer:
		#generator
		if cache and language + str(descrpitive) + str(dictionary_forms) + str(convert_to_openfst) in generator_cache:
			generator = generator_cache[language + str(descrpitive) + str(dictionary_forms)+ str(convert_to_openfst)]
		else:
			filename = os.path.join(__where_models(language), __generator_model_name(descrpitive, dictionary_forms))
			input_stream = hfst.HfstInputStream(filename)
			generator = input_stream.read()
			if convert_to_openfst:
				generator.convert(conversion_type)
			generator_cache[language+ str(descrpitive) + str(dictionary_forms)+ str(convert_to_openfst)] = generator
	else:
		if cache and language + str(descrpitive)+ str(convert_to_openfst) in analyzer_cache:
			generator = analyzer_cache[language+ str(descrpitive)+ str(convert_to_openfst)]
		else:
			filename = os.path.join(__where_models(language), __analyzer_model_name(descrpitive))
			input_stream = hfst.HfstInputStream(filename)
			generator = input_stream.read()
			if convert_to_openfst:
				generator.convert(conversion_type)
			analyzer_cache[language+ str(descrpitive)+ str(convert_to_openfst)] = generator
	return generator


def __analyzer_model_name(descrpitive):
	if descrpitive:
		return "analyser"
	else:
		return "analyser-norm"

def __analyze_locally(query, language, cache=True, descrpitive=True):
	generator = get_transducer(language,cache=cache, analyzer=True, descrpitive=descrpitive)
	r = generator.lookup(query)
	return r

def __encode_query(query):
	if not new_python and type(query) is unicode:
		query = query.encode('utf-8')
	return query

def __regex_escape(word):
	escape = ["#", "/","+","~","\\","&","-","$", "*", "|", "?", "{","}","\"",":",";","!", "."]
	for e in escape:
		word = word.replace(e, "%" +e)
	return word

def get_all_forms(word, pos, language, descrpitive=True, limit_forms=-1, filter_out=["#", "+Der", "+Cmp","+Err"]):
	analyzer = get_transducer(language, descrpitive=descrpitive, analyzer=True, convert_to_openfst=True)
	abcs = analyzer.get_alphabet()
	f = []
	flags = []
	for abc in abcs:
		for fi in filter_out:
			if abc.startswith(fi):
				f.append(__regex_escape(abc))
				break
		if "@" in abc and "@_"  not in abc:
			flags.append( "\"" + abc + "\"")
	flag_string = ""
	flag_end = ""
	start_flag_end = ""
	flag_string_start = ""
	if len(flags) > 0:
		flag_string_start =  " [ "+ " | ".join(flags)
		flag_string =  flag_string_start +" | "
		flag_string_start = "" +flag_string_start
		flag_end = "]"
		start_flag_end = "]* "
	reg_text = flag_string_start + start_flag_end + "{"+word+"} %+"+pos+ flag_string + " [ ? -  [ "+ " | ".join(f) +" ]]"+flag_end+"*"
	reg = hfst.regex(reg_text)
	analyzer2 = copy.copy(analyzer)
	analyzer2.compose(reg)
	output = analyzer2.extract_paths(max_cycles=1, max_number=limit_forms,output='text').replace("@_EPSILON_SYMBOL_@","").split("\n")
	output = filter(lambda x: x, output)
	output = list(map(lambda x: x.split('\t'), output))
	return list(map(lambda x: (x[0], float(x[1]),), output))

def generate(query, language, force_local=False, descrpitive=False, dictionary_forms=True):
	if force_local or __where_models(language, safe=True):
		return __generate_locally(__encode_query(query), language, descrpitive=descrpitive, dictionary_forms=dictionary_forms)
	else:
		return __api_generate(query, language, descrpitive=descrpitive, dictionary_forms=dictionary_forms)

def __remove_symbols(string):
	return re.sub('@[^@]*@', '', string)

def analyze(query, language, force_local=False, descrpitive=True, remove_symbols=True):
	if force_local or __where_models(language, safe=True):
		r = __analyze_locally(__encode_query(query), language,descrpitive=descrpitive)
	else:
		r = __api_analyze(query, language,descrpitive=descrpitive)
	if remove_symbols:
		r = list(r)
		for i in range(len(r)):
			item = r[i]
			r[i] = (__remove_symbols(item[0]),item[1])

	return r

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