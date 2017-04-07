from collections import Counter
from itertools import chain

DATADIR = './brown/'
ALLDIRFILE = DATADIR + 'cats.txt'
OUTPUT = 'wordList.txt'

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
            result.append(list(map(wordClean,line.split())))
    result = filter(lambda x:x, result) # remove newlines
    return list(result)

def getAllWords():
    result = []
    for filename in allFilenames():
        result += getWordsFromFile(filename)
    return result

def getWordCounts(sentences):
    wordBag = Counter(chain.from_iterable(sentences))
    for w in wordBag.keys():
        if wordBag[w] < 11:
            wordBag['UNK'] += wordBag[w]
            del wordBag[w]
    return wordBag

def SortAndWrite(wordCounts):
    print('see {} for word list.'.format(OUTPUT))
    with open(OUTPUT,'w') as outfile:
        for x,y in sorted(wordCounts.items(),key = lambda (x,y):(y,x)):
            outfile.write('{:.<20}{}\n'.format(x,y))

if __name__ == "__main__":
    bag = getWordCounts(getAllWords())
    print(len(bag))
    print(bag['UNK'])
    SortAndWrite(bag)
