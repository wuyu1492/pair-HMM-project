from read_data import *
from getTrans import *
import numpy as np
import sys, getopt

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args =  getopt.getopt(argv, "i:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('testmain.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print('inputfile = ', inputfile)
    print('outputfile = ', outputfile)
    data_all = readInput(inputfile)
    #print('data_all:', len(data_all))
    for d in range(0, len(data_all)):
        print('Processing data set', d)
        data = data_all[d]
        for l in range(0, len(data[0])):
            print('base No.', l)
            for h in range(0, len(data[5])):
                print('haplo No.', h)
                prior = getPrior(data[0][l], data[5][h], data[1][l])
                mm, im, dm, mi, ii, md, dd = getTrans(data[2][l], data[3][l], data[4][l])
    #prior = getPrior(data_all[0][0][0], data_all[0][5][0], data_all[0][1][0] )
    #print('prior.shape =', prior.shape)
    #mm, im, dm, mi, ii, md, dd = getTrans(data_all[0][2][0], data_all[0][3][0], data_all[0][4][0])

if __name__ == "__main__":
    main(sys.argv[1:])

