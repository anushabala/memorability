#Written by: Anusha Balakrishnan
#Date: 4/10/14
import random

'''
Splits a combined training+validation set into training and validation, depending on the fold number
  data - the combined dataset to be split
  k - the number of the fold (1-total)
  total - the total number of folds (default 5)
  '''
def get_kth_split(data, k, total=5):
    corpus_size = len(data)
    val_size = corpus_size/total
    val_fold = (total-(k-1))
    print val_fold

    val_start = ((val_fold-1) * val_size) - 1
    val_end = val_start+val_size

    val_set = data[val_start: val_end+1]
    train_set = list(set(data)-set(val_set))

    return train_set, val_set


def read_data(data):
    infile = file(data, 'r')
    lines = []
    line = infile.readline()
    while line:
        lines.append(line)
        line = infile.readline().strip()
    return lines


def random_split(lines, train, val, test):
    corpus_size = len(lines)
    combined_size = int(corpus_size*(train+val))
    combined_size = combined_size - combined_size%5

    corpus_ind = []
    corpus_ind.extend(range(0, corpus_size))

    combined_ind = random.sample(xrange(corpus_size), combined_size)
    combined_ind.sort()
    test_ind = list(set(corpus_ind) - set(combined_ind))
    test_ind.sort()

    combined_set = []
    test_set = []
    for i in combined_ind:
        combined_set.append(lines[i])
    for i in test_ind:
        test_set.append(lines[i])


    return combined_set, test_set

    # print combined

lines = read_data('../quotes.dat')
combined, test = random_split(lines, 0.6, 0.2, 0.2)
combined_file = file('../combined.dat', 'w')
test_file = file('../test.dat', 'w')
for line in combined:
    combined_file.write(line+'\n')

for line in test:
    test_file.write(line+'\n')

combined_file.close()
test_file.close()
train_set, val_set = get_kth_split(combined, 1, 5)

