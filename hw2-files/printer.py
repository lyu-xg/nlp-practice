import sys
def getChar(line):
    line = line.split('\t')
    if len(line)<3: return ''
    return line[2] if line[2]!='<space>' else ' '

print(''.join([getChar(line) for line in sys.stdin])+'\n')
