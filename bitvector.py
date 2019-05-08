import weakref

class BitVector(object):
    def __init__(self,
                 value_a,
                 size_in_bits_a):
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
        address = self._m - i - 1

        mask = 1 << address
        return (self._value & mask) >> address
    def __setitem__(self, i, new_val):
        if i > self._m - 1:
            raise ValueError
        # we might want the (self._m - nth) largest bit (vector addressing, 
        #  rather than intuitive bit ordering)
        address = self._m - i - 1
        mask = 1 << address

        old = self._value        
        if new_val == 1:
            self._value = self._value | mask
        elif new_val == 0:
            self._value = (1 << self.m()) - 1 - self._value
            # print "old:", old, "new:", self._value, "<><> bit should now be", new_val

    def _assure_dimensions(self, y):
        if y.m() != self.m():
            raise ValueError

    def __add__(self, y):
        self._assure_dimensions(y)
        return BitVector(self._value ^ y._value, 
                         self._m)

    def __sub__(self, y):
        self._assure_dimensions(y)
        return BitVector(self._value ^ y._value,
                         self._m)

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


# to allow things like this:
#  H[row][col] = 1
# to work correctly (these only work)
class RowBitVector(BitVector):
    def __init__(self, 
                 value_a,
                 size_in_bits_a,
                 parent_matrix_a,
                 row_in_parent_matrix_a):
        self._parent_matrix = parent_matrix_a #weakref.ref(parent_matrix_a)
        self._row_in_parent_matrix = row_in_parent_matrix_a
        super(RowBitVector, self).__init__(value_a, size_in_bits_a)

    def __setitem__(self, key, value):
        self._parent_matrix._columns[self._row_in_parent_matrix][key] = value
        super(RowBitVector, self).__setitem__(key, value)
