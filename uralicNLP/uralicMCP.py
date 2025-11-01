from mcp.server.fastmcp import FastMCP
from . import uralicApi
from . import string_processing


mcp = FastMCP("Uralic Language Processor (UralicMCP)")

@mcp.tool()
def analyze_word(word: str, language_iso_code: str) -> list:
	"""Analyzes a word in a supported language and returns a list of analysis. Each analysis consists of a lemma and morphological tags such as kissa+N+Sg+Nom"""
	return [x[0] for x in uralicApi.analyze(word, language_iso_code.lower())]


@mcp.tool()
def morphological_segmentation(word: str, language_iso_code: str) -> list:
	"""Splits a word into morphemes. Returns a list of lists given that sometimes a word can be understood in multiple ways. E.g. koiranikin koira, ni, kin"""
	return uralicApi.segment(word, language_iso_code.lower())

@mcp.tool()
def inflect_word(inflection: str, language_iso_code: str)  -> list:
	"""Inflects a lemma to a given form. The inflection parameter must have the entire morphological reading such as koira+N+Sg+Gen to output koiran. NB there can be multiple forms for the same inflection"""
	return [x[0] for x in uralicApi.generate(inflection, language_iso_code.lower())]

@mcp.tool()
def lemmatize(word: str, language_iso_code: str)  -> list:
	"""Lemmatizes a word in a given language. For example, voin in Finnish returns voi and voida"""
	return uralicApi.lemmatize(word, language_iso_code.lower())

@mcp.tool()
def dictionary_lookup(lemma:str, source_language_iso:str, target_language_iso:str):
	"""Finds target language translations for a lemma in source language. Target language can also be set to "all" for translations in all languages. The language codes are ISO codes. It's recommended to get translations for all languages."""
	if target_language_iso == "all" or target_language_iso is None:
		target_language_iso = None
	else:
		target_language_iso = target_language_iso.lower()
	return uralicApi.get_translation(lemma, source_language_iso, target_language_iso)

@mcp.tool()
def list_supported_languages() -> dict:
	"""Lists supported languages, their names and ISO codes. Use this if you don't know the ISO code.  """
	sup = {x: [(z, string_processing.iso_to_name(z)) for z in y ] for x, y in uralicApi.supported_languages().items() }
	del sup["cg"]
	return sup

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
