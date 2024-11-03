from sklearn.cluster import AffinityPropagation
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def _get_matrix(embeddings):
	m = []
	embeddings = [np.array(e).reshape(1, -1) for e in embeddings]
	for em in embeddings:
		r = []
		for e in embeddings:
			r.append(cosine_similarity(em, e)[0][0])
		m.append(r)
	return m

def _centroid(vecs):
	return np.mean(vecs, axis=0)

def _semantic_clusters(embeddings, group=True):
	m = np.array(_get_matrix(embeddings))
	agg = AffinityPropagation(affinity="precomputed")
	u = agg.fit_predict(m)
	if group:
		return _group_results(agg.labels_)
	else:
		return agg.labels_

def _group_results(labels):
	groups = []
	for x in range(len(set(labels))):
		groups.append([])
	for i, label in enumerate(labels):
		groups[label].append(i)
	return groups

def _cluster(embeddings, hierarchical_clustering):
	clusters = _semantic_clusters(embeddings)
	if not hierarchical_clustering:
		return clusters
	else:
		c_embeddings = embeddings
		c_map = clusters
		last_len = len(clusters)
		while True:
			c_embeddings = [_centroid([embeddings[v] for v in x]) for x in c_map]
			x_map = _semantic_clusters(c_embeddings, False)
			c_map = _semantic_clusters(c_embeddings, True)
			groups = []
			for x in range(len(set(x_map))):
				groups.append([])
			for i, label in enumerate(x_map):
				groups[label].append(clusters[i])
			clusters = groups
			l = len(clusters)
			if l == last_len:
				break
			else:
				last_len = l	
	return clusters


def _map_clusters(texts, clusters):
	for x in range(len(clusters)):
		c = clusters[x]
		if isinstance(c, list):
			_map_clusters(texts, c)
		else:
			clusters[x] = texts[c]

def cluster(texts, llm, return_ids=False, hierarchical_clustering=False):
	embeddings = [llm.embed(t) for t in texts]
	cs = _cluster(embeddings, hierarchical_clustering)
	if not return_ids:
		_map_clusters(texts, cs)
	return cs

def cluster_endangered(texts, llm, lang, dict_lang, return_ids=False, hierarchical_clustering=False):
	embeddings = [llm.embed_endangered(t, lang, dict_lang) for t in texts]
	cs = _cluster(embeddings, hierarchical_clustering)
	if not return_ids:
		_map_clusters(texts, cs)
	return cs
