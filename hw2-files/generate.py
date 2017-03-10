for i in range(97,123):
    inchar = chr(i)
    for j in range(97,123):
        outchar = chr(j)
        if i==j:
            continue
        print '0 1',inchar,outchar
