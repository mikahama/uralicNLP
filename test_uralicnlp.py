#encoding: utf-8
from uralicNLP import uralicApi
from uralicNLP.cg3 import Cg3, Cg3Pipe
from uralicNLP.translate import *
from uralicNLP import dependency
from uralicNLP.ud_tools import UD_collection
from uralicNLP.dictionary_backends import MongoDictionary
import re
from mikatools import *

from uralicNLP.llm import get_llm, disambiguate_sentence
from uralicNLP import semantics

#print(uralicApi.get_all_forms("kissa", "N", "fin"))

#uralicApi.get_transducer("spa", analyzer=True).lookup_optimize()

"""
print(uralicApi.analyze("segiz", "kaa"))
print(uralicApi.analyze("barchamizga", "uzb"))
print(uralicApi.analyze("como", "spa"))
print(uralicApi.generate("perro<n><m><sg>", "spa"))
print(uralicApi.generate("segiz<num><subst><nom>+e<cop><aor><p3><pl>", "kaa"))
print(uralicApi.lemmatize("como", "spa"))
print(uralicApi.lemmatize("segiz", "kaa"))
print(uralicApi.lemmatize("segiz", "kaa",word_boundaries=True))
"""

#print(type(uralicApi.get_transducer("spa", analyzer=True)))
#print()
#print(uralicApi.supported_languages())

#uralicApi.download("fin")
"""
print(uralicApi.analyze("voita", "fin"))
print(uralicApi.analyze("voita", "fin", descriptive=False))
print(uralicApi.analyze("voita", "fin"))
print(uralicApi.analyze("voita", "fin", descriptive=False))



print(uralicApi.generate("käsi+N+Sg+Par", "fin"))
print(uralicApi.generate("käsi+N+Sg+Par", "fin"))
print(uralicApi.generate("käsi+N+Sg+Par", "fin", descriptive=True))
print(uralicApi.generate("käsi+N+Sg+Par", "fin", descriptive=True))
print(uralicApi.generate("käsi+N+Sg+Par", "fin", dictionary_forms=False))
print(uralicApi.generate("käsi+N+Sg+Par", "fin", dictionary_forms=False))

print(uralicApi.generate("käsi+N+Sg+Par", "deu"))

#print(uralicApi.dictionary_search("car", "sms"))

print(uralicApi.lemmatize("voita", "fin", descriptive=True))


#uralicApi.download("kpv")

"""
"""
cg = Cg3("fin")
print(cg.disambiguate(["Kissa","voi","nauraa", "."], descriptive=True))


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


#print(uralicApi.analyze("kissat", "fin"))
#print(uralicApi.generate("koira+N+Pl+Nom", "fin"))

#print(uralicApi.segment("luutapiirinikin", "fin"))

#print(uralicApi.analyze("on", ["fin","olo"]))
#print(uralicApi.analyze("on", ["fin","olo"], language_flags=True))
"""
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

"""
ud = UD_collection(open_read("test_data/fi_test.conllu"))
sentences = ud.find_sentences(query={"lemma": "olla"}) #finds all sentences with the lemma kissa

for sentence in sentences:
    word = sentence.find(query={"lemma": "olla"})
    print(word[0].get_attribute("form"))



print(uralicApi.analyze("hörpähdin", "fin", neural_fallback=True, n_best=10))
print(uralicApi.lemmatize("nirhautan", "fin", neural_fallback=True, n_best=10))
print(uralicApi.generate("hömpötti+N+Sg+Gen", "fin", neural_fallback=True, n_best=10))
print(uralicApi.generate("koirailla+V+Act+Ind+Prs+Sg1", "fin", neural_fallback=True, n_best=10))
print(uralicApi.analyze("juoksen", "fin", neural_fallback=True))

"""

#print(uralicApi.get_translation("piânnai", "sms", "fin",backend=MongoDictionary))
#uralicApi.import_dictionary_to_db("sms")

#llm = get_llm("chatgpt", open_read(os.path.expanduser("~/.openaiapikey")).read().strip())
llm = get_llm("gemini", open_read(os.path.expanduser("~/.geminiapikey")).read().strip())
#llm = get_llm("mistral", open_read(os.path.expanduser("~/.mistralapikey")).read().strip())

#llm = get_llm("perplexity", open_read(os.path.expanduser("~/.perplexityapikey")).read().strip())
#llm = get_llm("claude", open_read(os.path.expanduser("~/.claudeapikey")).read().strip())

print(llm.prompt_video("What is happening on this video?", "/Users/mikahama/Downloads/6830385-uhd_4096_2160_25fps.mp4"))

#print(llm.prompt_image("What is this image about?", "/Users/mikahama/Desktop/teams.jpg"))

#print(llm.prompt("I forgot where I put my hat..."))

#llm.set_system_prompt("You are an evil monkey that likes to steal hats.")
#print("_____-----______")

#print(llm.prompt("I forgot where I put my hat..."))

#result, llm_output = disambiguate_sentence("Ёртозь ёртовсь кудостонть.", "myv", "fin", llm)
#print(result)
#print(llm_output)
#llm = get_llm("mistral", open_read(os.path.expanduser("~/.mistralapikey")).read().strip(), model="mistral-embed")
#llm = get_llm("roneneldan/TinyStories-33M")
#llm.load_cache("cache.bin")
#"microsoft/Phi-3.5-mini-instruct")
#prompts = ["What is Livonian?", "Look at this dog", "WTF are you talking about", "Yeah, right"]
#for prompt in prompts:
#	print(llm.prompt(prompt))
#	llm.embed(prompt)

#llm.save_cache("cache.bin")


#llm = get_llm("claude", open_read(os.path.expanduser("~/.claudeapikey")).read().strip())
#print(llm.prompt("What is Tundra Nenets?")) 

#llm = get_llm("voyage", open_read(os.path.expanduser("~/.voyageapikey")).read().strip())
#print(llm.embed("Super great text to embed")[:10])

#print(llm.embed_endangered("Näʹde täävtõõđi âʹtte peeʹlljid pärnnses täävtõõđi.", "sms", "fin"))
#llm = get_llm("google-bert/bert-base-uncased")
#texts = ["dogs are funny", "cats play around", "cars go fast", "planes fly around", "parrots like to eat", "eagles soar in the skies", "moon is big", "saturn is a planet"]
#endangered_texts = ["Ёртозь ёртовсь кудостонть.", "Теке сялгонзояк те касовксонть арасть.", "Истяяк арсеват.", "Атякштне, кунсолан, сыргойсть омбоцеде.", "Вальмаванть неявить ульцява ардыцят.", "Морат эрзянь моро?"]
#print(semantics.cluster(texts, llm, method="hdbscan"))
#print(semantics.cluster(texts, llm))
#print(semantics.cluster(texts, llm, hierarchical_clustering=True))
#print(semantics.cluster_endangered(endangered_texts, llm, "myv", "fin"))
#print(semantics.cluster_endangered(endangered_texts, llm, "myv", "fin", hierarchical_clustering=True, method="hdbscan"))

#t = TartuTranslator()
#print(t.translate("Hello, how are you?", "eng", "fin"))

#llm = get_llm("chatgpt", open_read(os.path.expanduser("~/.openaiapikey")).read().strip(), model="omni-moderation-latest")
#print(llm.moderate("those faggots punched idiots and fucked each other."))


