def getPYON(path):
    with open(path) as infile:
        return eval(infile.read())

def readBiCodes():
    return getPYON('savedBinaryStrings.pyon')

def bicodePrinter(b):
    for word,code in b.items():
        print('{} - {}\n'.format(word,code))

def main():
    bicodePrinter(readBiCodes())

if __name__ == '__main__':
    main()
