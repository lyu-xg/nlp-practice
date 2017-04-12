from collections import Counter
from itertools import chain
import os.path

DEBUG = False

DATADIR = './brown/'
ALLDIRFILE = DATADIR + 'cats.txt'
OUTPUT = 'wordList.txt'
SENTENCESDIR = 'allwords.txt'

def allFilenames():
    def getAllDirs():
        with open(ALLDIRFILE) as allDirFile:
            return [line.split()[0] for line in allDirFile]
    return map(lambda x:DATADIR+x, getAllDirs())


def getWordsFromFile(path):
    # list of list(sentence) from a filepath
    def wordClean(word):
        return word.lower()[:word.find('/')]
    result = []
    with open(path) as infile:
        for line in infile:
            result.append(tuple(map(wordClean,line.split())))
    return tuple(filter(lambda x:x, result)) # remove newlines


def getAllWords():
    if os.path.exists(SENTENCESDIR):
        with open(SENTENCESDIR) as infile:
            result = eval(infile.read())
            print('reading cached sentences allwords.txt')
    else:
        result = []
        for filename in allFilenames():
            result += getWordsFromFile(filename)
        with open(SENTENCESDIR,'w') as outfile:
            outfile.write(repr(tuple(result)))
    return result

def getWordCounts(sentences):
    wordBag = Counter(chain.from_iterable(sentences))
    del wordBag['']
    for w in wordBag.keys():
        if wordBag[w] < 11:
            wordBag['UNK'] += wordBag[w]
            del wordBag[w]
    return wordBag

def SortAndWrite(wordCounts):
    with open(OUTPUT,'w') as outfile:
        for x,y in sorted(wordCounts.items(),key = lambda x:(x[1],x[0])):
            outfile.write('{:20}{}\n'.format(x,y))

if __name__ == "__main__":
    bag = getWordCounts(getAllWords())
    SortAndWrite(bag)
    if DEBUG:
        with open(OUTPUT) as infile:
            print(infile.read())
    print('see {} for word list.'.format(OUTPUT))
