from .models import *
from .utils import *
from .config import CLEMB_KWARGS
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import argparse
import warnings
warnings.filterwarnings("ignore")


parser = argparse.ArgumentParser(description='Optional summarization arguments')
parser.add_argument(
		'--custom', 
		type=bool, 
		default=False,
		help='to halt provided example loading and enter user articles'
	)
args = parser.parse_args()

if args.custom:
	articles = []
	while True:
		inp = input('>>> ')
		if inp == 'exit':
			break
		else:
			articles.append(inp)

	sentences, words = make_data(articles)
	embeddings = sentence2embedding(sentences, EMBEDDING_MODEL)

	CUSTOM_CLEMB_KWARGS = {
		'clustering_algorithm': AgglomerativeClustering(
			n_clusters=None,
			distance_threshold=7
		),
		'embeddings': embeddings,
		'sentences': sentences,
		'words': words,
		'num_articles': len(articles)
	}

	clemb = ClusterSentenceEmbeddings(**CUSTOM_CLEMB_KWARGS)
	sentence_clusters = clemb.get_sentence_clusters()

	final_summary = ""
	for cluster in sentence_clusters:
		summary = bart_summarize(cluster, SUMMARIZATION_MODEL, SUMMARIZATION_TOKENIZER)
		final_summary += summary + " "

	print(final_summary)

else:
	clemb = ClusterSentenceEmbeddings(**CLEMB_KWARGS)
	sentence_clusters = clemb.get_sentence_clusters()

	final_summary = ""
	for cluster in sentence_clusters:
		summary = bart_summarize(cluster, SUMMARIZATION_MODEL, SUMMARIZATION_TOKENIZER)
		final_summary += summary + " "

	print(final_summary)