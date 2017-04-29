from collections import Counter
from itertools import chain
from parser import getAllWords

DEBUG = True

class TwoGramModel(object):
    def __init__(self,wordlist):
        if DEBUG: print("building bi-gram model.")
        WBAG = set(wordlist)
        self.N = len(WBAG)
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
            print('WARNING: illegal access to the Model, trying to get {}'.format(args))
            return -1

    def merge(self,w1,w2):
        # we merge w2 to w1, hence deleting c2
        self.OneGramCounter[w1] += self.OneGramCounter[w2]
        del self.OneGramCounter[w2]

        for (x1,x2),count in tuple(self.TwoGramCounter.items()):
            if w2 not in (x1,x2):
                continue
            if x1 == w2 and x2 == w2:
                self.TwoGramCounter[(w1,w1)] += count
            elif x1 == w2:
                self.TwoGramCounter[(w1,x2)] += count
            elif x2 == w2:
                self.TwoGramCounter[(x1,w1)] += count
            del self.TwoGramCounter[(x1,x2)]


if __name__ == '__main__':
    M = TwoGramModel([])
