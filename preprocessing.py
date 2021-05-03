import sys
import csv

# input_file is a file that should be read
# mode is either train or test
# extract is either title or article
# Return type: test - list of string, train - list of tuple (tuple = (category string, content string))
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

def main():
    input_file = sys.argv[1]
    mode = sys.argv[2]
    extract = sys.argv[3]

    print(preprocess(input_file, mode, extract))

if __name__ == "__main__":
    main()




