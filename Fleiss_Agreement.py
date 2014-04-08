import sys

def small_P(slogans,N,n, cols):
	p = {'Y':0,'N':0}
	for slogan in slogans:
		if '?' not in slogan and '-' not in slogan:
			for c in cols:
				for rating in slogan[c]:
                                    if 'Y' in rating or 'N' in rating:
					p[rating] += 1
	p['Y'] = float(p['Y'])/(N*n)
	p['N'] = float(p['N'])/(N*n)

	return p
def big_P(slogans, N, n,k, cols):
	P = []
	for i in range(0,N):
		P.append(1.0/(n*(n-1)))


	for i in range(0,N):
		sum = 0.0
		j = {'Y':0, 'N':0}
		for key in j.keys():
			for c in cols:
				for rating in slogans[i][c]:
					if rating==key:
						j[key] += 1
			sum+= j[key]*j[key]
		sum = sum - n
		P[i] = sum*P[i]	
	
	#print P
	return P
def calc_agreement(filename):
	N=0
	k = 2
	in_file = file(filename, 'r')
	line = in_file.readline()
	slogans = []
	while line:
		line = line.strip().split('\t')
		slogans.append(line) 
		line = in_file.readline()
		N += 1
	cols = [[1,2],[1,3],[2,3],[1,2,3]]
	for c in cols:
		print c
		n = len(c)
		p = small_P(slogans, N,n, c)
		P = big_P(slogans, N, n, k, c)
		mean_P = 0.0
		for x in P:
			mean_P += x
		mean_P /= N
		#print mean_P
	
		mean_Pe = p['Y']*p['Y'] + p['N']*p['N']	
		#print mean_Pe
	
		k = float(mean_P - mean_Pe) / (1-mean_Pe)
	
		print k
		
def __main__(args):

	
	name = args[1]
	
	calc_agreement(name)
	
__main__(sys.argv)
