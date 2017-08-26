#import numpy as np

# open the file
f = open('tiny.in', 'r')

data_all = []   # the list of all the data
data = []       # the list of one set of data
data_size = []
base = []
Qbase = []
Qi = []
Qd = []
Qg = []
haplo = []

for line in f:
    token = line.partition(' ')
    if token[0].isdigit():
        size_temp = [int(token[0]), int(token[2])]  # read the size of the data set
        data_size.append(size_temp)
        print(data_size)
        # store the original data list to data_all
        if base:
            data.extend([base, Qbase, Qi, Qd, Qg, haplo])
            data_all.append(data)
            data = []
            base = []
            Qbase = []
            Qi = []
            Qd = []
            Qg = []
            haplo = []
    elif token[2]:
        temp = []
        for c in token[0]:
            temp.append(c)
        base.append(temp)
        temp = []
        token = token[2].partition(' ')
        for c in token[0]:
            temp.append(ord(c)-33)
        Qbase.append(temp)
        temp = []
        token = token[2].partition(' ')
        for c in token[0]:
            temp.append(ord(c)-33)
        Qi.append(temp)
        temp = []
        token = token[2].partition(' ')
        for c in token[0]:
            temp.append(ord(c)-33)
        Qd.append(temp)
        temp = []
        for c in token[2]:
            temp.append(ord(c)-33)
        temp.pop()
        Qg.append(temp)
    else:
        temp = []
        for c in token[0]:
            temp.append(c)
        temp.pop()
        haplo.append(temp)

if base:
    data.extend([base, Qbase, Qi, Qd, Qg, haplo])
    data_all.append(data)

print(len(data_all[0]), len(data_all[1]), len(data_all[2]))
print(len(data_all[0][0]), len(data_all[0][1]), len(data_all[0][5]))
print(len(data_all[0][0][0]), len(data_all[0][1][0]), len(data_all[0][4][0]))
print(data_all[0][4][0])

# for each line, parse into base, Qbase, Qi, Qd, Qg
# for each data, compare every base with haplotype

