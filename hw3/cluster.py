from parser import getAllWords, OUTPUT
from math import log
import os.path
from itertools import chain, combinations, permutations
from collections import Counter

DEBUG = True
DETAIL = False


class TwoGramModel(object):
    def __init__(self,wordlist):
        if DEBUG: print("building bi-gram model.")
        WBAG = set(wordlist)
        def replaceLoFreq(sentence):
            return tuple(map(lambda x:x if x in WBAG else 'UNK', sentence))
        def combineTwoWord(sentence):
            res = []
            for i in range(len(sentence)-1):
                res.append((sentence[i],sentence[i+1]))
            return res

        #allPurmutations = permutations(WBAG, 2)
        #sentences = chain(map(replaceLoFreq, getAllWords()),allPurmutations)
        sentences = tuple(map(replaceLoFreq,getAllWords()))
        self.OneGramCounter = Counter(chain.from_iterable(sentences))

        combinedSentence = map(combineTwoWord, sentences)
        self.TwoGramCounter = Counter(chain.from_iterable(combinedSentence))
        if DEBUG: print('bi-gram model build complete.')

    def count(self,*args):
        # e.g. M.count('there')  M.count('there','is')
        if len(args)==1:
            return self.OneGramCounter[args[0]]
        elif len(args)==2:
            return self.TwoGramCounter[tuple(args)]
        else:
            print('illegal access to the Model.')
            return 0

class Clusters(object):
    def __init__(self, gramModel, wordlist, K=40):
        self.K = K
        self.M = gramModel
        self.allWords = set(wordlist)
        self.remainingWords = wordlist
        self.C = [[self.remainingWords.pop()] for i in range(self.K)]
        #print('calculating all word pairs')
        #self.calcAllWordPairs()

        self.initL()
        if DEBUG: print('L table initialization complete.')

    def calcAllWordPairs(self):
        pairs = combinations(self.allWords, 2)
        pairs = filter(lambda x:M.count(x[0],x[1]) or M.count(x[1],x[0]), pairs)
        self.wordPairs = list(pairs)

    def weight(self,c1,c2):

        biCount = self.BiCount(c1,c2)
        if not biCount:
            return 0
        individualCounts = self.count(c1) * self.count(c2)
        #print(biCount,individualCounts)
        return biCount*log(biCount/individualCounts, 2)

    def W(self,c1,c2):
        #if DEBUG: print('calculating weight for {}'.format([c1,c2]))
        if DETAIL:
            print('weight of {} and {}: '.format(c1,c2),self.weight(c1,c2)+self.weight(c2,c1))
        if c1==c2:
            return self.weight(c1,c2)
        else:
            return self.weight(c1,c2)+self.weight(c2,c1)

    def count(self, c):
        return sum(self.M.count(w) for w in c)# or 0.1

    def BiCount(self, c1, c2):
        #if DEBUG: print('getting BiCount for {} and {}'.format(c1,c2))
        return sum(self.M.count(i,j) for i in c1 for j in c2) #or 0.1

    def allClusterWords(self):
        return chain.from_iterable(self.C)

    def LFromScratch(self, c1, c2):
        W = self.W
        otherNodes = filter(lambda x:x not in c1 and x not in c2, self.allClusterWords())
        return -W(c1,c2)-W(c1,c1)-W(c2,c2)+W(c1+c2,c1+c2) - \
                sum(W(c1,(w,)) for w in otherNodes) - \
                sum(W(c2,(w,)) for w in otherNodes) + \
                sum(W(c1+c2,(w,)) for w in otherNodes)

    def LAfterMerge(self, c1, c2, m1, m2):
        pass

    def initL(self):
        # L = change of Quality if c1 and c2 were to be Merged
        cacheDir = 'initialL.txt'
        if os.path.exists(cacheDir):
            with open(cacheDir) as infile:
                self.L = eval(infile.read())
            if DEBUG: print('loaded initlialzed L table from disk.')
            return

        if DEBUG: print('initializing L Table from scratch')

        self.L = Counter()
        clusterPairs = combinations(self.C+[[self.remainingWords.pop()]], 2)
        for c1,c2 in clusterPairs:
            if DETAIL: print('calculating for cluster pair',c1,c2)
            self.L[(tuple(c1),tuple(c2))] = self.LFromScratch(c1,c2)
            if DETAIL: print('value being:',self.L[(tuple(c1),tuple(c2))])
        with open(cacheDir,'w') as outfile:
            outfile.write(repr(self.L))
        if DEBUG: print('L table initialized from scratch complete:')



def main():
    with open(OUTPUT) as infile:
        WORDLIST = [line[:line.find(' ')] for line in infile]
    M = TwoGramModel(WORDLIST)
    C = Clusters(M, WORDLIST)
    print(M.count('the','wine'))
    for item in C.L.items():
        print(item)


if __name__ == '__main__':
    main()
    #print('initialized Clusters',C.C)
    #print('initialized L table',C.L)
