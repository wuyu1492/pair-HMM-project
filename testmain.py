from read_data import *
from getTrans import *
from PEring import *
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
    data_all = readInput(inputfile)
    f = open(outputfile, 'w')
    initCycle()     # initial cycle counter to 0
    pcs = 16        # precision: 64/32/16
    setPrecision(pcs)
    print('current precision =', pcs)
    ring_size = 16
    total_PE = 32
    ring_num = total_PE/ring_size
    myring = PEring(ring_size)
    for d in range(0, len(data_all)):
        print('Processing data set', d)
        f.write("data set %d \n" % d)
        data = data_all[d]
        for l in range(len(data[0])):        # for each line in one set
            #print('base ', l)
            f.write("base %d \n" % l)
            mm, im, dm, mi, ii, md, dd = getTrans(data[2][l], data[3][l], data[4][l])
            for h in range(0, len(data[5])):    # for each haplo
                #print('haplo', h, end=" ")
                f.write("haplo %d " % h)
                myring.initRing(mm[0])               # initial PE ring
                trans = makeTrans(mm, im, dm, mi, ii, md, dd)
                result = myring.proc(data[0][l], data[5][h], data[1][l], trans)
                #print(result)
                f.write("result = %e\n" % result)
            #break
        #break
    total_cycle = reportCycle()
    total_cycle /= ring_num
    print("total cycle =", total_cycle)
    f.write("total cycle = %d " % total_cycle)
    f.close()

if __name__ == "__main__":
    main(sys.argv[1:])

