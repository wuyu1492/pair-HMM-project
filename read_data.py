def readInput( fin_name ):
    f = open('tiny.in', 'r')
    data_all = []
    data = []
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
            size_temp = [int(token[0]), int(token[2])]
            data_size.append(size_temp)
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
    f.close()
    return data_all
