#Written by: Anusha Balakrishnan
#Date: 4/8/14

in_file = file('cornell_movie_quotes_corpus/moviequotes.memorable_nonmemorable_pairs.google_filtered.txt','r')
out_file = file('../quotes.dat','w')
mov_set = []
line = in_file.readline()
mov_set.append(line)
while line:
    if line.strip()=="":
        mem = mov_set[1].strip()+"\tM"
        nonmem = mov_set[3].strip()
        nonmem = nonmem.split(' ', 1)
        nonmem = nonmem[1] + "\tN"
        mov_set = []
        out_file.write(mem+"\n")
        out_file.write(nonmem+"\n")
    line = in_file.readline()
    mov_set.append(line)
