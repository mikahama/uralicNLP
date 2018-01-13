#encoding: utf-8
import re

class UD_collection():
	"""docstring for UD_collection"""
	def __init__(self, file_handle):
		sentence = []
		self.sentences = []
		for line in file_handle:
			if line == "\n":
				self.sentences.append(parse_sentence(sentence))
				sentence = []
			else:
				sentence.append(line.replace("\n", ""))

	def find_sentences(self, query={}, head_query={}, match_range_tokens = False, match_empty_nodes = False, return_root= False):
		results = []
		for sentence in self.sentences:
			r = sentence.find(query, head_query, match_range_tokens, match_empty_nodes)
			if return_root and len(r) > 0:
				results.append(sentence)
			else:
				results.extend(r)
		return results
		

class UD_relation():
	"""docstring for UD_relation"""
	def __init__(self, node, relation, head):
		self.node = node
		self.head = head
		self.relation = relation
		if head is not None:
			head.children.append(self)
		node.head = self

		

class UD_node():
	"""docstring for UD_node"""
	def __init__(self, id, form, lemma, upostag, xpostag, feats, misc):
		self.id = id
		self.form = form 
		self.lemma = lemma
		self.upostag = upostag
		self.xpostag = xpostag
		self.feats = feats
		self.misc = misc
		self.head = None
		self.children = []

	def find(self, query={}, head_query={}, match_range_tokens = False, match_empty_nodes = False):
		results = []
		passed = True
		if (!match_range_tokens and "-" in self.id) or (!match_empty_nodes and "." in self.id):
			passed = False
		else:
			for key in query:
				attr = getattr(self, key)
				v = query[key]
				if isinstance(v, re._pattern_type):
					if v.match(attr) is None:
						passed = False
						break
				else:
					if v != attr:
						passed = False
						break
		
			head = self.head
			if head not is None:
				for key in head_query:
					attr = getattr(head, key)
					v = head_query[key]
					if isinstance(v, re._pattern_type):
						if v.match(attr) is None:
							passed = False
							break
					else:
						if v != attr:
							passed = False
							break
			elif head is None and len(head_query.keys()) >0:
				passed = False
		if passed:
			results.append(self)
		for child in self.children:
			r = child.find(query, head_query, match_range_tokens, match_empty_nodes)
			results.extend(r)
		return results


def parse_sentence(conll_u_sentence):
	if type(conll_u_sentence) == str or type(conll_u_sentence) == unicode:
		conll_u_sentence = conll_u_sentence.split("\n")
	nodes = {}
	relations = {}
	for annotation in conll_u_sentence:
		if annotation = "" or annotation.startswith("#"):
			continue
		parts = annotation.split("\t")
		node = UD_node(parts[0],parts[1],parts[2],parts[3],parts[4],parts[5],parts[9])
		nodes[parts[0]] = node
		relations[parts[0]] = [parts[6],parts[7],parts[8]]
	root = None
	for id in relations:
		relation = relations[id]
		head_id = relation[0]
		if head_id == "0":
			root = nodes[id]
			continue
		head_relation = UD_relation(nodes[id], relation[1], nodes[head_id])
		o_rel = relation[2]
		if o_rel == u"_":
			o_rel = ""
		other_relations = o_rel.split("|")
		head_rel = head_id + ":" + relation[1]
		for other_relation in other_relations:
			if other_relation == head_rel:
				continue
			other_parts = other_relation.split(":")
			r = UD_relation(nodes[other_parts[0]], other_parts[1], nodes[id])
	return root
