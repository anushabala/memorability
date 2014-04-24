#Written by: Anusha Balakrishnan
#Date: 4/18/14
import json
import pickle
import urllib
import urllib2


class SentimentAnalyzer:
    def save_corpus_polarities(self, in_file, path):
        read_file = file(in_file, 'r')
        polarity_info = []
        line = read_file.readline()
        while line:
            line = line.strip().split('\t')
            quote = line[0].strip()
            mem = line[1].strip()
            response = self.call_sentiment_analysis_api(quote)
            json_response = json.loads(response)
            if json_response==None:
                break
            packaged_data = (quote, mem, json_response)
            print packaged_data
            polarity_info.append(packaged_data)
            line = read_file.readline()

        pickle.dump(polarity_info, file(path, 'wb'))
    def call_sentiment_analysis_api(self,sentence):
        url = "http://text-processing.com/api/sentiment/"
        param = {"text":sentence}
        data = urllib.urlencode(param)

        try:
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except urllib2.HTTPError as e:
            print e.code
            print e.read()
            return None

    '''
    Returns the polarity of a sentence.
    Returns 1 if positive, 0 if neutral, -1 if negative.
    '''
    def get_polarity(self,response):
        label = response['label']
        if label=="neutral" :
            return 0
        elif label=="pos":
            return 1
        elif label=="neg":
            return -1
        else:
            return -9

        # polarities = json_response['probability']
        # print polarities
        # pos = float(polarities['pos'])
        # neg = float(polarities['neg'])
        # neutral = float(polarities['neutral'])
        # max_pol = max(pos, neg, neutral)
        # if max_pol==pos:
        #     return 1
        # elif max_pol==neg:
        #     return -1
        # else:
        #     return 0
    def get_quote_polarity(self, quote):
        response = self.call_sentiment_analysis_api(quote)
        if response==None:
            return -9
        try:
            json_response = json.loads(response)
            polarity = self.get_polarity(json_response)
            return polarity
        except ValueError as v:
            print v
            return -9

    def get_emotion_strength(self, quote):
        response = self.call_sentiment_analysis_api(quote)
        try:
            json_response = json.loads(response)

            label = json_response['label']
            probabilities = json_response['probability']
            pos = float(probabilities['pos'])
            neg = float(probabilities['neg'])
            neutral = float(probabilities['neutral'])

            if label=="neutral":
                return neutral
            elif label=="pos":
                return pos
            elif label=="neg":
                return neg
            else:
                return -9

        except ValueError as v:
            print response
    
def test_corpus_polarity():
    sentAnalysis = SentimentAnalyzer()
    corpus = file('../quotes.dat', 'r')
    line = corpus.readline()
    pos = {'M':0, 'N':0}
    neg = {'M':0, 'N':0}
    neut = {'M':0, 'N':0}
    total = {'M':0, 'N':0}
    while line:

        line = line.split('\t')
        sentence = line[0]
        mem = line[1].strip()
        polarity = sentAnalysis.get_quote_polarity(sentence)
        total[mem]+=1
        if polarity==1:
            pos[mem] +=1
        elif polarity==0:
            neut[mem]+=1
        elif polarity==-1:
            neg[mem]+=1
        line = corpus.readline()

        if (total['M']+total['N'])%500==0:
            print "Polarized %d quotes" %(total['M']+total['N'])


    print "MEMORABLE QUOTES"
    print "Percent positive: %f" % (float(pos['M'])/total['M'])
    print "Percent negative: %f" % (float(neg['M'])/total['M'])
    print "Percent neutral: %f" % (float(neut['M'])/total['M'])

    print "NON-MEMORABLE QUOTES"
    print "Percent positive: %f" % (float(pos['N'])/total['N'])
    print "Percent negative: %f" % (float(neg['N'])/total['N'])
    print "Percent neutral: %f" % (float(neut['N'])/total['N'])

def compare_corpus_polarity(corpus_polarities):
    corpus = pickle.load(file(corpus_polarities, 'rb'))
    i=0
    while i<len(corpus):
        current_info = corpus[i]
        next_info= corpus[i+1]
        print current_info,"\n", next_info

        current_quote = current_info[0]
        current_mem = current_info[1]
        current_polarities = current_info[2]
        i+=2


# test_corpus_polarity()
sentAnalyzer = SentimentAnalyzer()
sentAnalyzer.save_corpus_polarities('../quotes.dat', 'corpus_polarities.pkl')
# compare_corpus_polarity('corpus_polarities.pkl')