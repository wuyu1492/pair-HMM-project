import numpy as np
from collections import deque

class PE:
    """ process element"""
    def __init__(self):
        self.ta = [0]
        self.tb = [0]
        self.fmid = [(0,0,0)]   # [fm, fi, fd]

    def initPE(self):
        self.ta = [0]
        self.tb = [0]
        self.fmid = [(0, 0, 0)]

    def getFwd(self, fmid_in, prior, trans):
        fm_in, fi_in, fd_in = fmid_in
        mm, im, dm, mi, ii, md, dd = trans
        self.ta.insert(0, dm * (fi_in + fd_in))
        self.tb.insert(0, mm * fm_in)
        fm = prior * (self.ta[-1] + self.tb[-1])
        fi = mi * self.fmid[-1][0] + ii * self.fmid[-1][1]
        fd = md * fm_in + dd * fd_in
        fmid = (fm, fi, fd)
        self.fmid.insert(0, fmid)

    def mvFwd(self):
        self.ta.pop()
        self.tb.pop()
        self.fmid.pop()

def makeTrans(mm, im, dm, mi, ii, md, dd):
    length = len(mm)
    trans = []
    for l in range(length):
        trans_temp = (mm[l], im[l], dm[l], mi[l], ii[l], md[l], dd[l])
        trans.append(trans_temp)
    return trans

class PEring: 
    def __init__(self, rsize):
        self.PElist = [PE()]
        self.rsize = rsize
        for i in range(1, rsize):
            self.PElist.append(PE())

    def initRing(self, amm):
        for i in range(self.rsize):
            self.PElist[i].initPE()
        self.PElist[0].tb = [amm]

    def proc(self, prior, trans):
        jLen,iLen = prior.shape
        interBuf = deque(maxlen=iLen)
        interBufLen = iLen - self.rsize
        for t in range(iLen-1):
            interBuf.appendleft((0,0,0))
        notfinish = True
        i = 0
        while notfinish:
            #print('i =', i, ' interBuf size :', len(interBuf))
            Q = []
            for j in range(self.rsize):
                priori = i - j
                if priori < 0:
                    break
                n = 0
                while priori >= iLen :
                    dLen = iLen
                    if iLen < self.rsize:
                        dLen = self.rsize
                    priori -= dLen
                    n += 1
                priorj = j + n*self.rsize       # finish computing position of PE
                if priorj < jLen:
                    buf = ()
                    if (interBuf and j == 0):
                        buf = interBuf.pop()
                    else:
                        buf = self.PElist[j-1].fmid[-1]
                    self.PElist[j].getFwd(buf, prior[priorj][priori], trans[j])
                    Q.append(self.PElist[j])
                    if (j == self.rsize-1 and interBufLen > 0):
                        interBuf.appendleft(self.PElist[j].fmid[-1])
                    if (priori == iLen-1 and priorj == jLen-1):
                        fm, fi, fd = self.PElist[j].fmid[0]
                        result = fm + fi + fd
                        return result
            while Q:
                Q.pop().mvFwd()
            i += 1  # while finish

    def dp(self, prior, mm, im, dm, mi, ii, md, dd):
        jLen, iLen = prior.shape
        trans = makeTrans(mm, im, dm, mi, ii, md, dd)
        result = 0
        #if (jLen > self.rsize and iLen > self.rsize):     # type 1
            #result = self.proc(prior, trans)
        #else:                                       # type 3 with internal buffer
        result = self.proc(prior, trans)
        return result

