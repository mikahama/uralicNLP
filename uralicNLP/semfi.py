#encoding: utf-8
import mikatools
import os
from .uralicApi import __find_writable_folder, __model_base_folders, ModelNotFound
import sqlite3
from collections import defaultdict

semfi_urls = "https://mikakalevi.com/whereis_semfi.json"

__connections = {}

def supported_languages():
	urls = mikatools.download_json(semfi_urls)
	return urls.keys()

def download(lang,show_progress=True):
	urls = mikatools.download_json(semfi_urls)
	if lang not in urls:
		raise "Language not supported. Currently supported languages " + ", ".join(urls.keys())
	download_to = os.path.join(__find_writable_folder(__model_base_folders()), lang)
	if not os.path.exists(download_to):
		os.makedirs(download_to)
	save_to = os.path.join(download_to, "sem.db")
	print("Downloading: "+ lang)
	mikatools.download_file(urls[lang], save_to, show_progress)

def __where_semfi(lang, safe=False):
	folders = __model_base_folders()
	for folder in folders:
		try_file = os.path.join(os.path.join(folder, lang), "sem.db")
		e = os.path.exists(try_file)
		if e:
			return try_file
	if safe:
		return None
	raise ModelNotFound()

def is_language_installed(language):
	path = __where_semfi(language, True)
	if path is None:
		return False
	return True

def __get_connection(lang):
	if lang in __connections:
		return __connections[lang]
	else:
		db_file = __where_semfi(lang)
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		__connections[lang] = c
		return c

def __column_headers(lang, table):
	if table == "words":
		hs = ["id", "word", "pos", "frequency", "relative_frequency"]
		if lang == "fin":
			hs.append("compund")
		else:
			hs.append("mwe")
	else:
		hs = ["word1", "word2", "relation", "frequency", "relative_frequency", "zscore"]
	return hs

def __add_titles(rows, lang, table):
	keys = __column_headers(lang, table)
	ret = []
	for row in rows:
		d = {}
		for i in range(len(row)):
			d[keys[i]] = row[i]
		ret.append(d)
	return ret

def __replace_by_word_object(word1, word2, relations, lang):
	c = __get_connection(lang)
	if word2 is not None:
		for relation in relations:
			relation["word1"] = word1
			relation["word2"] = word2
		return relations
	else:
		for relation in relations:
			relation["word1"] = word1
			relation["word2"] = get_word_by_id(relation["word2"], lang)
		return relations

def get_word(lemma, pos, lang):
	c = __get_connection(lang)
	c.execute('SELECT * FROM words WHERE word="'+lemma+'" and pos="' + pos +'"')
	all_rows = c.fetchall()
	rows = __add_titles(all_rows, lang, "words")
	if len(rows) > 0:
		return rows[0]
	else:
		return None

def get_word_by_id(id, lang):
	c = __get_connection(lang)
	c.execute('SELECT * FROM words WHERE id="'+id+'"')
	all_rows = c.fetchall()
	rows = __add_titles(all_rows, lang, "words")
	if len(rows) > 0:
		return rows[0]
	else:
		return None

def get_words(lemma, lang):
	c = __get_connection(lang)
	c.execute('SELECT * FROM words WHERE word="'+lemma+'"')
	all_rows = c.fetchall()
	return __add_titles(all_rows, lang, "words")

def get_all_relations(word_object, lang, sort=False, search_by_word2=False):
	sorting = ""
	if sort:
		sorting = " ORDER BY frequency DESC"
	c = __get_connection(lang)
	n = "1"
	if search_by_word2:
		n = "2"
	c.execute('SELECT * FROM relations WHERE word'+n+'="'+word_object["id"]+'"'+sorting)
	all_rows = c.fetchall()
	all_rows = __add_titles(all_rows, lang, "relations")
	rows = __replace_by_word_object(word_object, None, all_rows, lang)
	return rows

def get_by_relation(word_object, relation, lang, sort=False, search_by_word2=False):
	sorting = ""
	if sort:
		sorting = " ORDER BY frequency DESC"
	c = __get_connection(lang)
	n = "1"
	if search_by_word2:
		n = "2"
	c.execute('SELECT * FROM relations WHERE word'+n+'="'+word_object["id"]+'" and relation_name="' + relation +'"'+sorting)
	all_rows = c.fetchall()
	all_rows = __add_titles(all_rows, lang, "relations")
	rows = __replace_by_word_object(word_object, None, all_rows, lang)
	return rows

def get_by_word(word_object1, word_object2, lang, sort=False):
	sorting = ""
	if sort:
		sorting = " ORDER BY frequency DESC"
	c = __get_connection(lang)
	c.execute('SELECT * FROM relations WHERE word1="'+word_object1["id"]+'" and word2="' + word_object2["id"] +'"'+sorting)
	all_rows = c.fetchall()
	all_rows = __add_titles(all_rows, lang, "relations")
	rows = __replace_by_word_object(word_object1, word_object2, all_rows, lang)
	return rows

def get_by_word_and_relation(word_object1, word_object2, relation, lang, sort=False):
	sorting = ""
	if sort:
		sorting = " ORDER BY frequency DESC"
	c = __get_connection(lang)
	c.execute('SELECT * FROM relations WHERE word1="'+word_object1["id"]+'" and word2="' + word_object2["id"] +'" and relation_name="' + relation +'"'+sorting)
	all_rows = c.fetchall()
	all_rows = __add_titles(all_rows, lang, "relations")
	rows = __replace_by_word_object(word_object1, word_object2, all_rows, lang)
	return rows

def realtion_frequency(relations):
	rels = defaultdict(int)
	for relation in relations:
		rels[relation["relation"]] += relation["frequency"]
	return rels


def sort_by_frequency(lang, ascending=True, number=None, format=True):
	sort = "DESC"
	if ascending:
		sort = "ASC"
	c = __get_connection(lang)
	c.execute("SELECT * FROM words ORDER BY frequency " + sort)
	if number == None:
		all_rows = c.fetchall()
	else:
		all_rows = c.fetchmany(number)
	if format:
		return __add_titles(all_rows, lang, "words")
	else:
		return all_rows

