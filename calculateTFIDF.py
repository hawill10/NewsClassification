import sys
import nltk
import string
import math
import csv

nltk.download('stopwords')
nltk.download('punkt')

closedClassStopWords = [
  'a','the','an','and','or','but','about','above','after','along','amid','among',\
  'as','at','by','for','from','in','into','like','minus','near','of','off','on',\
  'onto','out','over','past','per','plus','since','till','to','under','until','up',\
  'via','vs','with','that','can','cannot','could','may','might','must',\
  'need','ought','shall','should','will','would','have','had','has','having','be',\
  'is','am','are','was','were','being','been','get','gets','got','gotten',\
  'getting','seem','seeming','seems','seemed',\
  'enough', 'both', 'all', 'your' 'those', 'this', 'these', \
  'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',\
  'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',\
  'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',\
  'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',\
  'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',\
  'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',\
  'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',\
  'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \
  'anything', 'anytime' 'anywhere', 'everybody', 'everyday',\
  'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',\
  'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',\
  'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\
  'you','your','yours','me','my','mine','I','we','us','much','and/or'
]

stopwords = set(list(nltk.corpus.stopwords.words('english')) + list(string.punctuation) + closedClassStopWords)

def insertToWordVector_IDF(line, wordvector):
  # Transform tokenized list to set for getting unique words
  for rawToken in set(nltk.word_tokenize(line.lower())):
    # Check if the token is not a stopword
    if rawToken not in stopwords:
      
      if rawToken not in wordvector:
        wordvector[rawToken] = 1
      else:
        wordvector[rawToken] += 1

def calculateIDF(wordVector, documentCount):
  for term in wordVector:
    count = wordVector[term]
    wordVector[term] = math.log(documentCount / count)

# -------------------------------------------------------

def insertToTrainingTFWordVector(categoryIndex, line, wordVectorDict):
  tempTFWordVector = {}

  if categoryIndex not in wordVectorDict:
    wordVectorDict[categoryIndex] = []

  for rawToken in nltk.word_tokenize(line.lower()):
    # Check if the token is not a stopword
    if rawToken not in stopwords:

      if rawToken not in tempTFWordVector:
        tempTFWordVector[rawToken] = 1
      else:
        tempTFWordVector[rawToken] += 1

  wordVectorDict[categoryIndex].append(tempTFWordVector)

def insertToTestTFWordVector(line, wordVectorList):
  tempTFWordVector = {}

  for rawToken in nltk.word_tokenize(line.lower()):
     # Check if the token is not a stopword
    if rawToken not in stopwords:

      if rawToken not in tempTFWordVector:
        tempTFWordVector[rawToken] = 1
      else:
        tempTFWordVector[rawToken] += 1

  wordVectorList.append(tempTFWordVector)


# -------------------------------------------------------

def getAverageTFIDFWordVector(tf_WordVecs, idf_WordVec):
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
        # Average TFIDF = [(Sum of TF) * IDF] / Size of Category Documents
        AverageTFIDF[categoryIndex][word] = (AverageTFIDF[categoryIndex][word] * idf_WordVec[word]) / categoryDocumentSize
      else:
        # If the term is not found, set to zero
        AverageTFIDF[categoryIndex][word] = 0

  return AverageTFIDF

def getTFIDFWordVector(tf_WordVecs, idf_WordVec):
  # Base Dict
  TFIDF = {}

  # 1. Loop through the TF word vectors
  for wordvector in tf_WordVecs:

    # 2. Calculate TFIDF for the words
    for word in idf_WordVec:
      if word in wordvector:
        TFIDF[word] = wordvector[word] * idf_WordVec[word]
      else:
        TFIDF[word] = 0

  return TFIDF



# -------------------------------------------------------

# TFIDF Calculator Function
def calculateTFIDF(inputList, mode):
  """
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
      insertToWordVector_IDF(row[1], IDF_WordVector)
      insertToTrainingTFWordVector(int(row[0]), row[1], Training_TF_WordVectors)

    # Calculate IDF
    calculateIDF(IDF_WordVector, docCount)

    # Calculate Average TFIDF
    Training_TFIDF_WordVectors = getAverageTFIDFWordVector(Training_TF_WordVectors, IDF_WordVector)

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

    Test_TFIDF_WordVectors = getTFIDFWordVector(Test_TF_WordVectors, IDF_WordVector)

    print("==================================")
    print("Unique Word Count in IDF Word Vec:")
    print(len(IDF_WordVector))
    print("==================================")

    return Test_TFIDF_WordVectors

  else:
    return None

# ============================================================ #

def preprocess(input_file, mode, extract):
  if extract == "title":
      content_index = 0
  elif extract == "article":
      content_index = 1
  else:
      print("extract should be either title or article")
      exit(0)

  output = []
  if mode == "train":
      content_index += 1
      
      with open(input_file, 'r') as file:
          reader = csv.reader(file)

          for row in reader:
              output.append((row[0], row[content_index]))
  elif mode == "test":
      with open(input_file, 'r') as file:
          reader = csv.reader(file)

          for row in reader:
              output.append(row[content_index])
  else:
      print("mode should be either train or test")
      exit(0)

  return output

# TEST WITH PREPROCESSING
input_file = sys.argv[1]
mode = sys.argv[2]
extract = sys.argv[3]

input_data = preprocess(input_file, mode, extract)

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