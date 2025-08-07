import random  as r
import logging as l
#l.basicConfig(level=l.DEBUG)

class cec_ham:
    '''
    A class with methods to implement the classical
    hamming based error correcting codes.
    '''
    p  = [] # Parity matrix
    i  = [] # Identity matrix
    h  = [] # Parity check matrix
    pt = [] # Transpose of p

    def __init__(self, dsize=4):

        if dsize==4:
            self.p = [ [1,0,1,1],
                       [1,1,1,0],
                       [0,1,1,1],
                       [1,1,0,1]]
            self.i = [ [1,0,0,0],
                       [0,1,0,0],
                       [0,0,1,0],
                       [0,0,0,1]]
            self.num_rows = 4
            self.num_columns = 4
        elif dsize==32:
            self.p = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,],
                      [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,],
                      [0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,],
                      [0,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,1,1,1,],
                      [1,0,1,1,0,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,1,1,0,0,1,],
                      [1,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,],
                      [1,1,1,0,1,1,0,1,0,0,1,1,1,0,1,0,0,1,1,0,0,1,0,1,1,0,1,1,0,1,0,0,]]
            self.i = [[1,0,0,0,0,0,0],
                      [0,1,0,0,0,0,0],
                      [0,0,1,0,0,0,0],
                      [0,0,0,1,0,0,0],
                      [0,0,0,0,1,0,0],
                      [0,0,0,0,0,1,0],
                      [0,0,0,0,0,0,1]]

            self.num_rows = 32
            self.num_columns = 7

        self.num_tcolumns = self.num_rows+self.num_columns

        # Transpose of p using list comprehension
        self.pt = [[self.p[j][i] for j in range(self.num_rows)] for i in range(self.num_columns)]

        # Combine p and i to obtain our check matrix using list comprehension
        self.h = [(self.pt[row]+self.i[row]) for row in range(self.num_rows)]

    def gen_code(self, d: list) -> list:
        '''
        This method generates an ECC code given
        data input. The input is a binary vector
        which is represented as a list.
        '''
        result = [0]*self.num_rows

        for row in range(self.num_rows):
            for column in range(self.num_columns):
                result[row] += self.pt[row][column] * d[column]
            result[row] = result[row]%2
        return result

    def gen_syndrome(self, r_data: list, r_code: list) -> list:
        '''
        Provided a list of received data and received ECC code,
        generate a syndrome
        '''
        syndrome = [0]*self.num_rows
        inp = r_data + r_code

        for row in range(self.num_rows):
            for column in range(self.num_tcolumns):
                syndrome[row] += self.h[row][column] * inp[column]
            syndrome[row] = syndrome[row]%2
        return syndrome

    def dec_syndrome_err(self, synd: list) -> bool:
        '''
        Decode the error syndrome. This method simply returns if
        there is any error or not.
        '''
        return not all([synd[i]==0 for i in range(self.num_rows)])

    def dec_syndrome_err_1bit_code(self, synd: list) -> bool:
        '''
        Decode the error syndrome. This method simply returns a
        boolean true if the syndrome identifies a correctable
        error in the code.
        '''
        return synd.count(1)==1

    def dec_syndrome_err_1bit_data(self, synd: list) -> list:
        '''
        Decode the error syndrome. This method simply returns a
        vector with the location of the error (if it is correctable). Note
        that an error can occur in the code itself in which case the
        error vector will be empty.
        '''
        return [1 if self.pt[row] == synd else 0 for row in range(self.num_columns)]

    def dec_syndrome_err_mbit(self, synd: list) -> bool:
        '''
        Decode the error syndrome. This method simply returns true
        if there was a multi-bit error
        '''
        err_1bitv = self.dec_syndrome_err_1bit_data(synd)

        return \
            (self.dec_syndrome_err(synd)) and \
            (not self.dec_syndrome_err_1bit_code(synd)) and \
            (all([err_1bitv[i]==0 for i in range(self.num_rows)]))

class cec_ham_tst:
    '''
    A class that can generate random input data and inject
    a random error into the data to then test if the cec scheme
    can detect/correct these errors
    '''

    def __init__(self, size: int):
        self.data_size = size

    def gen_data(self) -> list:
        '''
        Return a list of random 1s and 0s
        '''
        num_ones = r.randint(0,self.data_size)
        my_list = [0]*(self.data_size-num_ones) + [1]*(num_ones)
        r.shuffle(my_list)
        return my_list

    def gen_1bit_err(self) -> list:
        '''
        Return a vector which has a 1 in the position where
        the error is to be injected and 0 otherwise.
        This is for a single bit error test.
        '''
        onebit_err_location = r.randint(0,self.data_size-1)
        my_list = [0]*self.data_size
        my_list[onebit_err_location] = 1
        return my_list

    def xor_list(self, list_a: list, list_b: list) -> list:
        '''
        XOR the elements of a list
        '''
        assert len(list_a) == len(list_b)
        return [list_a[i] ^ list_b[i] for i in range(len(list_a))]

    def run_tst(self, ham, size):
        '''
        This method takes a hamming scheme as an input and runs
        a random test of a given size
        '''
        for i in range(size):
            src_data     = self.gen_data()
            src_code     = ham.gen_code(src_data)
            dst_1biterrv = self.gen_1bit_err()
            # This is the corrupted version of the source data
            dst_data     = self.xor_list(src_data,dst_1biterrv)
            syndrome     = ham.gen_syndrome(dst_data,src_code)

            l.debug("Running iteration: %d", i)
            l.debug(str(("Src data:", src_data)))
            l.debug(str(("Src code:", src_code)))
            l.debug(str(("1bit error vector:", dst_1biterrv)))
            l.debug(str(("Dst data:", dst_data)))
            l.debug(str(("Syndrome:", syndrome)))

            # Run our random tests of hamming over 10 iterations
            # We should always get an error
            assert ham.dec_syndrome_err(syndrome)
            # It should be not be fatal
            assert not ham.dec_syndrome_err_mbit(syndrome)

if __name__ == "__main__":
    ham = cec_ham(4)
    ham_tst = cec_ham_tst(4)
    ham_tst.run_tst(ham,100)
