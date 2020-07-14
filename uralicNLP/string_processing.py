#encoding: utf-8
from __future__ import unicode_literals
import re, unicodedata
import mikatools

isos = mikatools.json_load(mikatools.script_path("lang_codes.json"))

pattern = re.compile(r'(\w[\u02F3\u0300\u2013\u032E\u208D\u203F\u0311\u0323\u035E\u031C\u02FC\u030C\u02F9\u0328\u032D:\u02F4\u032F\u0330\u035C\u0302\u0327\u03572\u0308\u0351\u0304\u02F2\u0352\u0355\u00B7\u032C\u030B\u2019\u0339\u00B4\u0301\u02F1\u0303\u0306\u030A7\u0325\u0307\u0354`\u02F0]+|\w|\W)', re.UNICODE | re.IGNORECASE)

def char_split(word):
	word = unicodedata.normalize('NFKC',word)
	_result = pattern.findall(word)
	return list(_result)

def filter_arabic(text, keep_vowels=True, combine_by=""):
	if keep_vowels:
		return combine_by.join(re.findall(r"[ء-ي'ًٌٍَُِّْـ']+", text))
	else:
		return combine_by.join(re.findall(r"[ء-ي]+", text))
		
def iso_to_name(iso):
    return isos[iso]