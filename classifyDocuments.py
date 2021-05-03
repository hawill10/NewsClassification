import math

train = {
    1: {'a': 0.1, 'b': 0.3, 'c': 0, 'd': 0.7, 'e': 0},
    2: {'a': 0, 'b': 0.2, 'c': 0.2, 'd': 0.3, 'e': 0.6},
    3: {'a': 0.3, 'b': 0.2, 'c': 0.1, 'd': 0.7, 'e': 0.6},
    4: {'a': 0.2, 'b': 0, 'c': 0.2, 'd': 0.3, 'e': 0.1},
    5: {'a': 0.1, 'b': 0.1, 'c': 0.1, 'd': 0.2, 'e': 0.3},
    }
    
test = [{'c': 0.2, 'd': 0.4, 'e': 0.1, 'f': 1}]

# calculate cosine similarity of two word vectors
def cosine_similarity(vector_a, vector_b):
    numerator = 0
    denominator_a = 0
    denominator_b = 0
    for word in vector_a.keys():
        denominator_a += vector_a[word]**2
        if word not in vector_b:
            pass
        else:
            numerator += vector_a[word]*vector_b[word]
            denominator_b += vector_b[word]**2

    similarity = numerator / (math.sqrt(denominator_a)*math.sqrt(denominator_b))
    # print("numerator: {}, denominator: {}, {}".format(numerator, math.sqrt(denominator_a), math.sqrt(denominator_b)))

    return similarity

def classify(unclassified_doc_vectors, category_word_vectors):
    classified = []
    for document in unclassified_doc_vectors:
        category = 0
        max_similarity = 0
        for cat in range(1,6):
            similarity = cosine_similarity(category_word_vectors[cat], document)
            if similarity >= max_similarity:
                max_similarity = similarity
                category = cat
        classified.append(category)
    
    return classified
    
print(classify(test, train))
