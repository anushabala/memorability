#Written by: Ashima Arora
#Date: 4/24/2014
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
stopwords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your']

def tokenize(sentence):      #sentence is of string type
    tokens=[]
    result=wordpunct_tokenize(sentence)
    return result

def removeStopWords(tokens):
    words = tokens
    for sword in stopwords:
        if(sword in tokens):
            words.remove(sword)
    return words

def lowercase(tokens):
    sent_l=[]
    for word in tokens:
        sent_l.append(word.lower())
    return sent_l

def removePunctuations(sentence):
    puncts = '?!,-_.:;\',",'
    for punct in puncts:
        if(punct in sentence):
            sentence = sentence.replace(punct,'')
    return sentence

def getTokens(quote):
    quote = removePunctuations(quote)
    tokens = tokenize(quote)
    tokens = lowercase(tokens)
    # tokens = removeStopWords(tokens)
    return tokens

def getPreprocessedQuote(quote):
    return " ".join(getTokens(quote))

def hasRhyme(words,k=3):
    # words = getTokens(quote)
    # print getPreprocessedQuote(quote),': ',mem,': '
    # for i in range(0,len(words)-1):
    #     curr_word = words[i]
    #     next_word = words[i+1]
    #     if(curr_word[-k:]==next_word[-k:]):
    #         print 'Rhyme!'
    #         return 1 
    # return 0

    rhyme={}
    for word in words:
        if(word[-k:] in rhyme and len(word[-k:])>=k):
            # print 'RHYME!!', '  ', word[-k:]
            return 1
        else:
            rhyme[word[-k:]] = 1
    return 0

def checkRhyme():
    corpus = file('../quotes.dat', 'r')
    line = corpus.readline()
    A_present = {'M':0, 'N':0}
    A_absent = {'M':0, 'N':0}
    total = {'M':0, 'N':0}
    k = 3
    while line:
        line = line.split('\t')
        sentence = line[0]
        mem = line[1].strip()
        hasR = hasRhyme(sentence, mem, k)
        if(hasR == 1):
            A_present[mem] = A_present[mem] + 1
        else:
            A_absent[mem] = A_absent[mem] + 1
        total[mem] = total[mem] + 1
        line = corpus.readline()
    print "MEMORABLE QUOTES"
    print "Percent with Rhyme: %f" % (float(A_present['M'])/total['M'])
    print "Percent without Rhyme: %f" % (float(A_absent['M'])/total['M'])

    print "NON-MEMORABLE QUOTES"
    print "Percent with Rhyme: %f" % (float(A_present['N'])/total['N'])
    print "Percent without Rhyme: %f" % (float(A_absent['N'])/total['N'])
checkRhyme()