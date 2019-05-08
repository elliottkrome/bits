from bitmatrix import BitMatrix
from bitvector import BitVector

from random import randint  # for bit-flipping

def flip_n_bits(bits_a, n_a):
    if isinstance(bits_a, BitVector):
        st = " "
        value = bits_a.value()
        m = bits_a.m()
        for i in range(n_a):
            address_of_bit_to_flip = randint(0, m - 1)
            st = st + str(address_of_bit_to_flip)
            value = value ^ pow(2, address_of_bit_to_flip)

        return BitVector(value, m), st
    else:
        raise TypeError

def flip_up_to_n_bits(bits_a, n_a):

    if isinstance(bits_a, BitVector):
       n_bits_to_flip = randint(0, n_a)
       print "flipped", n_bits_to_flip, "bits"
       return flip_n_bits(bits_a, n_bits_to_flip)
    elif isinstance(bits_a, BitMatrix):
        row_vectors = []
        bits_flipped = []
        for i in range(bits_a.m()):
            n_bits_to_flip = randint(0, n_a)
            perturbed_row, bits_flipped_current_row = flip_n_bits(bits_a[i], n_bits_to_flip)
            row_vectors.insert(len(row_vectors), perturbed_row)
            bits_flipped.insert(len(bits_flipped), bits_flipped_current_row)
        print bits_flipped_current_row
        return BitMatrix(row_vectors, bits_a.n()).transpose()
    else:
        raise ValueError
