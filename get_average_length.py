__author__ = 'Rituparna'
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize

infile = 'create_datasets/quotes.dat'

def get_avg_len():
    mem_quotes = 0
    mem_quotes_len = 0
    nonmem_quotes = 0
    non_mem_quotes_len = 0

    with open(infile, 'r') as f:
        for line in f:
            if(line.strip().split('\t')[1]=='M'):
                mem_quotes+=1
                mem_quotes_len+=len(wordpunct_tokenize(line.strip().split('\t')[0]))
            else:
                nonmem_quotes+=1
                non_mem_quotes_len+=len(wordpunct_tokenize(line.strip().split('\t')[0]))
    f.close()

    avg_mem_len = float(mem_quotes_len)/float(mem_quotes)
    avg_non_mem_len = float(non_mem_quotes_len)/float(nonmem_quotes)

    std_dev = 0.66* avg_mem_len

    print avg_mem_len
    print avg_non_mem_len
    print std_dev



def get_pair_wise_len_stat():
    mem_len = 0
    non_mem_len = 0
    stats = 0
    pairs = 0
    with open(infile, 'r') as f:
        for line in f:
            if(line.strip().split('\t')[1]=='M'):
                mem_len+=len(wordpunct_tokenize(line))
            else:
                non_mem_len+=len(wordpunct_tokenize(line))
            #Compare the length of the memorable and non memorable quotes
            if(mem_len!=0 and non_mem_len!=0):
                pairs+=1
                if (mem_len <= non_mem_len):
                    stats+=1
                mem_len = 0
                non_mem_len = 0
    f.close()
    mem_percentage = float(stats)/float(pairs)
    print mem_percentage

def check_len_stats(std_dev):
    fraction = 0
    for i in range(1,5):
        fraction+=0.25
        count1 = 0
        count2 = 0
        mcount = 0
        ncount = 0
        threshold = fraction*std_dev
        print threshold
        with open(infile, 'r') as f:
            for line in f:
                mem_len = 0
                nonmem_len= 0
                if(line.strip().split('\t')[1]=='M'):
                    mem_len+=len(wordpunct_tokenize(line.strip().split('\t')[0]))
                    mcount +=1
                    if (float(mem_len) < threshold):
                        count1+=1
                else:
                    nonmem_len+=len(wordpunct_tokenize(line.strip().split('\t')[0]))
                    ncount+=1
                    if (float(nonmem_len) < threshold):
                        count2+=1
        f.close()
        print "iteration-" , i
        print "memorable quotes below threshold-", count1
        print "total memorable quotes-",mcount
        print "non-memorable quotes below threshold-",count2
        print "non memorable quotes-",ncount


#get_avg_len()
#get_pair_wise_len_stat()
check_len_stats(38)