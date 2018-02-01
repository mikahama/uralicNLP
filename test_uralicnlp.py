#encoding: utf-8
from uralicNLP import uralicApi
from uralicNLP.cg3 import Cg3


print(uralicApi.supported_languages())

#uralicApi.download("fin")

print(uralicApi.analyze("voita", "fin"))

print(uralicApi.generate("käsi+N+Sg+Par", "fin"))

print(uralicApi.dictionary_search("car", "sms"))

print(uralicApi.lemmatize("voita", "fin"))

"""

uralicApi.download("kpv")

cg = Cg3("fin")
print(cg.disambiguate(["Kissa","voi","nauraa"]))


cg = Cg3("kpv")
print(cg.disambiguate("театрӧ пыран абонемент".split(" ")))
"""