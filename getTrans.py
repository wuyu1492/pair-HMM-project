import numpy as np
"""
def getPrior(base, haplo, Qbase):
    prior = np.zeros((len(base), len(haplo)))    # initialize prior matrix
    #print(prior.shape)  # check prior shape
    for i in range(0, len(base)):
        for j in range(0, len(haplo)):
            if base[i] == haplo[j]:
                prior[i][j] = 1-Qbase[i]
            else:
                prior[i][j] = Qbase[i]
    return prior
"""

def getTrans(Qi, Qd, Qg):
    qi = np.array(Qi)
    qd = np.array(Qd)
    qg = np.array(Qg)
    mm = 1.0 - (qi + qd)
    im = 1.0 - qg
    dm = im
    mi = qi
    ii = qg
    md = qd
    dd = qg
    return mm, im, dm, mi, ii, md, dd

