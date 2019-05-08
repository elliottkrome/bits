from bits import BitMatrix
from bits import BitVector

if __name__ == "__main__":
    cols = [11, 14, 7, 8, 4, 2, 1]
    m = 4 # 3 bits per column

    C = BitMatrix(cols, m)
    print "C:"
    C.print_bits()

    x = BitMatrix([3, 13], m).transpose()
    print "x:", x
    print x, C
    xC = x * C
    print "xC:", xC
    xC.print_bits()

    print "C':"
    C.transpose().print_bits()

    print "before setting to 0: ", C[0]
    C[0][0] = 0
    print "after  setting to 0: ", C[0]
    C[0][0] = 1
    print "after  setting to 1: ", C[0]
