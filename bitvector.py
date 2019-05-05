from random import randint  # for bit-flipping

class BitVector:
    def __init__(self,
                 value_a,
                 size_in_bits_a,
                 msb_top_a=False):
        if isinstance(value_a, list):
            raise NotImplementedError
        elif isinstance(value_a, str):
            if value_a[0] == '0':
                if value_a[1] == 'x':
                    self._value = int(value_a, 16)
                elif value_a[1] == 'b':
                    self._value = int(value_a, 2)
                else:
                    self._value = int(value_a, 16)
            # if string w/out 0x* prefix, assume hex string by default
            else:
                self._value = int(value_a, 16)
        elif isinstance(value_a, int):
            self._value = value_a
        else:
            raise NotImplementedError
    
        self._m = size_in_bits_a
        # self._max_val_d = int("0b" + "1" * self._m, 2)
        self._max_val_d = pow(2, self._m) - 1
        # self._value = self._value % self._max_val_d
        if self._value > self._max_val_d:
            print "value " + str(self._value) + \
                " not representible given " + str(self._m) + " bits"
            raise ValueError

        # just to be safe, should be unnecessary
        self._value = self._value & self._max_val_d
        self._msb_on_top = msb_top_a

    def m(self):
        return self._m
    def value(self):
        return self._value

    def __repr__(self):
        # length_of_output = self._m + 2 # two chars for '0b'
        # format_string = '#0' + str(length_of_output) + 'b'
        output = "0b"
        for index in range(self.m()):
            output = output + str(self[index])
        return output

    def __getitem__(self, i):
        if i > self._m - 1:
            raise ValueError
        # we might want the (self._m - nth) largest bit (vector addressing, 
        #  rather than intuitive bit ordering)
        if self._msb_on_top:
            address = self._m - i - 1
        else:
            address = i
        # print "here"

        mask = 1 << address
        return (self._value & mask) >> address

    def _assure_dimensions(self, y):
        if y.m() != self.m():
            raise ValueError

    def __add__(self, y):
        self._assure_dimensions(y)
        return BitVector(self._value ^ y._value, 
                         self._m,
                         self._msb_on_top)

    def __sub__(self, y):
        self._assure_dimensions(y)
        return BitVector(self._value ^ y._value,
                         self._m,
                         self._msb_on_top)

    def __mul__(self, y):
        self._assure_dimensions(y)
        val = 0
        for i in range(self.m()):
            val = val + self[i] * y[i]
        val = val % 2
        return val

    def hamming_weight(self):
        weight = 0
        val = self._value
        for i in range(self._m):
            bit = val & 1
            weight = weight + bit
            val = val >> 1
        return weight

def flip_n_bits(bit_vector_a, n_a):
    if not isinstance(bit_vector_a, BitVector):
        raise ValueError
    else:
        value = bit_vector_a.value()
        m = bit_vector_a.m()
        for i in range(n_a):
            address_of_bit_to_flip = randint(0, m - 1)
            value = value ^ pow(2, address_of_bit_to_flip)
        return BitVector(value, m)
