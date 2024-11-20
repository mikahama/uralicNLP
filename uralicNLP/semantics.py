from sklearn.cluster import AffinityPropagation, HDBSCAN
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class NotSupportedException(Exception):
	pass


def _get_matrix(embeddings):
	m = []
	embeddings = [np.array(e).reshape(1, -1) for e in embeddings]
	for em in embeddings:
		r = []
		for e in embeddings:
			r.append(cosine_similarity(em, e)[0][0])
		m.append(r)
	return m

def similarity(e1, e2):
	e1 = np.array(e1).reshape(1, -1)
	e2 = np.array(e2).reshape(1, -1)
	return cosine_similarity(e1, e2)[0][0]

def _centroid(vecs):
	return np.mean(vecs, axis=0)

def _semantic_clusters(embeddings, group=True, method="affinity", **kwargs):
	if method == "affinity":
		return _affinity_clusters(embeddings, group=group, **kwargs)
	elif method == "hdbscan":
		return _hdbscan_clusters(embeddings, group=group, **kwargs)
	else:
		raise NotSupportedException("Method must be affinity or hdbscan")


def _hdbscan_clusters(embeddings, group=True, min_cluster_size=2, **kwargs):
	hdb = HDBSCAN(min_cluster_size=min_cluster_size, **kwargs)
	u = hdb.fit([np.array(e) for e in embeddings])
	if group:
		return _group_results(hdb.labels_)
	else:
		return hdb.labels_

def _affinity_clusters(embeddings, group=True, **kwargs):
	m = np.array(_get_matrix(embeddings))
	agg = AffinityPropagation(affinity="precomputed", **kwargs)
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

def _cluster(embeddings, hierarchical_clustering, method="affinity", **kwargs):
	clusters = _semantic_clusters(embeddings, method=method, **kwargs)
	if not hierarchical_clustering:
		return clusters
	else:
		c_embeddings = embeddings
		c_map = clusters
		last_len = len(clusters)
		while True:
			c_embeddings = [_centroid([c_embeddings[v] for v in x]) for x in c_map]
			if len(c_embeddings) == 1:
				break
			x_map = _semantic_clusters(c_embeddings, False, method=method)
			c_map = _semantic_clusters(c_embeddings, True, method=method)
			groups = []
			for x in range(len(set(x_map))):
				groups.append([])
			for i, label in enumerate(x_map):
				groups[label].append(clusters[i])
			clusters = groups
			l = len(clusters)
			if l == last_len or l ==1:
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

def cluster(texts, llm, return_ids=False, hierarchical_clustering=False, method="affinity", **kwargs):
	embeddings = [llm.embed(t) for t in texts]
	cs = _cluster(embeddings, hierarchical_clustering, method=method, **kwargs)
	if not return_ids:
		_map_clusters(texts, cs)
	return cs

def cluster_endangered(texts, llm, lang, dict_lang, return_ids=False, hierarchical_clustering=False, method="affinity", **kwargs):
	embeddings = [llm.embed_endangered(t, lang, dict_lang) for t in texts]
	cs = _cluster(embeddings, hierarchical_clustering, method=method, **kwargs)
	if not return_ids:
		_map_clusters(texts, cs)
	return cs
