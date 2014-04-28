#Written by: Anusha Balakrishnan
#Date: 4/24/14
# coding: utf-8
from collections import defaultdict
from math import log
import os
import pickle
from nltk.corpus import brown
from nltk.tokenize.treebank import TreebankWordTokenizer
import nltk


class BrownLanguageModel:
    def __init__(self, rel="./", pos_path=None, lex_path=None, rebuild=False):
        """
        Iniializes a BrownLanguageModel object that obtains POS and lexical N-gram counts
        and document frequencies from the Brown corpus.
        :param rel:     Defines the path of this module relative to the one using it. Defaults to "./" - current
                        directory.
        :param pos_path: Defaults to pos_ngrams.pkl. If specified, POS ngram counts are loaded from this path
                        if the path points to an existing file, and if the rebuild parameter is set to false.
                         If the file doesn't exist, N-gram counts are created and saved to this path.
        :param lex_path: Defaults to lex_grams.pkl. If specified, lexical ngram counts are loaded from this
                        path if the points to an existing file, and if the rebuild parameter is set to false.
                        If the file doesn't exist, N-gram counts are created and saved to this path.
        :param rebuild: Force rebuilds lexical and POS N-gram counts and saves them to either the default paths
                        or to paths as specified by the pos_path and lex_path parameters.
        """

        self.LEX_IDFS = '%sngram_lex_idfs.pkl' % rel
        self.POS_IDFS = '%sngram_pos_idfs.pkl' % rel
        self.POS_NGRAMS = '%spos_ngrams.pkl' % rel
        self.LEX_NGRAMS = '%slex_ngrams.pkl' % rel
        self.ngram_pos_count = defaultdict(int)
        self.ngram_lex_count = defaultdict(int)
        self.document_freqs_pos = defaultdict(int)
        self.document_freqs_lex = defaultdict(int)
        self.categories = ['news']
        self.CORPUS_SIZE = len(brown.tagged_sents(simplify_tags=True, categories=self.categories))

        if pos_path==None:
            pos_path = self.POS_NGRAMS
        if lex_path == None:
            lex_path = self.LEX_NGRAMS
        if not rebuild and os.path.isfile(pos_path) and os.path.isfile(lex_path):
            # self.ngram_pos_count = pickle.load(file(pos_path, 'rb'))
            # self.ngram_lex_count = pickle.load(file(lex_path, 'rb'))
            pass
        else:
            self.get_ngram_counts()
            pickle.dump(self.ngram_pos_count, file(pos_path, 'wb'))
            pickle.dump(self.ngram_lex_count, file(lex_path, 'wb'))


    def get_ngram_counts(self):
        print "Finding and storing N-gram counts"
        count=0
        target_corpus = brown.tagged_sents(simplify_tags=True, categories=self.categories)
        total = len(target_corpus)
        while count < total:
            sent = target_corpus[count]
            sent = self.__fix_tag_scheme(sent)
            sent = self.__add_start_end_tags(sent)

            num_tokens = len(sent)
            i = 0
            while i < num_tokens:

                this_tag = sent[i][1]
                this_word = sent[i][0].lower()
                self.ngram_pos_count[this_tag] += 1
                self.ngram_lex_count[this_word] += 1
                # print this_tag
                if i+1<num_tokens:
                    next_tag = sent[i+1][1]
                    next_word = sent[i+1][0]
                    if next_word!='STOP':
                        next_word = next_word.lower()
                    pos_key = "%s:%s" % (this_tag, next_tag)
                    lex_key = "%s:%s" % (this_word, next_word)
                    self.ngram_pos_count[pos_key] += 1
                    self.ngram_pos_count[lex_key] += 1
                if i+2 < num_tokens:
                    next_tag = sent[i+1][1]
                    next_word = sent[i+1][0]
                    third_tag = sent[i+2][1]
                    third_word = sent[i+2][0]
                    if third_word!='STOP':
                        third_word=third_word.lower()
                    pos_key = "%s:%s:%s" % (this_tag, next_tag, third_tag)
                    lex_key = "%s:%s:%s" % (this_word, next_word, third_word)
                    self.ngram_pos_count[pos_key] += 1
                    self.ngram_pos_count[lex_key] += 1
                i+=1

            count+=1
            if count%100==0:
                print "\tProgress: %d sentences" % count

    def __add_start_end_tags(self, tags):
        tags.insert(0, ('*', '*'))
        tags.append(('STOP', 'STOP'))
        return tags
    def load_doc_freqs(self, pos_path=None, lex_path=None, rebuild=False):

        if pos_path==None:
            pos_path = self.POS_IDFS
        if lex_path==None:
            lex_path = self.LEX_IDFS
        if not rebuild:
            self.document_freqs_pos = pickle.load(file(pos_path, 'rb'))
            self.document_freqs_lex= pickle.load(file(lex_path, 'rb'))
        else:
            print "Finding document frequencies.."
            target_corpus = brown.tagged_sents(simplify_tags=True, categories=self.categories)
            total = len(target_corpus)
            count = 0
            while count < total:
                sent = target_corpus[count]
                sent = self.__fix_tag_scheme(sent)
                sent = self.__add_start_end_tags(sent)
                num_tokens = len(sent)
                added_pos = []
                added_lex = []
                i = 0
                while i < num_tokens:
                    this_tag = sent[i][1]
                    this_word = sent[i][0].lower()
                    if this_tag not in added_pos:
                        self.document_freqs_pos[this_tag] += 1
                        added_pos.append(this_tag)
                    if this_word not in added_lex:
                        self.document_freqs_lex[this_word] += 1
                        added_lex.append(this_word)
                    if i+1<num_tokens:
                        next_tag = sent[i+1][1]
                        next_word = sent[i+1][0]
                        if next_word!='STOP':
                            next_word = next_word.lower()
                        pos_key = "%s:%s" % (this_tag, next_tag)
                        lex_key = "%s:%s" % (this_word, next_word)
                        if pos_key not in added_pos:
                            self.document_freqs_pos[pos_key] += 1
                            added_pos.append(pos_key)
                        if lex_key not in added_lex:
                            self.document_freqs_lex[lex_key] += 1
                            added_lex.append(lex_key)
                    if i+2 < num_tokens:
                        next_tag = sent[i+1][1]
                        next_word = sent[i+1][0].lower()
                        third_tag = sent[i+2][1]
                        third_word = sent[i+2][0]
                        if third_word!='STOP':
                            third_word=third_word.lower()
                        pos_key = "%s:%s:%s" % (this_tag, next_tag, third_tag)
                        lex_key = "%s:%s:%s" % (this_word, next_word, third_word)
                        if pos_key not in added_pos:
                            self.document_freqs_pos[pos_key] += 1
                            added_pos.append(pos_key)
                        if lex_key not in added_lex:
                            self.document_freqs_lex[lex_key] += 1
                            added_lex.append(lex_key)
                    i+=1

                count+=1
                if count%100==0:
                    print "\tProgress: %d sentences" % count
            pickle.dump(self.document_freqs_pos, file(pos_path, 'wb'))
            pickle.dump(self.document_freqs_lex, file(lex_path, 'wb'))

    def get_tf_idf_score(self, sentence, mode, ngram=1):
        if ngram not in range(1,4):
            try:
                raise ValueError
            except ValueError as v:
                print "Only unigrams, bigrams and trigrams are supported."
        if mode!="lex" and mode!="pos":
            try:
                raise ValueError
            except ValueError as v:
                print "Only lexical and POS distinctness supported."
        if len(self.document_freqs_lex.keys())==0 or len(self.document_freqs_pos.keys())==0:
            try:
                raise AttributeError
            except AttributeError as ae:
                print "Document frequency dictionaries not initialized. Call load_doc_freqs() " \
                      "on the LM object."
        tokenizer = TreebankWordTokenizer()
        sentence = sentence.lower()
        tokens = tokenizer.tokenize(sentence)
        tokens = self.__fix_tokens(tokens)
        tags = nltk.pos_tag(tokens)
        tags = self.__add_start_end_tags(tags)
        if mode=="lex":
            score = self.__get_lex_tf_idf(tags, ngram)
            return score
        else:
            score = self.__get_pos_tf_idf(tags, ngram)
            return score

    def __fix_tag_scheme(self, sentence):
        untagged = nltk.untag(sentence)
        new_tags = nltk.pos_tag(untagged)
        return new_tags
    def __fix_tokens(self, tokens):
        new_tokens = []
        i=0
        while i<len(tokens):
            this_token = tokens[i]
            if i+1 < len(tokens):
                next_token = tokens[i+1]
                if "'" in next_token and len(next_token)>1:
                    joint_token = "%s%s" % (this_token, next_token)
                    new_tokens.append(joint_token)
                    i+=1
                else:
                    new_tokens.append(this_token)
            i+=1
        return new_tokens

    def __get_lex_tf_idf(self, tags, ngram):
        # print tags
        total = len(tags)
        count = 0
        sentence_freqs = defaultdict(int)
        while count+(ngram-1) < total:
            key = ""
            for i in range(0,ngram):
                this_word = tags[count+i][0]
                key = "%s:%s" %(key, this_word)
            key = key.strip(':')
            sentence_freqs[key]+=1
            count +=1
        score = 0
        for key in sentence_freqs.keys():
            tf = float(sentence_freqs[key])/total
            # print self.CORPUS_SIZE, 1+self.document_freqs_pos[key]
            idf = log(float(self.CORPUS_SIZE)/(1+self.document_freqs_lex[key]))
            # print tf, idf
            score += (float(tf) * idf)

        return score

    def __get_pos_tf_idf(self, tags, ngram):
        total = len(tags)
        count = 0
        sentence_freqs = defaultdict(int)
        while count+(ngram-1) < total:
            key = ""
            for i in range(0,ngram):
                this_tag = tags[count+i][1]
                key = "%s:%s" %(key, this_tag)
            key = key.strip(':')
            # print "%s\t%d" % (key, self.document_freqs_pos[key])
            sentence_freqs[key]+=1
            count +=1

        score = 0
        for key in sentence_freqs.keys():
            tf = float(sentence_freqs[key])/total
            # print self.CORPUS_SIZE, 1+self.document_freqs_pos[key]
            idf = log(float(self.CORPUS_SIZE)/(1+self.document_freqs_pos[key]))
            # print tf, idf
            score += (float(tf) * idf)
        return score


# Add function to get the lex and synt log sum of tf-idfs for 1-, 2-, 3- grams of a sentence.
# compare log sum of mem to non-mem
# get stats
# establish threshold


def compare_tf_idf_scores():
    LM = BrownLanguageModel(rebuild=True)
    LM.load_doc_freqs(rebuild=True)
    corpus = file('../quotes.dat', 'r')
    line = corpus.readline()
    mem_pairs = 0
    nonmem_pairs = 0
    total = 0
    ngram = 3
    mode = "pos"
    while line:
        total+=1

        mem_quote = line.split('\t')[0]
        line = corpus.readline()
        nonmem_quote = line.split('\t')[0]
        # print "mem"
        mem_score = LM.get_tf_idf_score(mem_quote, mode=mode, ngram=ngram)
        # print "nonmem"
        nonmem_score = LM.get_tf_idf_score(nonmem_quote, mode=mode, ngram=ngram)
        if mem_score > nonmem_score:
            mem_pairs +=1
        elif nonmem_score > mem_score:
            nonmem_pairs+=1
        elif mem_score==nonmem_score:
            total-=1
        line = corpus.readline()

        if total%500==0:
            print "%d pairs compared" % total
    append_str = "lexically"
    if mode == "pos":
        append_str = "syntactically"
    print "Percentage of pairs where memorable quote is %s more distinct " \
          "(%d-grams): %f" % (append_str, ngram, float(mem_pairs)/total)
    print "Percentage of pairs where non-memorable quote is %s more distinct " \
          "(%d-grams): %f" % (append_str, ngram, float(nonmem_pairs)/total)
    corpus.close()

def compare_total_distinctiveness_pairwise():
    LM = BrownLanguageModel()
    LM.load_doc_freqs()
    corpus = file('../quotes.dat', 'r')
    line = corpus.readline()
    mem_pairs = 0
    nonmem_pairs = 0
    total = 0
    mode = "lex"
    while line:
        total+=1
        mem_quote = line.split('\t')[0]
        line = corpus.readline()
        nonmem_quote = line.split('\t')[0]
        # print "mem"
        mem_score = 0
        nonmem_score = 0

        for ngram in range(1,4):
            mem_score += LM.get_tf_idf_score(mem_quote, mode=mode, ngram=ngram)
            # print "nonmem"
            nonmem_score += LM.get_tf_idf_score(nonmem_quote, mode=mode, ngram=ngram)

        if mem_score > nonmem_score:
            mem_pairs +=1
        elif nonmem_score > mem_score:
            nonmem_pairs+=1
        elif mem_score==nonmem_score:
            total-=1
        line = corpus.readline()

        if total%500==0:
            print "%d pairs compared" % total
    append_str = "lexically"
    if mode == "pos":
        append_str = "syntactically"
    print "Percentage of pairs where memorable quote is %s more distinct " \
          "(combined): %f" % (append_str, float(mem_pairs)/total)
    print "Percentage of pairs where non-memorable quote is %s more distinct " \
          "(combined): %f" % (append_str, float(nonmem_pairs)/total)
    corpus.close()

def compare_test_distinctiveness(path):
    LM = BrownLanguageModel()
    LM.load_doc_freqs()
    total = {'M':0, 'N':0}
    dist = {'M':0, 'N':0}
    corpus_file = file(path, 'r')
    line = corpus_file.readline()
    ngram = 1
    mode = "pos"
    while line:
        line = line.strip()
        print line
        if line=="":
            continue
        line = line.split('\t')
        if len(line) ==1:
            line = corpus_file.readline()
            continue
        slogan = line[0].strip()
        mem = line[1].strip()

        score = LM.get_tf_idf_score(slogan, mode=mode, ngram=ngram)
        dist[mem] += score
        total[mem]+=1
        line = corpus_file.readline()
    appendstr = "lexical"
    if mode == "pos":
        appendstr = "syntactic"
    print "Average %d-gram %s TF-IDF score for memorable slogans: %f" % (ngram, appendstr, float(dist['M'])/total['M'])
    print "Average %d-gram %s TF-IDF score for non-memorable slogans: %f" % (ngram, appendstr, float(dist['N'])/total['N'])
# compare_total_distinctiveness_pairwise()
# compare_test_distinctiveness('../Memfiles/Advertising.dat')
# LM = BrownLanguageModel(rebuild=True)
# LM.load_doc_freqs(rebuild=True)

# todo: create brand new test data files that aren't corrupted