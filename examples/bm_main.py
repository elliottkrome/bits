from bitmatrix import BitMatrix
from bitvector import BitVector

if __name__ == "__main__":
    cols = [1, 2, 3, 4, 5, 6, 7]
    H = BitMatrix(cols)

    H.print_bits()
    H.transpose().print_bits()

    x = BitVector(3, H.n())
    Hx = H * x
    Hx.print_bits()

    HtH = H * H.transpose()
    HtH.print_bits()

    print H
    print HtH
