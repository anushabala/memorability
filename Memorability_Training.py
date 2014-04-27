import create_training_corpus as ctc
import pprint
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
stopwords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'your']

class Train():
    def __init__(self):
        self.memQuotes={}
        self.nonmemQuotes={}
        self.featureList=['Unigram','Bigram']
        self.unigrams=[]
        self.bigrams=[]
        self.trainfile =  'create_datasets/fv_train'
        self.trainparsed = 'create_datasets/train'#'quotes.dat'
        self.testfile    = 'create_datasets/fv_dev'
        self.testparsed  = 'create_datasets/dev'
        self.lastIndex   =0

    #def readfile(self,filename, outputfile):
    #    ctc.getMovieCorpusContents(filename,outputfile)

    
    def buildQuoteDictionaries(self, filename):
        datafile=open(filename)#('data.dat')
        self.lines=datafile.readlines()
        for line in self.lines:
            quoteandtag=line.strip().split('\t')
            if(quoteandtag[1]=='M'):
                self.memQuotes[quoteandtag[0]]=1
            else:
                self.nonmemQuotes[quoteandtag[0]]=1
    
    def tokenize(self,sentence):      #sentence is of string type
        tokens=[]
        result=wordpunct_tokenize(sentence)
        return result

    def stem(self,stpwremoved):
        stemmer = PorterStemmer()
        plurals = stpwremoved
        singles=[]
        for plural in plurals:
            singles.append(stemmer.stem(plural))
        return singles
        
    def lowercase(self,tokens):
        sent_l=[]
        for word in tokens:
            sent_l.append(word.lower())
        return sent_l
        
    def stopwordremoval(self,lcased):
        filtered_word_list = lcased[:]         # make a copy of the word_list
        for word in lcased:                    # iterate over word_list
            if word in stopwords: 
                filtered_word_list.remove(word) # remove word from filtered_word_list if it is a stopword
        return filtered_word_list
    
    def preprocess(self,sentence):
        tokens=self.tokenize(sentence)
        lcased=self.lowercase(tokens)
        stpwremoved=self.stopwordremoval(lcased)
        ftokens=self.stem(stpwremoved)
        return ftokens        
        
    def buildFeatureFile(self, filename, path, fold):
        feature_file = path+str(fold)+".dat"
        with open(feature_file, 'w') as fw:
            f=open(filename,'r')
            quotecount=0
            for line in self.lines:
                st=''
                quote=line.strip().split('\t')[0]
                if(line.strip().split('\t')[1]=='M'):
                    #st+='1 '
                    st+='1'
                else:
                    #st+='0 '
                    st+='0'
                tokens=self.preprocess(quote)

                #Other Lexical and Synatctic features
                fv = {}
                self.lastIndex = 0
                self.lastIndex= self.getLastIndex()
                fv = self.add_extra_features(fv, tokens)

                #Form the feature vector with unigram, bigram, trigram tokens
                bigramTokens= ' '
                trigramTokens= ' '
                for i in range(0,len(tokens)):
                    token=tokens[i]
                    if (token in self.unigrams):
                        unigramIndex= self.unigrams.index(token)+1
                        unigramCount= tokens.count(token)
                        fv.update({unigramIndex:unigramCount})
                    if i <= len(tokens)-2:
                        bigram=tokens[i]+'_'+tokens[i+1]
                        bigramTokens+=' '+bigram
                        if i<= len(tokens)-3:
                            trigram=tokens[i]+'_'+tokens[i+1]+'_'+tokens[i+2]
                            trigramTokens+=' '+trigram

                #Create feature vectors with the bigram features
                bigramTokens = bigramTokens.split()
                for token in bigramTokens:
                    if(token in self.unigrams):
                        bigramIndex= self.unigrams.index(token)+1
                        bigramCount= bigramTokens.count(token)
                        fv.update({bigramIndex:bigramCount})

                #Create feature vectors with the trigram features
                trigramTokens = trigramTokens.split()
                for token in trigramTokens:
                    if(token in self.unigrams):
                        trigramIndex= self.unigrams.index(token)+1
                        trigramCount= trigramTokens.count(token)
                        fv.update({trigramIndex:trigramCount})

                #Sort the features by index
                for key in sorted(fv):
                    st+=' '+str(key)+":"+str(fv[key])

                #Write the feature vector to te file
                fw.write(st+"\n")

                quotecount+=1
            f.close()
        fw.close()
        
    def buildFeatureDictionaries(self):
        for line in self.lines:
            tokens=self.preprocess(line)
            #Store unigrams
            for token in tokens:
                self.unigrams.append(token)
            #Create bigrams and Trigrams separated by '_' and store in the feature list
            #The unigrams, bigrams and trigrams feature list is kept same to ease the process fo creating the Feature Vectors
            for i in range(0,len(tokens)-1):
                bigram = tokens[i]+"_"+tokens[i+1]
                self.unigrams.append(bigram)
                if (i < len(tokens) - 2):
                    trigram = tokens[i]+'_'+tokens[i+1]+'_'+tokens[i+2]
                    self.unigrams.append(trigram)

    def getLastIndex(self):
        return len(self.unigrams)

    def add_extra_features(self, fv,tokens):
        #Length Feature of the quote
        qoute_len = len(tokens)
        self.lastIndex+=1
        fv.update({self.lastIndex:qoute_len})

        #Check for presence of 'you' in the quotes
        self.lastIndex+=1
        if (tokens.count("you") > 0):
            value = 1
        else:
            value =0
        fv.update({self.lastIndex:value})
        return fv

#     def computeBigramCounts(self):
    
    #Reading the training file and creating the feature vector for that
    #train.readfile(train.trainfile,train.trainparsed)

for fold in range(1,6):
    train=Train()
    train_file = train.trainparsed+str(fold)+".dat"
    train.buildQuoteDictionaries(train_file)
    train.buildFeatureDictionaries()
    train.buildFeatureFile(train_file, train.trainfile, fold)#(train.trainfile)

    test_file = train.testparsed+str(fold)+".dat"
    train.buildQuoteDictionaries(test_file)
    train.buildFeatureFile(test_file, train.testfile, fold )

