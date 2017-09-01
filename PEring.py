import numpy as np
from collections import deque
# get forward variable
# initial a table of len(base)*len(haplo)
# each (i, j) has three forward variable and t_a, t_b
# input: fwd var from (i-1, j) and (i, j-1) and trans at j

# in PE:
# store latest two results
# i from 0 to N_h, j from 0 to N_r
class PE:
    """ class process element"""
    def __init__(self):
        self.ta = [0]
        self.tb = [0]
        self.fi = [0]
        self.fd = [0]
        self.fm = [0]

    def initPE(self):
        self.ta = [0]
        self.tb = [0]
        self.fi = [0]
        self.fd = [0]
        self.fm = [0]

    def getFwd(self, fm_in, fi_in, fd_in, prior, mm, im, dm, mi, ii, md, dd):
        self.ta.insert(0, dm * (fi_in + fd_in))
        self.tb.insert(0, mm * fm_in)
        self.fm.insert(0, prior * (self.ta[-1] + self.tb[-1]))
        self.fi.insert(0, mi * self.fm[-1] + ii * self.fi[-1])
        self.fd.insert(0, md * fm_in + dd * fd_in)

    def mvFwd(self):
        self.ta.pop()
        self.tb.pop()
        self.fi.pop()
        self.fd.pop()
        self.fm.pop()

"""
# in BufEle: internal buffer element
class BufEle:
    def __init__(self):
        #self.ta = [0]
        #self.tb = [0]
        self.fi = [0]
        self.fd = [0]
        self.fm = [0]

    def getFwd(self, fm_in, fi_in, fd_in, prior, mm, im, dm, mi, ii, md, dd):
        self.fi.insert(0, fi_in)
        self.fd.insert(0, fd_in)
        self.fm.insert(0, fm_in)

    def mvFwd(self):
        self.fi.pop()
        self.fd.pop()
        self.fm.pop()
"""

class PEring:
    def __init__(self, rsize):
        self.PElist = [PE()]
        self.rsize = rsize
        for i in range(1, rsize):
            self.PElist.append(PE())
        self.aposit = 0     # i = aposit
    
    def initRing(self, amm):
        self.aposit = 0
        for i in range(self.rsize):
            self.PElist[i].initPE()
        self.PElist[0].tb = [amm]

    def dp(self, prior, mm, im, dm, mi, ii, md, dd):
        jLen, iLen = prior.shape
        #print('prior.shape =', jLen, iLen)
        if (jLen <= self.rsize and
                iLen >= self.rsize):
            for i in range(iLen):
                self.PElist[0].getFwd(0, 0, 0, prior[0][i], mm[0], im[0], dm[0], mi[0], ii[0], md[0], dd[0])
                if i < (jLen-1) :
                    len_temp = i+1
                else:
                    len_temp = jLen
                for j in range(1, len_temp):
                    self.PElist[j].getFwd(
                            self.PElist[j-1].fm[-1], self.PElist[j-1].fi[-1], self.PElist[j-1].fd[-1],
                            prior[j][i-j], mm[j], im[j], dm[j], mi[j], ii[j], md[j], dd[j])
                for j in range(0, len_temp):
                    self.PElist[j].mvFwd()
                self.aposit += 1
            for i in range(1, jLen):
                for j in range(i, jLen):
                    self.PElist[j].getFwd(
                            self.PElist[j-1].fm[-1], self.PElist[j-1].fi[-1], self.PElist[j-1].fd[-1],
                            prior[j][iLen+i-1-j], mm[j], im[j], dm[j], mi[j], ii[j], md[j], dd[j])
                for j in range(i, jLen):
                    self.PElist[j].mvFwd()
                self.aposit += 1
            result = self.PElist[jLen-1].fm[-1] + self.PElist[jLen-1].fi[-1] + self.PElist[jLen-1].fd[-1]
            return result
        elif (iLen <= self.rsize and
                jLen >= self.rsize):
            for i in range(iLen):
                self.PElist[0].getFwd(0, 0, 0, prior[0][i], mm[0], im[0], dm[0], mi[0], ii[0], md[0], dd[0])
                for j in range(1, i+1):
                    self.PElist[j].getFwd(
                            self.PElist[j-1].fm[-1], self.PElist[j-1].fi[-1], self.PElist[j-1].fd[-1],
                            prior[j][i-j], mm[j], im[j], dm[j], mi[j], ii[j], md[j], dd[j])
                for j in range(0, i+1):
                    self.PElist[j].mvFwd()
            queue = deque(self.PElist)
            for i in range(1, jLen):
                queue.rotate(-1)
                if iLen > (jLen - i):
                    len_temp = jLen - i
                else:
                    len_temp = iLen
                for j in range(len_temp):
                    queue[j].getFwd(
                            queue[j-1].fm[-1], queue[j-1].fi[-1], queue[j-1].fd[-1],
                            prior[i+j][j], mm[i+j], im[i+j], dm[i+j], mi[i+j], ii[i+j], md[i+j], dd[i+j])
                for j in range(len_temp):
                    queue[j].mvFwd()
            result = queue[0].fm[-1] + queue[0].fi[-1] + queue[0].fd[-1]
            return result
        elif (iLen <= self.rsize and
                jLen <= self.rsize):
            for i in range(iLen):
                self.PElist[0].getFwd(0, 0, 0, prior[0][i], mm[0], im[0], dm[0], mi[0], ii[0], md[0], dd[0])
                if jLen < (i+1) :
                    len_temp = jLen
                else:
                    len_temp = i+1
                for j in range(1, len_temp):
                    self.PElist[j].getFwd(
                            self.PElist[j-1].fm[-1], self.PElist[j-1].fi[-1], self.PElist[j-1].fd[-1], 
                            prior[j][i-j], mm[j], im[j], dm[j], mi[j], ii[j], md[j], dd[j])
                for j in range(0, len_temp):
                    self.PElist[j].mvFwd()
            for i in range(1, jLen):
                for j in range(i, jLen):
                    self.PElist[j].getFwd(
                            self.PElist[j-1].fm[-1], self.PElist[j-1].fi[-1], self.PElist[j-1].fd[-1],
                            prior[j][iLen-1-j+i], mm[j], im[j], dm[j], mi[j], ii[j], md[j], dd[j])
                for j in range(i, jLen):
                    self.PElist[j].mvFwd()
            result = self.PElist[jLen-1].fm[-1] + self.PElist[jLen-1].fi[-1] + self.PElist[jLen-1].fd[-1]
            return result
        else:   # for type 3: with internal buffer
            jposit = 0
            interBufLen = iLen - self.rsize + 1
            interBuf = deque(maxlen=interBufLen)    # initial internal buffer
            for i in range(iLen):                   # first row
                #print('size of internal buffer:', len(interBuf), ' i =', i)
                self.PElist[0].getFwd(0, 0, 0, prior[0][i], mm[0], im[0], dm[0], mi[0], ii[0], md[0], dd[0])
                if i < self.rsize - 1:
                    len_temp = i + 1
                else:
                    len_temp = self.rsize
                for j in range(1, len_temp):
                    self.PElist[j].getFwd(
                            self.PElist[j-1].fm[-1], self.PElist[j-1].fi[-1], self.PElist[j-1].fd[-1], 
                            prior[j][i-j], mm[j], im[j], dm[j], mi[j], ii[j], md[j], dd[j])
                for j in range(len_temp):
                    self.PElist[j].mvFwd()
                if i+1 >= self.rsize:
                    interBuf.appendleft([self.PElist[-1].fm[-1], self.PElist[-1].fi[-1], self.PElist[-1].fd[-1]])   # add to internal buffer
            jposit += self.rsize
            while (jLen - jposit) > self.rsize :    # rows in the middle
                for i in range(iLen):
                    #print('size of internal buffer:', len(interBuf), ' i =', i)
                    buf = interBuf.pop()
                    self.PElist[0].getFwd(
                            buf[0], buf[1], buf[2], prior[jposit][i], mm[jposit], im[jposit],
                            dm[jposit], mi[jposit], ii[jposit], md[jposit], dd[jposit])
                    if i < self.rsize - 1:
                        for j in range(1, i+1):
                            self.PElist[j].getFwd(
                                    self.PElist[j-1].fm[-1], self.PElist[j-1].fi[-1], self.PElist[j-1].fd[-1], prior[j+jposit][i-j], mm[j+jposit], im[j+jposit], 
                                    dm[j+jposit], mi[j+jposit], ii[j+jposit], md[j+jposit], dd[j+jposit])
                        for j in range(i+1, self.rsize):
                            jtemp = jposit - self.rsize
                            self.PElist[j].getFwd(
                                    self.PElist[j-1].fm[-1], self.PElist[j-1].fi[-1], self.PElist[j-1].fd[-1], prior[j+jtemp][iLen+i-j], mm[j+jtemp],
                                    im[j+jtemp], dm[j+jtemp], mi[j+jtemp], ii[j+jtemp], md[j+jtemp], dd[j+jtemp])
                        for j in range(self.rsize):
                            self.PElist[j].mvFwd()
                        #interBuf.pop()
                        #interBuf.appendleft([self.PElist[-1].fm[-1], self.PElist[-1].fi[-1], self.PElist[-1].fd[-1]])
                    else:
                        for j in range(1, self.rsize):
                            self.PElist[j].getFwd(
                                    self.PElist[j-1].fm[-1], self.PElist[j-1].fi[-1], self.PElist[j-1].fd[-1], prior[j+jposit][i-j], mm[j+jposit], 
                                    im[j+jposit], dm[j+jposit], mi[j+jposit], ii[j+jposit], md[j+jposit], dd[j+jposit])
                        for j in range(self.rsize):
                            self.PElist[j].mvFwd()
                        #interBuf.pop()
                    interBuf.appendleft([self.PElist[-1].fm[-1], self.PElist[-1].fi[-1], self.PElist[-1].fd[-1]])
                jposit += self.rsize
            for i in range(iLen):                   # enter lowest part
                #print('size of internal buffer:', len(interBuf), ' i =', i)
                buf = interBuf.pop()
                self.PElist[0].getFwd(
                        buf[0], buf[1], buf[2], prior[jposit][i], mm[jposit], im[jposit], dm[jposit],
                        mi[jposit], ii[jposit], md[jposit], dd[jposit])
                jLen_temp = jLen - jposit
                if i < self.rsize - 1:              # still part of the ring processing on last row
                    if i < jLen_temp - 1:
                        len_temp = i+1
                    else:
                        len_temp = jLen_temp
                    for j in range(1, len_temp):
                        self.PElist[j].getFwd(
                                self.PElist[j-1].fm[-1], self.PElist[j-1].fi[-1], self.PElist[j-1].fd[-1], prior[j+jposit][i-j], mm[j+jposit], im[j+jposit],
                                dm[j+jposit], mi[j+jposit], ii[j+jposit], md[j+jposit], dd[j+jposit])
                    jtemp = jposit - self.rsize
                    for j in range(i+1, self.rsize):
                        self.PElist[j].getFwd(
                                self.PElist[j-1].fm[-1], self.PElist[j-1].fi[-1], self.PElist[j-1].fd[-1], prior[j+jtemp][iLen+i-j], mm[j+jtemp], 
                                im[j+jtemp], dm[j+jtemp], mi[j+jtemp], ii[j+jtemp], md[j+jtemp], dd[j+jtemp])
                    for j in range(len_temp):
                        self.PElist[j].mvFwd()
                    for j in range(i+1, self.rsize):
                        self.PElist[j].mvFwd()
                    #interBuf.pop()
                    interBuf.appendleft([self.PElist[-1].fm[-1], self.PElist[-1].fi[-1], self.PElist[-1].fd[-1]])
                else:
                    for j in range(1, jLen_temp):
                        self.PElist[j].getFwd(
                                self.PElist[j-1].fm[-1], self.PElist[j-1].fi[-1], self.PElist[j-1].fd[-1], prior[j+jposit][i-j], mm[j+jposit],
                                im[j+jposit], dm[j+jposit], mi[j+jposit], ii[j+jposit], md[j+jposit], dd[j+jposit])
                    for j in range(jLen_temp):
                        self.PElist[j].mvFwd()
                    #interBuf.pop()
            for i in range(jLen_temp):
                for j in range(i+1, jLen_temp):
                    self.PElist[j].getFwd(
                                self.PElist[j-1].fm[-1], self.PElist[j-1].fi[-1], self.PElist[j-1].fd[-1], prior[j+jposit][iLen+i-j], mm[j+jposit],
                                im[j+jposit], dm[j+jposit], mi[j+jposit], ii[j+jposit], md[j+jposit], dd[j+jposit])
                for j in range(i+1, jLen_temp):
                    self.PElist[j].mvFwd()
            result = self.PElist[jLen_temp-1].fm[0] + self.PElist[jLen_temp-1].fi[0] + self.PElist[jLen_temp-1].fd[0]
            #print('fd =', self.PElist[jLen_temp-1].fd[0])
            return result
