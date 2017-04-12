# Problem 1
from collections import defaultdict
from math import log

V = 26+10+1 # number of characters 

# data structure for our trigram model
class model(object):
	def __init__(self):
		self.probs = defaultdict(int)
		self.vocab = set()

	def addRecord(self,trigram):
		self.vocab.add(trigram[0])
		self.vocab.add(trigram[2])
		#assert(len(trigram) == 3 and type(trigram) is str)
		self.probs[trigram] += 1

	def getBigramProb(self,bigram):
		return

	def getProb(self,trigram):
		count = self.probs[trigram]
		bigram = trigram[0]+trigram[1]
		allbigram = sum(self.probs[bigram+i] for i in self.vocab)
		#print trigram,bigram,allbigram
		return float(0.1+count)/(allbigram+(V*0.1)) # 0.1 being lambda
	
		#print trigram,count,bigram,allCount
		 


# firstly, clean afp1k.txt and save as outputclean.txt
with open('afp1k-clean.txt','w') as newfile:
	newfile.write('')
with open('afp1k.txt') as infile, open('afp1k-clean.txt','a') as outfile:
	for line in infile:
		for char in line:
			if char.isalpha() or char.isdigit() or char==' ':
				outfile.write(char.lower())

print('afk1k.txt cleaned.')


# import data from outputclean.txt into the model
M = model()
with open('afp1k-clean.txt') as infile:
	for line in infile:
		content = line
	print('Got {} characters in afp1k-clean.txt'.format(len(content)))
	for i in range(2,len(content)-1):
		trigram = content[i-2]+content[i-1]+content[i]
		M.addRecord(trigram)
	
print('Got {} distinct trigrams from these chars.'.format(len(M.probs)))


# calculate entropy for each sentence
s1 = 'he somehow made this analogy sound exciting instead of hopeless'
s2 = 'no living humans had skeletal features remotely like these'
s3 = 'frequent internet and social media users do not have higher stress levels'
s4 = 'the sand the two women were sweeping into their dustpans was transferred into plastic bags'

for s in (s1,s2,s3,s4):
	entropy = 0
	for i in range(len(s)-2):
		tri = s[i]+s[i+1]+s[i+2]
		p = M.getProb(tri)
		entropy += -log(p,2)
	print entropy/(len(s)-2),'for:',s

