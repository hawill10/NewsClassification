import sys
import csv
import math
import preprocessing

# from https://gist.github.com/sebleier/554280
stop_words = ["0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above",
              "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj",
              "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against", "ah",
              "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also",
              "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another",
              "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao", "ap",
              "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar", "are", "aren",
              "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "au",
              "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "b1", "b2", "b3", "ba", "back",
              "bc", "bd", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand",
              "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides",
              "best", "better", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom",
              "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call",
              "came", "can", "cannot", "cant", "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly",
              "cf", "cg", "ch", "changes", "ci", "cit", "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come",
              "comes", "con", "concerning", "consequently", "consider", "considering", "contain", "containing",
              "contains", "corresponding", "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry",
              "cs", "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de",
              "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't",
              "different", "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "down",
              "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each",
              "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven",
              "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er",
              "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody",
              "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "f2", "fa",
              "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "first", "five",
              "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth",
              "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy",
              "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl",
              "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had",
              "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't",
              "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby",
              "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid", "him",
              "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit", "however", "how's", "hr",
              "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic",
              "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll", "im", "i'm", "immediate",
              "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", "index", "indicate",
              "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "invention",
              "inward", "io", "ip", "iq", "ir", "is", "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's",
              "itself", "iv", "i've", "ix", "iy", "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep",
              "keeps", "kept", "kg", "kj", "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last",
              "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets",
              "let's", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look",
              "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes",
              "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn",
              "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly",
              "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n",
              "n2", "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "necessary",
              "need", "needn", "needn't", "needs", "neither", "never", "nevertheless", "new", "next", "ng", "ni",
              "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor",
              "normally", "nos", "not", "noted", "nothing", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o",
              "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj",
              "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq",
              "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours", "ourselves", "out",
              "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page",
              "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per",
              "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly",
              "possible", "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably",
              "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py",
              "q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re",
              "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless",
              "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted",
              "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt",
              "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying", "says", "sc", "sd",
              "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems",
              "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "sf", "shall",
              "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should", "shouldn", "shouldn't",
              "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant", "significantly",
              "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so",
              "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat",
              "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr",
              "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently",
              "suggest", "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb",
              "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that",
              "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence",
              "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere",
              "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll",
              "theyre", "they're", "they've", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly",
              "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru",
              "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward",
              "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "t's", "tt", "tv",
              "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under",
              "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us",
              "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value",
              "various", "vd", "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs",
              "vt", "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd",
              "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't", "we've",
              "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", "when's", "where",
              "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether",
              "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever",
              "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing", "wish", "with", "within",
              "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would", "wouldn", "wouldnt",
              "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv",
              "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're",
              "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz"]


# remove unnecsary parts of each string of the query/doc
def process(arr):
    # punctuation to be removed
    punctuation = ['(', ')', '?', ':', ';', ',', '.', '!', '/', '"', "'", "-", '\\', '$', '#']

    for i in range(0, len(arr)):
        # split each word
        str = arr[i].split(' ')

        # remove any stop words
        for j in str[:]:
            if j.lower() in stop_words:
                str.remove(j)

        # rejoin str
        new_str = " ".join(str)

        # remove any punctuation
        for k in punctuation:
            while k in new_str:
                new_str = new_str.replace(k, '')

        # remove any numbers
        for l in new_str:
            if l.isdigit():
                new_str = new_str.replace(l, '')

        # remove any extra spaces
        str = new_str.split(" ")
        while '' in str:
            str.remove('')

        for z in str:
            if len(z) <= 2:
                str.remove(z)

        arr[i] = str

    return arr


# function to calculate the tf scores
def tf(doc):
    tf = []
    for sent in doc:
        tf_sent = []

        for word in sent:
            c = 0
            for k in sent:
                if word.lower() == k.lower():
                    c += 1

            res = c / len(sent)
            tf_sent.append(res)

        tf.append(tf_sent)

    return tf


def unique_words(doc):
    uniq = {}

    for sent in doc:
        temp = " ".join(sent)
        temp = temp.lower()
        sent = temp.split()

        uniqlist = []
        [uniqlist.append(x) for x in sent if x not in uniqlist]

        for word in uniqlist:
            if word.lower() in uniq:
                uniq[word.lower()] += 1
            else:
                uniq[word.lower()] = 1
    return uniq


# function to calculate idf for every sentence in the document
def idf(doc, uniq):
    idf = []
    docl = len(doc)

    for sent in doc:
        idf_sent = []
        for word in sent:
            score = math.log(docl / uniq[word.lower()])
            idf_sent.append(score)

        idf.append(idf_sent)

    return idf


# function to calculate the tf-idf scores.
def tfidf(tf, idf):
    tfidf = [[0 for j in range(len(tf[i]))] for i in range(len(tf))]
    for i in range(len(tf)):
        for j in range(len(tf[i])):
            tfidf[i][j] = tf[i][j] * float(idf[i][j])
    return tfidf


def tag(doc, uniq):
    tagged = []
    vec = tfidf(tf(doc), idf(doc, uniq))

    for i in range(len(doc)):
        tempdict = {}
        sent = doc[i]
        for j in range(len(sent)):
            tempdict[sent[j].lower()] = vec[i][j]
        tagged.append(tempdict)

    return tagged

def threshold(arr):
    for dict in arr:
        mean = sum(dict.values()) / len(dict)
        for key in dict.copy():
            if dict[key] < mean:
                del dict[key]

    return arr

def parset(input_file, mode, extract):
    answer = []
    arr = []

    processed_list = preprocessing.preprocess(input_file, mode, extract)

    if mode == "train":
        for row in processed_list:
            answer.append(row[0])
            arr.append(row[1])
    elif mode == "test":
        for row in processed_list:
            answer = 0
            arr.append(row)

    return answer, arr

def extract_keywords(input_file, mode, extract):
    output = []
    answer, arr = parset(input_file, mode, extract)
    arr = process(arr)
    # print(arr[0:5])
    uniq = unique_words(arr)
    arr = tag(arr, uniq)
    # print(arr[0:5])
    arr = threshold(arr)
    # print(arr[0:5])
    if answer:
        for line in range(len(answer)):
            keywords = " ".join(list(arr[line].keys()))
            output.append((answer[line], keywords))
    else:
        for line in range(len(arr)):
            keywords = " ".join(list(arr[line].keys()))
            output.append(keywords) 

    return output


def main():
    input_file = sys.argv[1]
    mode = sys.argv[2]
    extract = sys.argv[3]

    output = extract_keywords(input_file, mode, extract)
    output.sort()

    w = open("keyword_list", "w")

    for line in output:
        w.write(line + "\n")

if __name__ == "__main__":
    main()

