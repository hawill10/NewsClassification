import sys
import nltk
import string
import math
import csv

closed_class_stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',\
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

nltk.download('stopwords')
nltk.download('punkt')
stopwords = list(nltk.corpus.stopwords.words('english')) + list(string.punctuation)

print(stopwords)

train_file = open(sys.argv[1], "r")

categoryLineCount = {}

titleTermFreq = {}
titleTFIDF = {}
descriptionTermFreq = {}
descriptionTFIDF = {}

def getTermFrequency(line):
    termFrequency = {}

    for rawToken in nltk.word_tokenize(line.lower()):
        if rawToken not in closed_class_stop_words and rawToken not in stopwords:
            if rawToken in termFrequency:
                termFrequency[rawToken] += 1
            else:
                termFrequency[rawToken] = 1
    
    return termFrequency

def insertToTermFreqObj(line):
    categoryIndex = int(line[0])
    
    # Record to track the number of documents for a certain category
    if categoryIndex in categoryLineCount:
        categoryLineCount[categoryIndex] += 1
    else:
        categoryLineCount[categoryIndex] = 1
    
    # Get Term Frequencies of the document
    titleStr = line[1]
    titleDocTermFreq = getTermFrequency(titleStr)

    descriptionStr = line[2]
    descriptionDocTermFreq = getTermFrequency(descriptionStr)

    # Loop through tokens found in the title
    for token in titleDocTermFreq:
        # If category index is not in title-term-freq object, create an object
        if categoryIndex not in titleTermFreq:
            titleTermFreq[categoryIndex] = {}

        # If the token is not in title-term-freq object, create an array
        # The size of the array will be the number of documents that the token was found within the category
        if token not in titleTermFreq[categoryIndex]:
            titleTermFreq[categoryIndex][token] = []

        titleTermFreq[categoryIndex][token].append(titleDocTermFreq[token])

    # Loop through tokens found in the description
    for token in descriptionDocTermFreq:
        if categoryIndex not in descriptionTermFreq:
            descriptionTermFreq[categoryIndex] = {}

        if token not in descriptionTermFreq[categoryIndex]:
            descriptionTermFreq[categoryIndex][token] = []

        descriptionTermFreq[categoryIndex][token].append(descriptionDocTermFreq[token])

def TFIDF(termFreqObj, outputFile):
    TFIDF = {}
    # Calculate TFIDF of each term
    for categoryIndex in termFreqObj:
        TFIDF[categoryIndex] = {}

        for term in termFreqObj[categoryIndex]:
            TFIDF[categoryIndex][term] = []

            for tf in termFreqObj[categoryIndex][term]:
                idf = math.log(categoryLineCount[categoryIndex] / len(termFreqObj[categoryIndex][term]))
                tf_idf = tf * idf

                TFIDF[categoryIndex][term].append(tf_idf)

                # Write to file for logging TFIDFs
                # 1. Category Index
                # 2. Number of Documents in the category
                # 3. 
                outputFile.write("{0} {1} {2} {3} {4} {5}\n".format(
                    categoryIndex,
                    categoryLineCount[categoryIndex],
                    term,
                    tf,
                    len(termFreqObj[categoryIndex][term]),
                    idf
                ))
    
    outputFile.close()
    return TFIDF

output_titleTFIDF = open('title', 'w+')
output_descriptionTFIDF = open('description', 'w+')

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        insertToTermFreqObj(row)

# Get TFIDF and write to file
titleTFIDF = TFIDF(titleTermFreq, output_titleTFIDF)
descriptionTFIDF = TFIDF(descriptionTermFreq, output_descriptionTFIDF)

csv_file.close()