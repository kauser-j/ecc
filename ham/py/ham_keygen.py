import random  as r
import logging as l
#l.basicConfig(level=l.DEBUG)

# Hamming sizes
#
# SECDED:
# ------
# (72,64) : For 64bit data, 8bit code
# (39,32) : For 32bit data, 7bit code

class ham_keygen:
    '''
    A parity matrix generator for hamming code
    '''

    def __init__(self, code_size=7, data_size=32):

        self.csize = 7
        self.dsize = 32

    def gen_p(self):
        # For a given code size, generate the number of
        # columns that have atleast 3 1s in them. Add those
        # to a list.
        valid_p = []

        for i in range(2**self.csize):
            if ( (bin(i).count("1") > 2) and
                 (bin(i).count("1") %2 != 0)):
                bin_i = '{0:07b}'.format(i)
                valid_p.append(bin_i)

        # For the data size, return the number of valid columns
        # found
        for i in range(self.csize):
            curr_row = ""
            for j in range(self.dsize):
                curr_row += valid_p[j][i]
            print(curr_row)

    def gen_p_as_matrix(self):
        # For a given code size, generate the number of
        # columns that have atleast 3 1s in them. Add those
        # to a list.
        valid_p = []

        for i in range(2**self.csize):
            if ( (bin(i).count("1") > 2) and
                 (bin(i).count("1") %2 != 0)):
                bin_i = '{0:07b}'.format(i)
                valid_p.append(bin_i)

        # For the data size, return the number of valid columns
        # found
        for i in range(self.csize):
            curr_row = "["
            for j in range(self.dsize):
                curr_row += valid_p[j][i] + ","
            curr_row += "]"
            print(curr_row)

if __name__ == "__main__":
    k = ham_keygen()
    k.gen_p_as_matrix()
