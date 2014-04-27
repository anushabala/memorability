#Written by: Anusha Balakrishnan
#Date: 4/24/14
from collections import defaultdict
import os
import pickle
from nltk.corpus import brown
import nltk


class BrownLanguageModel:
    def __init__(self, pos_path=None, lex_path=None, rebuild=False):
        self.ngram_pos_count = defaultdict(int)
        self.ngram_lex_count = defaultdict(int)
        self.document_freqs = defaultdict(int)
        if (not rebuild) and (pos_path!=None and os.path.isfile(pos_path)) or (lex_path!=None and os.path.isfile(lex_path)):
            self.ngram_pos_count = pickle.load(file(pos_path, 'rb'))
            self.ngram_lex_count = pickle.load(file(lex_path, 'rb'))
        else:
            self.get_bigram_counts()
            pickle.dump(self.ngram_pos_count, file(pos_path, 'wb'))
            pickle.dump(self.ngram_lex_count, file(lex_path, 'wb'))

    def get_bigram_counts(self):
        count=0
        categories=['news','editorial']
        target_corpus = brown.tagged_sents(simplify_tags=True, categories=categories)
        total = len(target_corpus)
        while count < total:
            sent = target_corpus[count]
            # print sent
            sent.insert(0, ('*', '*'))
            sent.append(('STOP', 'STOP'))
            num_tokens = len(sent)
            i = 0
            while i < num_tokens:

                this_tag = sent[i][1]
                this_word = sent[i][0]
                self.ngram_pos_count[this_tag] += 1
                self.ngram_lex_count[this_word] += 1
                # print this_tag
                if i+1<num_tokens:
                    next_tag = sent[i+1][1]
                    next_word = sent[i+1][0]
                    pos_key = "%s:%s" % (this_tag, next_tag)
                    lex_key = "%s:%s" % (this_word, next_word)
                    self.ngram_pos_count[pos_key] += 1
                    self.ngram_pos_count[lex_key] += 1
                if i+2 < num_tokens:
                    next_tag = sent[i+1][1]
                    next_word = sent[i+1][0]
                    third_tag = sent[i+2][1]
                    third_word = sent[i+2][0]
                    pos_key = "%s:%s:%s" % (this_tag, next_tag, third_tag)
                    lex_key = "%s:%s:%s" % (this_word, next_word, third_word)
                    self.ngram_pos_count[pos_key] += 1
                    self.ngram_pos_count[lex_key] += 1
                i+=1

            count+=1
            if count%100==0:
                print "Progress: %d sentences" % count

    def find_doc_freqs(self, pos_path, lex_path):
        if len(self.ngram_pos_count.keys())==0 or len(self.ngram_lex_count.keys())==0:
            try:
                raise NameError()
            except NameError as e:
                print "Error occurred while accessing POS and lexical N-gram counts: " \
                      "Either POS N-gram counts or lexical N-gram counts haven\'t been " \
                      "initialized from %s and %s. Create LM object with the pos_path, lex_path," \
                      "and rebuild parameters set to true." %(pos_path, lex_path)
        else:
            # Search through the corpus for each key
            categories = ['news', 'editorial']
            target_corpus = brown.tagged_sents(simplify_tags=True, categories=categories)
            total = len(target_corpus)
            count = 0
            while count < total:
                sent = target_corpus[count]
                # print sent
                sent.insert(0, ('*', '*'))
                sent.append(('STOP', 'STOP'))
                num_tokens = len(sent)
                added_pos = []
                added_lex = []
                i = 0
                while i < num_tokens:
                    this_tag = sent[i][1]
                    this_word = sent[i][0]
                    if this_tag not in added_pos:
                        self.document_freqs[this_tag] += 1
                        added_pos.append(this_tag)
                    if this_word not in added_lex:
                        self.document_freqs[this_word] += 1
                        added_lex.append(this_word)
                    if i+1<num_tokens:
                        next_tag = sent[i+1][1]
                        next_word = sent[i+1][0]
                        pos_key = "%s:%s" % (this_tag, next_tag)
                        lex_key = "%s:%s" % (this_word, next_word)
                        if pos_key not in added_pos:
                            self.document_freqs[pos_key] += 1
                            added_pos.append(pos_key)
                        if lex_key not in added_lex:
                            self.document_freqs[lex_key] += 1
                            added_lex.append(lex_key)
                    if i+2 < num_tokens:
                        next_tag = sent[i+1][1]
                        next_word = sent[i+1][0]
                        third_tag = sent[i+2][1]
                        third_word = sent[i+2][0]
                        pos_key = "%s:%s:%s" % (this_tag, next_tag, third_tag)
                        lex_key = "%s:%s:%s" % (this_word, next_word, third_word)
                        if pos_key not in added_pos:
                            self.document_freqs[pos_key] += 1
                            added_pos.append(pos_key)
                        if lex_key not in added_lex:
                            self.document_freqs[lex_key] += 1
                            added_lex.append(lex_key)
                    i+=1

                count+=1
                if count%100==0:
                    print "Progress: %d sentences" % count




LM = BrownLanguageModel('pos_ngrams.pkl', 'lex_ngrams.pkl')
LM.find_doc_freqs('ngram_lex_idfs.pkl', 'ngram_pos_idfs.pkl')
