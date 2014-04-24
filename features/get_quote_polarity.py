#Written by: Anusha Balakrishnan
#Date: 4/18/14
import json
import urllib
import urllib2


def call_sentiment_analysis_api(sentence):
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
def get_polarity(response):
    try:
        json_response = json.loads(response)
        label = json_response['label']
        if label=="neutral" :
            return 0
        elif label=="pos":
            return 1
        elif label=="neg":
            return -1
        else:
            return -9
    except ValueError as v:
        print response
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

    
def test_corpus_polarity():
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
        response = call_sentiment_analysis_api(sentence)
        if response==None:
            break
        polarity = get_polarity(response)
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

test_corpus_polarity()