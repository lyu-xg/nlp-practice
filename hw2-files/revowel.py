import subprocess
revowelCommand = "fstcompose declaration.fst unvowel.fst | fstproject --project_output | fstrmepsilon | fstcompose - revowel{}.fst | fstshortestpath | fstproject --project_output | fstrmepsilon | fsttopsort | fstprint"
grams = [1,2,3,5,7]

def getChar(line):
    line = line.decode('UTF-8').split('\t')
    if len(line)<3: return ''
    return line[2] if line[2]!='<space>' else ' '


print('\nActual Text:')
p = subprocess.Popen('fstprint declaration.fst', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
actualText = ''.join([getChar(line) for line in p.stdout.readlines()])
actualWordBag = set(actualText.split(' '))
print(actualText)

for i in grams:
    print('\nRevoweling using {}-grams character model:'.format(i))
    p = subprocess.Popen(revowelCommand.format(i), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    revoweledText = ''.join([getChar(line) for line in p.stdout.readlines()])
    revoweledBag = set(revoweledText.split(' '))
    print(revoweledText)
    print('got {} out of {} words correct.'.format(len(actualWordBag.intersection(revoweledBag)),len(actualWordBag)))
