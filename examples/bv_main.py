from bits import BitVector, flip_n_bits

if __name__ == "__main__":
    nbits = 10
    bv  = BitVector("100", nbits)
    bv2 = BitVector("ff", nbits)
    add = bv + bv2
    mul = bv * bv2
    print add, mul
    for i in range(nbits):
        print "bit", i, ":", mul[i]
    print add.hamming_weight()
    print bv
    print flip_n_bits(bv, 1)
