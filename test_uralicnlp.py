#encoding: utf-8
from uralicNLP import uralicApi
print uralicApi.supported_languages()

print uralicApi.analyze("voita", "fin")

print uralicApi.generate("käsi+N+Sg+Par", "fin")

print uralicApi.dictionary_search("car", "sms")

print uralicApi.lemmatize("voita", "fin")