#encoding: utf-8
from uralicNLP import semfi

def print_for(word, pos, rel, target_pos):
	wo = semfi.get_word(word, pos, "fin")
	ws =semfi.get_by_relation(wo, rel, "fin", sort=True)
	for w in ws:
		if w["word2"] is not None and w["word2"]["pos"] == target_pos:
			print w["word2"]["word"]



#print_for("punainen","A", "amod", "N")
wo = semfi.get_word("kettu", "N", "fin")
print semfi.get_all_relations(wo, "fin")
#print semfi.get_by_word_and_relation(semfi.get_word("karhu", "N", "fin"), semfi.get_word("olla", "V", "fin"), "nsubj", "fin")