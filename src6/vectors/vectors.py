import numpy as np
from scipy.spatial.distance import cosine

with open("words.txt", encoding="utf-8") as f:
    words = {}
    for line in f:
        row = line.split()
        word = row[0]
        vector = np.array([float(x) for x in row[1:]])
        words[word] = vector


def distance(w1, w2):
    return cosine(w1, w2)


def closest_words(embedding):
    distances = {w: distance(embedding, emb) for w, emb in words.items()}
    return sorted(distances, key=distances.get)[:10]


def closest_word(embedding):
    return closest_words(embedding)[0]
