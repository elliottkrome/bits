from bits import BitMatrix
from bits import BitVector

if __name__ == "__main__":
    cols = [11, 14, 7, 8, 4, 2, 1]
    m = 4 # 3 bits per column
    msb_on_top = True

    C = BitMatrix(cols, m, msb_on_top)
    print "C:"
    C.print_bits()

    x = BitMatrix([3, 13], m, msb_on_top).transpose()
    print "x:", x
    print x, C
    xC = x * C
    print "xC:", xC
    xC.print_bits()

    print "C':"
    C.transpose().print_bits()
