import sys
import calculateTFIDF
import classifyDocuments
import keyword_extractor

if __name__ == "__main__":
    training_file = sys.argv[1]
    test_file = sys.argv[2]
    extract = sys.argv[3]

    training_input_keywords = keyword_extractor.extract_keywords(training_file, "train", extract)
    test_input_keywords = keyword_extractor.extract_keywords(test_file, "test", extract)

    category_vectors = calculateTFIDF.calculateTFIDF(training_input_keywords, "train")
    unclassified_docs = calculateTFIDF.calculateTFIDF(test_input_keywords, "test")

    output = classifyDocuments.classify(unclassified_docs, category_vectors)

    with open('output', 'w') as o:
        for ans in output:
            o.write(str(ans) + "\n")