"""
This is a more complex example on performing clustering on large scale dataset.

This examples find in a large set of sentences local communities, i.e., groups of sentences that are highly
similar. You can freely configure the threshold what is considered as similar. A high threshold will
only find extremely similar sentences, a lower threshold will find more sentence that are less similar.

A second parameter is 'min_community_size': Only communities with at least a certain number of sentences will be returned.

The method for finding the communities is extremely fast, for clustering 50k sentences it requires only 5 seconds (plus embedding comuptation).

In this example, we download a large set of questions from Quora and then find similar questions in this set.
"""
from spacy.symbols import nsubj, dobj, NOUN, VERB
import spacy
from sentence_transformers import SentenceTransformer, util
import os
import csv
import time
import json


def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency > counter):
            counter = curr_frequency
            num = i

    return num


# Model for computing sentence embeddings. We use one trained for similar questions detection
model = SentenceTransformer('all-MiniLM-L6-v2')

# Spacy model for tagging
nlp = spacy.load("en_core_web_sm")

# Lemmanizer for finding roots of words
# lem = nlp.add_pipe("lemmatizer", config={"mode": "lookup"})

# We donwload the Quora Duplicate Questions Dataset (https://www.quora.com/q/quoradata/First-Quora-Dataset-Release-Question-Pairs)
# and find similar question in it
# url = "http://qim.fs.quoracdn.net/quora_duplicate_questions.tsv"
dataset_path = "datasets/quora_duplicate_questions.tsv"
max_corpus_size = 20000  # We limit our corpus to only the first 50k questions


# Check if the dataset exists. If not, download and extract
# Download dataset if needed
# if not os.path.exists(dataset_path):
#     print("Download dataset")
#     util.http_get(url, dataset_path)

# Get all unique sentences from the file
# corpus_sentences = set()
# with open(dataset_path, encoding='utf8') as fIn:
#     data = json.load(fIn)
#     data
#     for row in data:
#         corpus_sentences.add(row['question1'])
#         corpus_sentences.add(row['question2'])
#         if len(corpus_sentences) >= max_corpus_size:
#             break

def load_corpus(dataset_path, max_corpus_size):
    corpus_sentences = set()
    with open(dataset_path, encoding='utf8') as fIn:
        reader = csv.DictReader(fIn, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            corpus_sentences.add(row['question1'])
            corpus_sentences.add(row['question2'])
            if len(corpus_sentences) >= max_corpus_size:
                break

    return list(corpus_sentences)


def encode_corpus(corpus):
    print("Encoding the corpus. This might take a while")
    corpus_embeddings = model.encode(
        corpus, batch_size=64, show_progress_bar=True, convert_to_tensor=True)
    return corpus_embeddings


# print("Start clustering")
# start_time = time.time()

# Two parameters to tune:
# min_cluster_size: Only consider cluster that have at least 25 elements
# threshold: Consider sentence pairs with a cosine-similarity larger than threshold as similar


def find_clusters_ids(embeddings):
    print("Start clustering")

    start_time = time.time()
    clustersIds = util.community_detection(
        embeddings, min_community_size=20, threshold=0.75)
    print("Clustering done after {:.2f} sec".format(time.time() - start_time))
    return clustersIds


# print("Clustering done after {:.2f} sec".format(time.time() - start_time))


def find_clusters_sentences(corpus):
    clustersIds = find_clusters_ids(encode_corpus(corpus))
    clusters = []
    for i, clusterId in enumerate(clustersIds):
        clusters.append([])
        for sentence_id in clusterId:
            clusters[i].append(corpus[sentence_id])
    return clusters


def extract_intents(clusters):
    action_object_list = []
    # print('clusters:', len(clusters))
    for cluster in clusters:
        doc = nlp('\n'.join(cluster))
        is_questions = []
        actions = []
        objects = []
        for possible_subject in doc:
            if possible_subject.dep == dobj and possible_subject.pos == NOUN and possible_subject.head.pos == VERB:
                # action_object_list.add(possible_subject.head.lemma_.lower() +
                #                        '-' + possible_subject.lemma_.lower())
                actions.append(possible_subject.head.lemma_.lower())
                objects.append(possible_subject.lemma_.lower())
        # print('actions:', len(actions))
        # print('objects:', len(objects))
        if len(actions) == len(objects):
            if len(actions) > 0:
                action_object_list.append(most_frequent(
                    actions) + '-' + most_frequent(objects))
            else:
                action_object_list.append('undefined')
    return action_object_list


corpus = load_corpus(dataset_path=dataset_path,
                     max_corpus_size=max_corpus_size)
clusters_sentences = find_clusters_sentences(corpus)
clusters_intents = extract_intents(clusters_sentences)
# print('sentences:', len(clusters_sentences))
# print('intents', len(clusters_intents))
for i in range(len(clusters_intents)):
    if clusters_intents[i] == 'undefined':
        continue
    for sentence in clusters_sentences[i]:
        print(sentence, '|', clusters_intents[i], '\n')
# print(extract_intents(clusters_sentences))
# for i in range(len(actions)):
#     print(actions[i], '-', objects[i])
