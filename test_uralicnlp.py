#encoding: utf-8
from uralicNLP import uralicApi
from uralicNLP.cg3 import Cg3, Cg3Pipe
from uralicNLP.translate import *
from uralicNLP import dependency
from uralicNLP.dictionary_backends import MongoDictionary
import re

uralicApi.get_all_forms("kissa", "N", "fin")

uralicApi.get_transducer("spa", analyzer=True).lookup_optimize()
print(uralicApi.analyze("hola", "spa"))
print(type(uralicApi.get_transducer("spa", analyzer=True)))
print()
#print(uralicApi.supported_languages())

#uralicApi.download("fin")
"""
print(uralicApi.analyze("voita", "fin"))
print(uralicApi.analyze("voita", "fin", descrpitive=False))
print(uralicApi.analyze("voita", "fin"))
print(uralicApi.analyze("voita", "fin", descrpitive=False))



print(uralicApi.generate("käsi+N+Sg+Par", "fin"))
print(uralicApi.generate("käsi+N+Sg+Par", "fin"))
print(uralicApi.generate("käsi+N+Sg+Par", "fin", descrpitive=True))
print(uralicApi.generate("käsi+N+Sg+Par", "fin", descrpitive=True))
print(uralicApi.generate("käsi+N+Sg+Par", "fin", dictionary_forms=False))
print(uralicApi.generate("käsi+N+Sg+Par", "fin", dictionary_forms=False))

print(uralicApi.generate("käsi+N+Sg+Par", "deu"))

#print(uralicApi.dictionary_search("car", "sms"))

print(uralicApi.lemmatize("voita", "fin", descrpitive=True))


#uralicApi.download("kpv")

"""
"""
cg = Cg3("fin")
print(cg.disambiguate(["Kissa","voi","nauraa", "."], descrpitive=True))


cg = Cg3("kpv")
print(cg.disambiguate("театрӧ пыран абонемент".split(" ")))
"""

#print (uralicApi.lemmatize("livsmedel", "swe",force_local=True, word_boundaries=True))



"""
for w in ["الكتاب", "الكاتب", "الميكا", "المكتوب", "كلب", "كلبين", "كلاب", "كلبتي", "كلبي", "قلب", "قلبين"]:
	print("\n\n" +w)
	print(uralicApi.analyze(w,"ara"))
	print(uralicApi.lemmatize(w,"ara"))
print(uralicApi.generate("+noun+humanكاتب+masc+pl@","ara"))



str = "+adj{كَلْبِيّ}+masc+sg@"
print(re.findall(r"[ء-ي]+", str))

"""
"""
print(uralicApi.analyze("kissa", "fin"))
print(uralicApi.analyze("on", ["fin","olo"]))
print(uralicApi.analyze("on", ["fin","olo"], language_flags=True))

cg = Cg3("fin", morphology_languages=["fin", "olo"])
print(cg.disambiguate(["Kissa","on","kotona", "."], language_flags=True))
"""

"""
cg = Cg3("fin")
cg2 = Cg3("rus")

cg_pipe = Cg3Pipe(cg, cg2)
print(cg_pipe.disambiguate(["Kissa","on","kotona", "."]))
"""

#print(uralicApi.dictionary_lemmas("sms", group_by_pos=True))
#print(uralicApi.dictionary_search("car", "sms",backend=MongoDictionary))
#print(uralicApi.dictionary_search("byrokratti", "sms",backend=MongoDictionary))

#print(uralicApi.dictionary_search("tavallinen ihminen", "sms",backend=MongoDictionary))

"""
print(uralicApi.analyze("cats", "eng"))
print(uralicApi.generate("cat[N]+N+PL", "eng"))
print(uralicApi.lemmatize("cats", "eng"))

"""

"""

translator = ApertiumGiellateknoTranslator()
print(translator.translate("kissa juoksee kovaa", "fin","sme"))


translator = ApertiumStableTranslator()
print(translator.translate("el gato corre rápido", "spa","cat"))
"""
"""
ud = dependency.parse_text("kissa nauroi kovaa\nLehmä lauloi ainiaan", "fin",url="http://localhost:9877")
for sentence in ud:
	for word in sentence:
		print word.pos, word.lemma, word.get_attribute("deprel")
	print "---"
"""