__author__ = 'Rituparna'
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
import nltk

infile = 'create_datasets/quotes.dat'
stopwords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your']

def preprocess(sentence):
    tokens=tokenize(sentence)
    lcased=lowercase(tokens)
    stpwremoved=stopwordremoval(lcased)
    return stpwremoved

def tokenize(sentence):      #sentence is of string type
    result=wordpunct_tokenize(sentence)
    return result


def lowercase(tokens):
    sent_l=[]
    for word in tokens:
        sent_l.append(word.lower())
    return sent_l

def stopwordremoval(lcased):
    filtered_word_list = lcased[:]         # make a copy of the word_list
    for word in lcased:                    # iterate over word_list
        if word in stopwords:
            filtered_word_list.remove(word) # remove word from filtered_word_list if it is a stopword
    return filtered_word_list

def get_repetitions():
    mem_repeat = 0
    nonmem_repeat = 0
    mem_repeat_pair = 0
    nonmem_repeat_pair = 0
    non_mem=0
    mem_pair=0
    with open(infile, 'r') as f:
        for line in f:
            count = 0
            tokens = preprocess(line.strip().split('\t')[0])
            if(line.strip().split('\t')[1]=='M'):
                for token in tokens:
                    count= tokens.count(token)
                    if count > 1:
                        mem_repeat +=1
                        mem_pair = 1
                        break

                #NER feature
                pos_tags = nltk.pos_tag(tokens)
                print nltk.ne_chunk(pos_tags, binary=True)
            else:
                for token in tokens:
                    count= tokens.count(token)
                    if count > 1:
                        nonmem_repeat +=1
                        non_mem = 1
                        break
                if mem_pair ==1 and non_mem == 0 :
                    mem_repeat_pair +=1
                elif mem_pair==0 and non_mem ==1:
                    nonmem_repeat_pair +=1
                mem_pair = 0
                non_mem = 0


    f.close()
    print "Number of Memorable qoutes with repetitions:", mem_repeat/float(1790)
    print "Number of Non-Memorable qoutes with repetitions:", nonmem_repeat/float(1790)

    print "*-----------------PAIR STATISTICS----------------*"
    print "Number of Memorale quotes with repetitions in pairs:", mem_repeat_pair/float(1790)
    print "Number of Memorale quotes with repetitions in pairs:", nonmem_repeat_pair/float(1790)

get_repetitions()