import sys
import re
import pandas as pd
import numpy as np

def score (keyFileName, responseFileName):
    with open(keyFileName, 'r') as keyFile:
        key = keyFile.readlines()
    with open(responseFileName, 'r') as responseFile:
        response = responseFile.readlines()
    if len(key) != len(response):
        print("length mismatch between key and submitted file")
        exit()
    
    categories = ["World", "Sports", "Business", "Sci/Tech"]
    correct = 0
    incorrect = 0
    matrix = np.zeros((len(categories), len(categories)), dtype=np.int8)
    confusion_matrix = pd.DataFrame(matrix, columns=categories, index=categories)

    for i in range(len(key)):
        fields = re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", key[i].strip())
        ans = int(fields[0])
        res = int(response[i].strip())
        confusion_matrix.iloc[ans-1 ,res-1] += 1
        if ans == res:
            correct += 1
        else:
            incorrect += 1
            print("answer: {}, response: {}\ntitle: {}\narticle: {}\n".format(categories[ans-1], categories[res-1], fields[1], fields[2]))

    print("\nConfusion Matrix:")
    print(confusion_matrix)
    print("column=response, row=answer\n")
    print("Correct: {}".format(correct))
    print("Incorrect: {}".format(incorrect))
    print("Accuracy: {:.2f}".format(correct/(correct + incorrect)))

def main(args):
    key_file = args[1]
    response_file = args[2]
    score(key_file,response_file)

if __name__ == '__main__': sys.exit(main(sys.argv))