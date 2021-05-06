import math
import calculateTFIDF
import sys
import preprocessing

# train = {
#     1: {'a': 0.1, 'b': 0.3, 'c': 0, 'd': 0.7, 'e': 0},
#     2: {'a': 0, 'b': 0.2, 'c': 0.2, 'd': 0.3, 'e': 0.6},
#     3: {'a': 0.3, 'b': 0.2, 'c': 0.1, 'd': 0.7, 'e': 0.6},
#     4: {'a': 0.2, 'b': 0, 'c': 0.2, 'd': 0.3, 'e': 0.1},
#     5: {'a': 0.1, 'b': 0.1, 'c': 0.1, 'd': 0.2, 'e': 0.3},
#     }

# test = [{'c': 0.2, 'd': 0.4, 'e': 0.1, 'f': 1}]

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
    if numerator:
        similarity = numerator / (math.sqrt(denominator_a)*math.sqrt(denominator_b))
    else:
        similarity = 0
    # print("numerator: {}, denominator: {}, {}".format(numerator, math.sqrt(denominator_a), math.sqrt(denominator_b)))

    return similarity

def classify(unclassified_doc_vectors, category_word_vectors):
    classified = []
    for i, document in enumerate(unclassified_doc_vectors):
        print("classifying {}".format(i))
        category = 0
        max_similarity = 0
        for cat in range(1,5):
            similarity = cosine_similarity(category_word_vectors[cat], document)
            if similarity >= max_similarity:
                max_similarity = similarity
                category = cat
        classified.append(category)
    
    return classified
    
if __name__ == "__main__":
    training_file = sys.argv[1]
    test_file = sys.argv[2]
    extract = sys.argv[3]

    keywords = []
    with open("keyword_list", "r") as keyword_list:
        for word in keyword_list:
            keywords.append(word.strip())

    training_input = preprocessing.preprocess(training_file, "train", extract)
    test_input = preprocessing.preprocess(test_file, "test", extract)

    # calculateTFIDF(inputList, mode, includeWeights = False, weightVal = 1, keywords = [])


    category_vectors = calculateTFIDF.calculateTFIDF(training_input, "train", True, 1.5, keywords)
    unclassified_docs = calculateTFIDF.calculateTFIDF(test_input, "test", True, 1.5, keywords)


    output = classify(unclassified_docs, category_vectors)

    with open('output', 'w') as o:
        for ans in output:
            o.write(str(ans) + "\n")