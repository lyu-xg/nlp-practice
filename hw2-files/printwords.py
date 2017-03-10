import sys
from collections import defaultdict

words = defaultdict(list)
words['0'] = [''] # start with state 0, having output <epsilon>
res = []

for line in sys.stdin:
    line = line.strip().split('\t')
    if len(line) == 1: # final state
        res += list(words[line[0]])
    else:
        start,end,_,outputchar = line
        if outputchar=='<epsilon>': outputchar=''
        words[end] += [w+outputchar for w in words[start]]

res = set(res)
print('Got {} words:'.format(len(res)))
for w in res: print(w)
