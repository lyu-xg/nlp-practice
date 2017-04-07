from parser import getAllWords, OUTPUT
from itertools import chain
from collections import Counter

class TwoGramModel(object):
    def __init__(self,wordlist):
        WBAG = set(wordlist)
        def replaceLoFreq(sentence):
            return list(map(lambda x:x if x in WBAG else 'UNK', sentence))
        def combineTwoWord(sentence):
            res = []
            for i in range(len(sentence)-1):
                res.append((sentence[i],sentence[i+1]))
            return res

        sentences = map(replaceLoFreq, getAllWords())
        self.OneGramCounter = Counter(chain.from_iterable(sentences))

        combinedSentence = map(combineTwoWord, sentences)
        self.TwoGramCounter = Counter(chain.from_iterable(combinedSentence))

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
        self.wordList = wordlist
        self.C = [[self.wordList.pop()] for i in range(self.K)]
        



if __name__ == '__main__':
    with open(OUTPUT) as infile:
        WORDLIST = [line[:line.find('.')] for line in infile]
    M = TwoGramModel(WORDLIST)
    C = Clusters(M, WORDLIST)
    print(M.count(','))
