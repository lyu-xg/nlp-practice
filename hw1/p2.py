# Problem 2-1 File Cleaner
# Author: Xueguang Lu
import os
import re
import json
from collections import Counter
from math import log

mypath = 'shakespeare/'
playdirs = ['comedies','tragedies']
comedies = ['awew.txt', 'ayli.txt', 'coe.txt', 'lll.txt', 'maan.txt', 'mfm.txt', 'mnd.txt', 'mov.txt', 'mww.txt', 'tgov.txt', 'tn.txt', 'tots.txt']
tragedies = ['ac.txt', 'cor.txt', 'ham.txt', 'jc.txt', 'lear.txt', 'mac.txt', 'oth.txt', 'rj.txt', 'ta.txt', 'tc.txt']


def removeWords(frequency, words):
	for w in words: 
		del frequency[w]

def readFile(filePath):
	content = []
	print('reading ' + filePath)
	with open(mypath+filePath) as infile:
		for line in infile:
			line = line.lower()
			line = re.sub('[^0-9a-zA-Z]+', ' ', line)
			content+=line.split(' ')
	frequency = Counter(content)
	del frequency['']

	return frequency

def writeFile(filePath, frequency):
	outPath = mypath+'cleaned-'+filePath
	#removeWords(frequency, lowFrequencyWords) # delete words with a total term count < 5
	with open(outPath,'w') as outfile:
		json.dump(frequency, outfile, sort_keys=True, indent=4)
		print('output to {} complete.'.format(outPath))

if __name__ == '__main__':
	frequencies = {}
	
	# read files and get word frequencies
	for c in comedies+tragedies:
		path = ('comedies/' if c in comedies else 'tragedies/') +c
		frequencies[path] = readFile(path)
	
	totalFrequencies = reduce(lambda a,b:a+b,frequencies.values())

	lowFrequencyWords = filter(lambda w:totalFrequencies[w]<5,totalFrequencies.keys())

	for _,f in frequencies.items():
		removeWords(f,lowFrequencyWords) # remove words with total frequency < 5
		for w,c in f.items():
			if totalFrequencies[w]==c: # remove words that only occur in one play
				del f[w]

	totalFrequencies = reduce(lambda a,b:a+b,frequencies.values())

	comedyFrequencies = Counter()
	tragedyFrequencies = Counter()
	for p,f in frequencies.items():
		if p.startswith('comedies'):
			comedyFrequencies+=f
		else:
			tragedyFrequencies+=f

	print('got total {} words as vocabulary.'.format(len(totalFrequencies)))

	# create folders to store cleaned files
	for directory in [mypath+'cleaned-comedies',mypath+'cleaned-tragedies']:
		if not os.path.exists(directory):
			os.makedirs(directory)

	# output frequency in files after clean
	for path, frequency in frequencies.items():
		writeFile(path, frequency)

	#########################################################################
	#Problem 2-2 Naive Bayes
	prior = 0.5

	V = len(totalFrequencies)
	size = {}
	for play in frequencies:
		size[play] = sum(frequencies[play].values())

	cSize = sum(size[p] for p in size if p.startswith('c'))
	tSize = sum(size[p] for p in size if p.startswith('t'))
	
	def p(word,play,c):

		label = play in comedies
		subdir = 'comedies/' if label else 'tragedies/'
		
		base = comedyFrequencies if c else tragedyFrequencies
		excludedCount = frequencies[subdir+play][word]
		count = base[word]
		
		allCount = cSize if c else tSize            
		if label==c:
			allCount -= size[subdir+play]
			count -= excludedCount

		return float(0.1+count)/(allCount+(V*0.1))

	

	#print frequencies.keys()
	#print comedies,tragedies
	
	with open(mypath+'outputNaiveBayes.csv','w') as outfile:
		fields = '\n\nlog-likihood-c, log-likihood-t, ratio, playName, TrueGenre, Predicted Genre\n'
		outfile.write(fields)
		print fields
		most_tragic_comedy = ('',float('-inf'))
		most_comic_tragedy = ('',float('-inf'))
		for play in comedies+tragedies:
			
			subdir = 'comedies/' if play in comedies else 'tragedies/'
			playWords = frequencies[subdir+play]
			
			Pt = Pc = log(prior,2)
			for w,wordCount in playWords.items():
				Pc += log(p(w,play,True),2)*wordCount
				Pt += log(p(w,play,False),2)*wordCount
			isComedy = Pt<Pc
			isCorrect = 'correct' if isComedy==subdir.startswith('c') else 'incorrect'
			trueGenre = 'comedy' if subdir.startswith('c') else 'tragedy'
			predictedGenre = 'comedy' if isComedy else 'tragedy'
			line = '{}, {}, {}, {}, {}, {}'.format(Pc,Pt,Pc-Pt,play,trueGenre,predictedGenre)
			outfile.write(line+'\n')
			print line,'  --',isCorrect
			

			if trueGenre is 'comedy' and Pt > most_tragic_comedy[1]:
				most_tragic_comedy = (play,Pt)
			if trueGenre is 'tragedy' and Pc > most_comic_tragedy[1]:
				most_comic_tragedy = (play,Pc)

		print('Most tragic comedy is: '+most_tragic_comedy[0])
		print('Most comic tragedy is: '+most_comic_tragedy[0])

	#########################################################################
	#Problem 2-3 Find most Comic and Tragic words

	comic = Counter()
	tragic = Counter()
	
	for w in totalFrequencies:
		c = float(0.1+comedyFrequencies[w])/(cSize+(V*0.1))
		t = float(0.1+tragedyFrequencies[w])/(tSize+(V*0.1))
		#print c,t,w
		comic[w]=log(c,2)-log(t,2)
		tragic[w]=log(t,2)-log(c,2)
	
	print '\nMost Comic words and log-pr-ratios:'
	for i,v in comic.most_common(20):
		print i,v
	print '\nMost Tragic words and log-pr-ratios:'
	for i,v in tragic.most_common(20):
		print i,v
	

