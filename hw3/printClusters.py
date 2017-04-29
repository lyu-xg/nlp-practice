def getPYON(path):
    with open(path) as infile:
        return eval(infile.read())

def readClusters():
    def reduceTuple(t):
        return list(map(lambda x:x[0], t))
    clusters = getPYON('savedClusters.pyon')
    return map(reduceTuple,clusters.values())

def clusterPrinter(c):
    for index,item in enumerate(c):
        print("{}.  {}\n".format(index+1,'  '.join(item),len(item)))

def main():
    clusterPrinter(readClusters())

if __name__ == '__main__':
    main()
