from mcp.server.fastmcp import FastMCP
from . import uralicApi
from . import string_processing


mcp = FastMCP("Uralic Language Processor (UralicMCP)")

@mcp.tool()
def analyze_word(word: str, language_iso_code: str) -> list:
	"""Analyzes a word in a supported language and returns a list of analysis. Each analysis consists of a lemma and morphological tags such as kissa, N, Sg, Nom"""
	return [", ".join(x[0].split("+")) for x in uralicApi.analyze(word, language_iso_code)]


@mcp.tool()
def morphological_segmentation(word: str, language_iso_code: str) -> list:
	"""Splits a word into morphemes. Returns a list of lists given that sometimes a word can be understood in multiple ways"""
	return uralicApi.segment(word, language_iso_code)

@mcp.tool()
def inflect_word(inflection: str, language_iso_code: str)  -> list:
	"""Inflects a lemma to a given form. The inflection parameter must have the entire morphological reading such as koira+N+Sg+Gen to output koiran. NB there can be multiple forms for the same inflection"""
	return [x[0] for x in uralicApi.generate(inflection, language_iso_code)]

@mcp.resource("dictionary://{lemma}/{source_language_iso}/{target_language_iso}")
def dictionary_lookup(lemma:str, source_language_iso:str, target_language_iso) -> list:
	"""Finds target language translations for a lemma in source language. The language codes are ISO codes. NB these dictionaries are for endangered languages. They mostly have translations from an endangered language to Finnish, Russian or English. There are no dictionaries between two endangered languages."""
	return uralicApi.get_translation(lemma, source_language_iso, target_language_iso)

@mcp.resource()
def list_supported_languages() -> dict:
	"""Lists supported languages, their names and ISO codes. Use this if you don't know the ISO code.  """
	sup = {x: [(z, string_processing.iso_to_name(z)) for z in y ] for x, y in uralicApi.supported_languages().items() }
	del sup["cg"]
	return sup

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
