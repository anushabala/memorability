#Written by: Anusha Balakrishnan
#Date: 4/23/14
import os
import pickle
import string
import urllib2
import nltk
from nltk.stem.snowball import SnowballStemmer
from bs4 import BeautifulSoup

class ProfanityChecker:
    def __init__(self, relative_path= "./"):
        self.PROFANE_FILE_PATH = '%sprofane_words.pkl' % relative_path
        self.SLANG_FILE_PATH = '%sslang_words.pkl' % relative_path
        self.slang_set = set()
        self.profane_set = set()
        self.stemmer = SnowballStemmer("english")
        self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        if os.path.isfile(self.PROFANE_FILE_PATH):
            self.profane_set = pickle.load(file(self.PROFANE_FILE_PATH, 'rb'))
        else:
            profane_file = file('%sprofanity.txt' % relative_path, 'r')
            line = profane_file.readline()
            while line:
                self.profane_set.add(line.strip())
                stem = self.stemmer.stem(line.strip())
                self.profane_set.add(stem)
                line = profane_file.readline()
            profane_file.close()
            pickle.dump(self.profane_set, file(self.PROFANE_FILE_PATH, 'wb'))

        if os.path.isfile(self.SLANG_FILE_PATH):
            self.slang_set = pickle.load(file(self.SLANG_FILE_PATH, 'rb'))
        else:
            self.__get_all_slang()

    def __get_all_slang(self):

        for i in range(1,20):
            url = "http://www.manythings.org/slang/slang%d.html" % i
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page.read())
            words = soup.findAll('b')
            for eachword in words:
                contents = eachword.contents
                if len(contents)!=0:
                    word = contents[0].strip()
                    if ' ' not in word:
                        self.slang_set.add(word)
                        self.slang_set.add(self.stemmer.stem(word))
        pickle.dump(self.slang_set, file(self.SLANG_FILE_PATH, 'wb'))

    def is_quote_profane(self, quote):

        sentences = self.sent_detector.tokenize(quote.strip())

        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            for word in tokens:
                if word not in string.punctuation:
                    stem = self.stemmer.stem(word)
                    if word in self.profane_set or stem in self.profane_set:
                        return True
        return False

    def is_quote_colloquial(self, quote):
        sentences = self.sent_detector.tokenize(quote.strip())

        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            for word in tokens:
                if word not in string.punctuation:
                    stem = self.stemmer.stem(word)
                    if word in self.slang_set or stem in self.slang_set:
                        return True
        return False

    def get_profanity_freq(self, quote):
        freq = 0
        total_tokens = 0
        sentences = self.sent_detector.tokenize(quote.strip())
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            for word in tokens:
                if word not in string.punctuation:
                    total_tokens+=1
                    stem = self.stemmer.stem(word)
                    if word in self.profane_set or stem in self.profane_set:
                        freq+=1
        if total_tokens==0:
            total_tokens=1
        return (freq, total_tokens)

    def get_normalized_profanity(self, quote):
        (freq, tokens) = self.get_profanity_freq(quote)
        return float(freq)/tokens

def find_corpus_profanities(corpus_file, rejected):
    profanity_filter = ProfanityChecker()
    write_rejects = True
    if rejected==None:
        write_rejects = False
    not_profane = None
    if write_rejects:
        not_profane = file(rejected, 'w')
    corpus = file(corpus_file,'r')
    line = corpus.readline()
    profane = {'M':0, 'N':0}
    total= {'M':0, 'N':0}
    while line:
        line = line.strip().split('\t')
        quote = line[0].strip()
        mem = line[1].strip()
        if profanity_filter.is_quote_profane(quote):
            profane[mem]+=1
        elif write_rejects:
            not_profane.write(quote+'\n')
        total[mem]+=1
        if sum(total.values())%500==0:
            print "%d quotes processed." % sum(total.values())
        line = corpus.readline()


    print "PROFANE"
    print "Percent of memorable quotes profane: %f (%d of %d)" % (float(profane['M'])/total['M'], profane['M'], total['M'])
    print "Percent of non-memorable quotes profane: %f (%d of %d)" % (float(profane['N'])/total['N'], profane['N'], total['N'])
    corpus.close()
    if write_rejects:
        not_profane.close()

# Not a useful feature, just experimental
def find_corpus_colloquialisms(corpus_file, rejected):
    profanity_filter = ProfanityChecker()
    not_profane = file(rejected, 'w')
    corpus = file(corpus_file,'r')
    line = corpus.readline()
    profane = {'M':0, 'N':0}
    total= {'M':0, 'N':0}
    while line:
        line = line.strip().split('\t')
        quote = line[0].strip()
        mem = line[1].strip()
        if profanity_filter.is_quote_colloquial(quote):
            profane[mem]+=1
        else:
            not_profane.write(quote+'\n')
        total[mem]+=1
        if sum(total.values())%500==0:
            print "%d quotes processed." % sum(total.values())
        line = corpus.readline()

    print "PROFANE"
    print "Percent of memorable quotes colloquial: %f (%d of %d)" % (float(profane['M'])/total['M'], profane['M'], total['M'])
    print "Percent of non-memorable quotes colloquial: %f (%d of %d)" % (float(profane['N'])/total['N'], profane['N'], total['N'])
    corpus.close()
    not_profane.close()

def compare_corpus_profanity(corpus_file):
    profanity_filter = ProfanityChecker()
    corpus = file(corpus_file,'r')
    line = corpus.readline()
    mem_pairs = 0
    more_pairs = 0
    nonmem_pairs = 0
    total = 0
    while line:
        line = line.strip().split('\t')
        mem_quote = line[0].strip()
        line = corpus.readline()
        nonmem_quote = line[0].strip()
        (mem_freq, mem_tokens) = profanity_filter.get_profanity_freq(mem_quote)
        (nonmem_freq, nonmem_tokens) = profanity_filter.get_profanity_freq(nonmem_quote)
        mem_norm = float(mem_freq)/mem_tokens
        nonmem_norm = float(nonmem_freq)/nonmem_tokens
        total+=1
        if mem_norm > nonmem_norm:
            mem_pairs += 1
        elif nonmem_norm > mem_norm:
            nonmem_pairs += 1
        if profanity_filter.is_quote_profane(mem_quote) and not profanity_filter.is_quote_profane(nonmem_quote):
            more_pairs +=1
        if total%500==0:
            print "%d pairs processed." % total

        line = corpus.readline()
    print "Percentage of pairs where the memorable quote is " \
          "more profane than the non-memorable quote: %f" % (float(mem_pairs)/total)
    print "Percentage of pairs where the non-memorable quote is " \
          "more profane than the memorable quote: %f" % (float(nonmem_pairs)/total)
    print "Percentage of pairs where the memorable quote is " \
          "profane and the memorable quote isn't: %f" % (float(more_pairs)/total)
# corpus = '../quotes.dat'
# rejected = 'rejected_colloquial.dat'
# find_corpus_colloquialisms(corpus, rejected)
# find_corpus_profanities(corpus, None)
# compare_corpus_profanity(corpus)
