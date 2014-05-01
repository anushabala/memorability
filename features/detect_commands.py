#Written by: Anusha Balakrishnan
#Date: 4/30/14
from collections import defaultdict
import nltk
from nltk.stem.snowball import SnowballStemmer

class CommandDetector:
    def __init__(self, rel="./"):
        self.imperatives_path = file('%sImperatives.dat' % rel, 'r')
        self.imperative_dict = defaultdict(str)
    def load_imperatives(self):
        line = self.imperatives_path.readline()
        while line:
            line = line.strip().split('\t')
            quote = line[0]
            yn = line[1]
            self.imperative_dict[quote] = yn

            line = self.imperatives_path.readline()
    def is_quote_command(self,sentence):
        if sentence in self.imperative_dict.keys():
            if self.imperative_dict[sentence]=='Y':
                return True
        return False

def corpus_commands():
    CD = CommandDetector()
    CD.load_imperatives()
    corpora = ['../quotes.dat', '../Memfiles/Advertising.dat', '../Memfiles/Political.dat', '../Memfiles/Mnemonics.dat']
    for name in corpora:
        print name
        corpus = file(name, 'r')
        line = corpus.readline()
        mem_com = 0
        nonmem_com  =0
        total_mem = 0
        total_nonmem = 0
        while line:

            line = line.strip().split('\t')
            quote = line[0].strip()
            if len(line)==1:
                mem = quote[-1]
                quote = quote[0:-1].strip()
            else:
                mem = line[1].strip()
            if mem=='M':
                total_mem+=1
            else:
                total_nonmem+=1
            if CD.is_quote_command(quote):
                if mem=='M':
                    mem_com+=1
                else:
                    nonmem_com +=1


            line = corpus.readline()
        print float(mem_com)/total_mem
        print float(nonmem_com)/total_nonmem


def annotate_imperatives():
    in_file = file('../Memfiles/Mnemonics.dat', 'r')
    out_file = file('Imperatives.dat', 'a')
    cont = True
    line = in_file.readline()
    while line:
        line = line.strip().split('\t')
        quote = line[0]
        if len(line)==1:
            quote = quote[0:-1]
        # if quote=="There's one thing you have to be aware of from the very beginning.":
        #     cont = False
        #     line = in_file.readline()
        #     continue
        # if cont:
        #     line = in_file.readline()
        #     continue
        print quote
        yn = int(raw_input("Imperative?"))
        if yn==1:
            out_file.write(quote + '\tY\n')
        else:
            out_file.write(quote + '\tN\n')

        line = in_file.readline()
    in_file.close()
    out_file.close()

# annotate_imperatives()
# CD = CommandDetector()
# CD.load_imperatives()



