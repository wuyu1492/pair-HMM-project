from collections import deque

class PE:
    """ process element"""
    def __init__(self, base='', trans=(0,0,0,0,0,0,0)):
        self.ta = [0]
        self.tb = [0]
        self.fmid = [(0,0,0)]
        self.base = base
        self.trans = trans
        self.haplo = ''
        self.Qbase = 0

    def initPE(self, base='', trans=(0,0,0,0,0,0,0)):
        self.ta = [0]
        self.tb = [0]
        self.fmid = [(0,0,0)]
        self.base = base
        self.trans = trans
        self.haplo = ''
        self.Qbase = 0

    def calPrior(self):
        prior = self.Qbase
        if self.haplo == self.base:
            prior = 1 - self.Qbase
        return prior

    def getFwd(self, fmid_in, haplo):
        self.haplo = haplo
        fm_in, fi_in, fd_in = fmid_in
        mm, im, dm, mi, ii, md, dd = self.trans
        newta = dm * (fi_in + fd_in)
        newtb = mm * fm_in
        prior = self.calPrior()
        fm = prior * (self.ta[-1] + self.tb[-1])
        fi = mi * self.fmid[-1][0] + ii * self.fmid[-1][1]
        fd = md * fm_in + dd * fd_in
        if self.base == '' or haplo == '':
            newta = 0
            newtb = 0
            fm = 0
            fi = 0
            fd = 0
        self.ta.insert(0, newta)
        self.tb.insert(0, newtb)
        self.fmid.insert(0, (fm, fi, fd))

    def mvFwd(self):
        self.ta.pop()
        self.tb.pop()
        fmid = self.fmid.pop()
        return fmid

def makeTrans(mm, im, dm, mi, ii, md, dd):
    length = len(mm)
    trans = []
    for l in range(length):
        trans_temp = (mm[l], im[l], dm[l], mi[l], ii[l], md[l], dd[l])
        trans.append(trans_temp)
    return trans

class PEring:
    def __init__(self, rsize):
        self.PElist = []
        self.rsize = rsize
        for i in range(rsize):
            self.PElist.append(PE())
        self.interBuf = deque((0, 0, 0))

    def initRing(self, amm):
        for i in range(self.rsize):
            self.PElist[i].initPE()
        self.PElist[0].tb = [amm]
        self.interBuf.clear()
        self.interBuf.appendleft((0, 0, 0))

    def mvRing(self, nh, bufout):
        for l in range(self.rsize-1, 0, -1):
            self.PElist[l].getFwd(self.PElist[l-1].fmid[-1], self.PElist[l-1].haplo)
        self.PElist[0].getFwd(bufout, nh)
        for l in range(self.rsize-1, -1, -1):
            self.PElist[l].mvFwd()
        bufin = self.PElist[-1].fmid[0]
        return bufin

    def proc(self, rbase, haplo, Qbase, trans):
        result = 0
        jLen = len(rbase)
        iLen = len(haplo)
        buflen = iLen - self.rsize  # prepare initial 
        if buflen < 0:
            buflen = self.rsize
        for l in range(buflen):
            self.interBuf.appendleft((0, 0, 0))      # forward var at j = 0
        jposit = 0      # next read base
        while jposit < jLen:
            lentemp = max(iLen, self.rsize)
            for i in range(lentemp):
                if i < min(iLen, self.rsize) and jposit < jLen:
                    j = jposit % self.rsize
                    self.PElist[j].base = rbase[jposit]
                    self.PElist[j].Qbase = Qbase[jposit]
                    self.PElist[j].trans = trans[jposit]
                    jposit += 1
                bufin = self.interBuf.pop()
                if i >= iLen:
                    nh = ''
                else:
                    nh = haplo[i]
                bufout = self.mvRing(nh, bufin)
                self.interBuf.appendleft(bufout)
            #print('jposit = ', jposit-1, self.PElist[0].fmid)
        jfinal = (jLen-1) % self.rsize
        for l in range(jfinal):
            bufin = self.interBuf.pop()
            bufout = self.mvRing('', bufin)
            self.interBuf.appendleft(bufout)
        fm, fi, fd = self.PElist[jfinal].fmid[0]
        result = fm + fi +fd
        return result
