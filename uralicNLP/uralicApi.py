#encoding: utf-8
import requests, os
import ssl
import copy
import re
import mikatools
from .foma import FomaFSTWrapper
from .string_processing import filter_arabic
from collections.abc import Iterable
import glob
import datetime
import shutil
from .dictionary_backends import TinyDictionary, MongoDictionary


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
download_server_url = "https://models.uralicnlp.com/nightly/"

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

def _file_modification_time(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def __where_models(language, safe=False, return_latest=True):
	paths = __model_base_folders()
	latest_model = [None, 0]
	for path in paths:
		path = os.path.join(path, language)
		e = os.path.exists(path)
		if e:
			if return_latest is False:
				return path
			else:
				files = glob.glob(os.path.join(path, "*"))
				files.sort(key=os.path.getmtime)
				if len(files) == 0:
					continue
				t = _file_modification_time(files[0])
				if latest_model[0] is None or t > latest_model[1]:
					latest_model = [path, t]
	if return_latest and latest_model[0] is not None:
		return latest_model[0]
	if safe:
		return None
	raise ModelNotFound("Models for " + language + " were not in " + " or ".join(paths) + ". Use uralicApi.download(\""+ language+"\") to download models.")

def model_info(language):
	filename = os.path.join(__where_models(language), "metadata.json")
	d = mikatools.json_load(filename)
	mikatools.print_json_help(d)

def uninstall(language):
	path = __where_models(language, safe=True)
	while path is not None:
		print("removing " + path)
		shutil.rmtree(path)
		path = __where_models(language, safe=True)

def download(language, show_progress=True):
	model_types = {"analyser":"analyser-gt-desc.hfstol", "analyser-norm":"analyser-gt-norm.hfstol","analyser-dict":"analyser-dict-gt-norm.hfstol", "generator-desc":"generator-gt-desc.hfstol", "generator-norm":"generator-gt-norm.hfstol", "generator":"generator-dict-gt-norm.hfstol", "cg":"disambiguator.bin", "metadata.json":"metadata.json", "dictionary.json":"dictionary.json"}
	download_to = os.path.join(__find_writable_folder(__model_base_folders()), language)
	ssl._create_default_https_context = ssl._create_unverified_context
	if not os.path.exists(download_to):
		os.makedirs(download_to)
	for model_type, model_url in model_types.items():
		try:
			print("Downloading " + model_type + " for " + language)
			url = download_server_url + language + "/" + model_url
			save_to = os.path.join(download_to, model_type)
			mikatools.download_file(url, save_to, show_progress)
			print("Model " + model_type + " for " + language + " was downloaded")
		except:
			if model_type == "metadata.json":
				mikatools.json_dump({"info":"no metadata provided"}, save_to)
			print("Couldn't download " + model_type + " for " + language + ". It might be that the model for the language is not supported yet.")

generator_cache = {}
analyzer_cache = {}
dictionary_cache = {}

def __generator_model_name(descrpitive, dictionary_forms):
	if not descrpitive and dictionary_forms:
		return "generator"
	elif descrpitive:
		return "generator-desc"
	else:
		return "generator-norm"

def __generate_locally(query, language, cache=True, descrpitive=False, dictionary_forms=True,filename=None):
	generator = get_transducer(language,cache=cache, analyzer=False, descrpitive=descrpitive, dictionary_forms=dictionary_forms,filename=filename)
	r = generator.lookup(query)
	return r

def get_transducer(language, cache=True, analyzer=True, descrpitive=True, dictionary_forms=True, convert_to_openfst=False, filename=None):
	conversion_type = hfst.ImplementationType.TROPICAL_OPENFST_TYPE
	if not analyzer:
		#generator
		if filename is None:
			filename = os.path.join(__where_models(language), __generator_model_name(descrpitive, dictionary_forms))
		if cache and filename in generator_cache:
			generator = generator_cache[filename]
		else:
			generator = _load_transducer(filename, True)
			if convert_to_openfst:
				generator.convert(conversion_type)
			generator_cache[filename] = generator
	else:
		if filename is None:
			filename = os.path.join(__where_models(language), __analyzer_model_name(descrpitive, dictionary_forms))
		if cache and filename in analyzer_cache:
			generator = analyzer_cache[filename]
		else:
			generator =  _load_transducer(filename, False)
			if convert_to_openfst:
				generator.convert(conversion_type)
			analyzer_cache[filename] = generator
	return generator

def _load_transducer(filename, invert):
	metadata_filename =  os.path.join(os.path.dirname(filename), "metadata.json")
	try:
		metadata = mikatools.json_load(metadata_filename)
	except:
		#No crash if JSON is not found or malformed for some reason
		metadata = {}
	if "fst_type" in metadata and metadata["fst_type"] == "foma":
		return FomaFSTWrapper(filename, invert)
	elif "fst_type" in metadata and metadata["fst_type"] == "att":
		return hfst.read_att_transducer(mikatools.open_read(filename))
	else:
		input_stream = hfst.HfstInputStream(filename)
		return input_stream.read()



def __analyzer_model_name(descrpitive, dictionary):
	if dictionary:
		return "analyser-dict"
	elif descrpitive:
		return "analyser"
	else:
		return "analyser-norm"

def __analyze_locally(query, language, cache=True, descrpitive=True, dictionary_forms=False, filename=None):
	generator = get_transducer(language,cache=cache, analyzer=True, descrpitive=descrpitive, dictionary_forms=dictionary_forms,filename=filename)
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
	analyzer = get_transducer(language, descrpitive=descrpitive, analyzer=True, convert_to_openfst=True, cache=True, dictionary_forms=False)
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
	analyzer2 = analyzer.copy()
	analyzer2.compose(reg)
	output = analyzer2.extract_paths(max_cycles=1, max_number=limit_forms,output='text').replace("@_EPSILON_SYMBOL_@","").split("\n")
	output = filter(lambda x: x, output)
	output = list(map(lambda x: x.split('\t'), output))
	return list(map(lambda x: (x[0], float(x[1]),), output))

def generate(query, language, force_local=True, descrpitive=False, dictionary_forms=False, remove_symbols=True, filename=None):
	if force_local or __where_models(language, safe=True):
		r = __generate_locally(__encode_query(query), language, descrpitive=descrpitive, dictionary_forms=dictionary_forms,filename=filename)
	else:
		r = __api_generate(query, language, descrpitive=descrpitive, dictionary_forms=dictionary_forms)
	if remove_symbols:
		r = _remove_analysis_symbols(r)
	return r

def __remove_symbols(string):
	return re.sub('@[^@]*@', '', string)

def analyze(query, language, force_local=True, descrpitive=True, remove_symbols=True,language_flags=False, dictionary_forms=False,filename=None):
	if not isinstance(language, str) and isinstance(language, Iterable):
		#Treat as a list
		r = []
		for l in language:
			r.extend(analyze(query,l, force_local=force_local, descrpitive=descrpitive, remove_symbols=remove_symbols,language_flags=language_flags, dictionary_forms=dictionary_forms,filename=filename))
		return r

	if force_local or __where_models(language, safe=True):
		r = __analyze_locally(__encode_query(query), language,descrpitive=descrpitive,dictionary_forms=dictionary_forms,filename=filename)
	else:
		r = __api_analyze(query, language,descrpitive=descrpitive)
	if remove_symbols:
		r = _remove_analysis_symbols(r)

	if language_flags:
		return _add_language_flag(r, language)
	else:
		return r

def _add_language_flag(analysis, language):
	r = []
	for a in analysis:
		r.append((a[0] + "+" +language, a[1]))
	return r

def _remove_analysis_symbols(r):
	r = list(r)
	for i in range(len(r)):
		item = r[i]
		r[i] = (__remove_symbols(item[0]),item[1])
	return r

def lemmatize(word, language, force_local=True, descrpitive=True, word_boundaries=False, dictionary_forms=False, filename=None):
    analysis = analyze(word, language, force_local, descrpitive=descrpitive, dictionary_forms=dictionary_forms, filename=filename)
    lemmas = []
    if word_boundaries:
    	bound = "|"
    else:
    	bound = ""
    for tupla in analysis:
        an = tupla[0]
        if language == "swe":
            lemma = re.sub("[\<].*?[\>]", bound, an).strip(bound)
            lemmas.append(lemma)
        elif language == "ara":
        	lemmas.append(filter_arabic(an,combine_by=bound))
        else:
            if not "+Cmp#" in an and "#" in an:
                an = an.replace("#", "+Cmp#")
            res = an.split("+Cmp#")
            lemma = [x.split("+")[0] for x in res]
            if language == "eng":
            	lemma = [re.sub("[\[].*?[\]]", "", x) for x in lemma]
            lemmas.append(bound.join(lemma))

    lemmas = list(set(lemmas))
    return lemmas

def supported_languages():
	d = requests.get("https://uralic.mikakalevi.com/nightly/supported_languages.json")
	return d.json()

def __api_analyze(word, language,descrpitive=True):
	if not descrpitive:
		raise UnsupportedModel("Server only supports descrpitive analysis. Please download the models and analyze locally")
	return __send_request("analyze/", {"word": word, "language": language})["analysis"]

def __api_generate(query, language, descrpitive=False, dictionary_forms=True):
	if descrpitive or not dictionary_forms:
		raise UnsupportedModel("Server only supports normative dictionary forms. Please download the models and generate locally")
	return __send_request("generate/", {"query": query, "language": language})["analysis"]

def dictionary_search(word, language, force_local=True, backend=TinyDictionary):
	if force_local:
		d = _get_dictionary(language,backend=backend)
		lemmas = list(set(lemmatize(word, language)) - set([word]))
		return d.find(word, lemmas)
	else:
		return _api_dictionary_search(word, language)

def dictionary_lemmas(language, backend=TinyDictionary, group_by_pos=False):
	d = _get_dictionary(language,backend=backend)
	return d.lemmas(group_by_pos=group_by_pos)

def import_dictionary_to_db(language, backend=MongoDictionary):
	d = _get_dictionary(language, backend=backend)
	d.import_data()

def _api_dictionary_search(word, language):
	return __send_request("search/", {"word": word, "language": language})

def __send_request(url, data):
	r = requests.get(api_url + url, params=data)
	return r.json()

def _get_dictionary(language, backend=TinyDictionary):
	cache_key = backend.__name__ + "_" + language
	if cache_key in dictionary_cache:
		return dictionary_cache[cache_key]
	path = os.path.join(__where_models(language), "dictionary.json")
	dictionary = backend(path, language)
	dictionary_cache[cache_key] = dictionary
	return dictionary

