from bitvector import BitVector, RowBitVector
'''
example:
>>> H = BitMatrix([12, 6, 13, 10, 5, 14, 6, 15, 11, 9 , 8 , 4, 2, 1])
>>> H.print_bits()
[1 0 0 1 1 0 1 0 1 1 1 1 0 0 0]
[1 1 0 1 0 1 1 1 1 0 0 0 1 0 0]
[0 1 1 0 1 0 1 1 1 1 0 0 0 1 0]
[0 0 1 1 0 1 0 1 1 1 1 0 0 0 1]

>>> print H * BitVector(27, H.m())
TODO
'''
class BitMatrix(object):
    def __init__(self,
                 columns_a,
                 m_a=None):

        if m_a is not None:
            self._m = m_a
        else:
            largest_value = max(columns_a)
            self._m = largest_value.bit_length()

        self._n = len(columns_a)
        
        # list of column vectors
        #
        if isinstance(columns_a, list):

            # presumably if the first column is an integer, the rest will be as well
            #
            if isinstance(columns_a[0], int):
                self._columns = []
                for column in columns_a:
                    if column < 0:
                        raise ValueError
                    self._columns.insert(len(self._columns),
                                        BitVector(column, 
                                                  self._m))
            elif isinstance(columns_a[0], BitVector):
                self._columns = columns_a

        elif isinstance(columns_a, BitMatrix):
            self._columns = columns_a.columns()
        else:
            raise NotImplementedError
    def n(self):
        return self._n
    def m(self):
        return self._m
    def columns(self):
        return self._columns

    # returns a row vector, by 
    def __getitem__(self, i):
        val = 0
        for j in range(self._n):
            # print "asdf", j, i, self._columns[j]
            
            bit_at_row_i_column_j = self._columns[j][i]
            power = self._n - j - 1
            val = val + (bit_at_row_i_column_j << power)
        return RowBitVector(val, self._n, self, i)

    def __repr__(self):
        values = [str(col._value) for col in self._columns]
        values_string = "["
        for i, val in enumerate(values):
            values_string = values_string + val
            if i == self._n - 1:
                values_string = values_string + "]"
            else:
                values_string = values_string + ", "
        
        return values_string + " (" + str(self._m) + " bits per column)"

    def print_bits(self):
        for i in range(self._m):
            row = "["
            for j in range(self._n):
                row = row + str(self[i][j]) 
                # add space between bits, unless
                if j != self._n - 1:
                    row = row + " "
            row = row + "]"
            print row

    def column(self, col_number_a):
        return self._columns[col_number_a]

    def transpose(self):
        cols = []
        for i in range(self._m):
            cols.insert(len(cols), self[i])
        return BitMatrix(cols, self._n)

    def __add__(self, y):
        pass
    def __sub__(self, y):
        pass
    def __mul__(self, y):
        if self.n() != y.m():
            print "left hand n =", self.n(), "!=", "right hand m = ", y.m()
            raise ValueError
        if isinstance(y, BitVector):
            val = 0
            for row_number in range(self._m):
                power = row_number
                _row_number = self._m - row_number - 1
                row_product = self[_row_number] * y
                val = val + (row_product << power)
            return BitVector(val, self._m)
        elif isinstance(y, BitMatrix):
            output_col_list = []
            for col_number in range(y._n):
                output_col_list.insert(len(output_col_list),
                                       self * y.column(col_number))
            return BitMatrix(output_col_list, self._m)
        else:
            raise ValueError
