import sys
import string
import math
import csv
import preprocessing

def insertToWordVector_IDF(tokens, wordvector):
  # Transform tokenized list to set for getting unique words
  for rawToken in tokens:
      if rawToken == '':
        continue

      if rawToken not in wordvector:
        wordvector[rawToken] = 1
      else:
        wordvector[rawToken] += 1

def calculateIDF(wordVector, documentCount):
  for term in wordVector:
    count = wordVector[term]
    wordVector[term] = math.log(documentCount / count)

# -------------------------------------------------------

def insertToTrainingTFWordVector(categoryIndex, tokens, wordVectorDict):
  tempTFWordVector = {}

  if categoryIndex not in wordVectorDict:
    wordVectorDict[categoryIndex] = []

  for rawToken in tokens:
    if rawToken == '':
      continue

    if rawToken not in tempTFWordVector:
      tempTFWordVector[rawToken] = 1
    else:
      tempTFWordVector[rawToken] += 1

  wordVectorDict[categoryIndex].append(tempTFWordVector)

def insertToTestTFWordVector(tokens, wordVectorList):
  tempTFWordVector = {}

  for rawToken in tokens:
    if rawToken not in tempTFWordVector:
      tempTFWordVector[rawToken] = 1
    else:
      tempTFWordVector[rawToken] += 1

  wordVectorList.append(tempTFWordVector)

# -------------------------------------------------------

def getAverageTFIDFWordVector(tf_WordVecs, idf_WordVec, includeWeights, weightVal, keywords):
  # Base Dict
  AverageTFIDF = {}

  # Loop through the categories in the TF Word Vector
  for categoryIndex in tf_WordVecs:
    AverageTFIDF[categoryIndex] = {}

    # Length of the Documents in a category
    categoryDocumentSize = len(tf_WordVecs[categoryIndex])

    # 1. Sum all the TFs and place it in the AverageTFIDF Dict
    for wordvector in tf_WordVecs[categoryIndex]:
      for word in wordvector:
        if word in AverageTFIDF[categoryIndex]:
          AverageTFIDF[categoryIndex][word] += wordvector[word]
        else:
          AverageTFIDF[categoryIndex][word] = wordvector[word]
    
    # 2. Calculate Average TFIDF in-place
    for word in idf_WordVec:
      if word in AverageTFIDF[categoryIndex]:
        if includeWeights and (word in keywords):
          TF_Sum = AverageTFIDF[categoryIndex][word] * weightVal
        else:
          TF_Sum = AverageTFIDF[categoryIndex][word]

        # Average TFIDF = [(Sum of TF) * IDF] / Size of Category Documents
        AverageTFIDF[categoryIndex][word] = (TF_Sum * idf_WordVec[word]) / categoryDocumentSize
      else:
        # If the term is not found, set to zero
        AverageTFIDF[categoryIndex][word] = 0

  return AverageTFIDF

def getTFIDFWordVector(tf_WordVecs, idf_WordVec, includeWeights, weightVal, keywords):
  # Base Dict
  # TFIDF = {}
  TFIDFWordVecs = []

  # 1. Loop through the TF word vectors
  for wordvector in tf_WordVecs:
    TFIDF = {}
    # 2. Calculate TFIDF for the words
    for word in idf_WordVec:
      if word in wordvector:
        if includeWeights and (word in keywords):
          TFIDF[word] = (wordvector[word] * weightVal) * idf_WordVec[word]
        else:
          TFIDF[word] = wordvector[word] * idf_WordVec[word]
      else:
        TFIDF[word] = 0
    TFIDFWordVecs.append(TFIDF)
    

  return TFIDFWordVecs



# -------------------------------------------------------

# TFIDF Calculator Function
def calculateTFIDF(inputList, mode, includeWeights = False, weightVal = 1, keywords = []):
  """
  Option:
    - Include Weights using Keywords
    - Keywords is given as a list of keywords
    - The TF of keywords are multiplied by the weight value

  Training Mode Output:
    - Dict with Category Index as its key and Average TF-IDF Word Vector Dict as value

  Test Mode Output:
    - List of TF-IDF Word Vector Dicts
    - The index of the dict is the line number of the input-file

  """
  IDF_WordVector = {}

  # Number of Documents
  docCount = len(inputList)

  # ------------------------------------------------------------- # 
  # Mode: Training
  # Input Structure: List of Tuples (categoryIndex, contentString)
  # ------------------------------------------------------------- #
  if mode == 'train':

    # Training TF WordVector Container Structure:
    #   - Dictionary with category-index as its keys and list of TF word-vectors for its value
    Training_TF_WordVectors = {}

    # Loop through the inputList to add to IDF Word Vector
    for row in inputList:
      print(row[0], row[1])
      print(type(row[1]))
      insertToWordVector_IDF(row[1], IDF_WordVector)
      insertToTrainingTFWordVector(int(row[0]), row[1], Training_TF_WordVectors)

    # Calculate IDF
    calculateIDF(IDF_WordVector, docCount)

    # Calculate Average TFIDF
    Training_TFIDF_WordVectors = getAverageTFIDFWordVector(Training_TF_WordVectors, IDF_WordVector, includeWeights, weightVal, keywords)

    print("==================================")
    print("Unique Word Count in IDF Word Vec:")
    print(len(IDF_WordVector))
    print("==================================")

    return Training_TFIDF_WordVectors
  
  # ------------------------------------------------------------- #
  # Mode: Test
  # Input Structure: List of Strings
  # ------------------------------------------------------------- #
  elif mode == 'test':
    # Test TF WordVector Container Structure:
    #   - List of Document TF Word Vectors
    Test_TF_WordVectors = []

    # Loop through the inputList to add to IDF Word Vector
    for row in inputList:
      insertToWordVector_IDF(row, IDF_WordVector)
      insertToTestTFWordVector(row, Test_TF_WordVectors)

    # Calculate IDF
    calculateIDF(IDF_WordVector, docCount)

    Test_TFIDF_WordVectors = getTFIDFWordVector(Test_TF_WordVectors, IDF_WordVector, includeWeights, weightVal, keywords)

    print("==================================")
    print("Unique Word Count in IDF Word Vec:")
    print(len(IDF_WordVector))
    print("==================================")

    return Test_TFIDF_WordVectors

  else:
    return None

# ============================================================ #

if __name__ == "__main__":
  # TEST WITH PREPROCESSING
  input_file = sys.argv[1]
  mode = sys.argv[2]
  extract = sys.argv[3]

  input_data = preprocessing.preprocess(input_file, mode, extract)

  result = calculateTFIDF(input_data, mode)

  # TEST OUPUT
  test_output = open('TFIDF_TEST_OUTPUT', 'w+')


  if mode == 'train':
    for categoryIndex in result:
      for word in result[categoryIndex]:
        test_output.write("Category: {0}  Avg. TFIDF: {2}   Word: {1}\n".format(
          categoryIndex,
          word,
          result[categoryIndex][word]
        ))

  if mode == 'test':
    for i, wordvector in enumerate(result):
      for word in wordvector:
        test_output.write("Line #: {0}  TFIDF: {2}    Word: {1}\n".format(
          i,
          word,
          wordvector[word]
        ))

  test_output.close()