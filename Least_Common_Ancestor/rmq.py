import sys
import math
from collections import deque
sys.path.append("../")


from utils.binary_tree import BinaryTree
import lca


class RMQ_base:
    """ Abstract base class for the RMQ indexing structure.
    Concrete subclasses must implement the methods _preprocess() and _query().
    """
    def __init__(self, arr):
        """ Initialize an instance of the RMQ_base class.
        @param arr (List[int]): A list of integers.
        """
        self._arr = arr
        self._length = len(arr)

        self._preprocess()

    def _preprocess(self):
        """ Preprocess the array. """
        raise NotImplementedError("This method must be implemented by the subclass")

    def _query(self, i, j):
        """ Query the preprocessed structure. Given array indecies i and j return the index
        of the minimal element in tha range arr[i...j].
        @param i (int): Element index.
        @param j (int): Element index.
        @return k (int): Element index such that arr[k] = min arr[i...j]
        """
        raise NotImplementedError("This method must be implemented by the subclass")

    def __call__(self, i, j):
        return self._query(i, j)


class RMQ_table(RMQ_base):
    """ Concrete class implementing table indexing strategy.
    Every possible query (i, j) is precomputed and the result is stored in a table.
    The size of the table is n^2. Computation of the minimal element is performed
    using bottom-up dynamic programming in O(n^2) time.
    Querying is performed by a simple table look-up in O(1) time.
    """
    def _preprocess(self):
        """ Precompute all n^2 possible queries and store them in a table. """
        self._table = [[None] * self._length for i in range(self._length)]

        # Build the table using bottom-up dynamic programming.
        for i in range(self._length):
            for j in range(i, self._length):
                if i == j:
                    self._table[i][j] = i
                elif self._arr[j] < self._arr[self._table[i][j - 1]]:
                    self._table[i][j] = j
                else:
                    self._table[i][j] = self._table[i][j - 1]

    def _query(self, i, j):
        """ Perform simple table look-up. """
        return self._table[i][j]


class RMQ_sparse(RMQ_base):
    """ Concrete class implementing sparse table indexing strategy.
    For every start index i, we consider intervals of length 1, 2, 4, 8, ..., 2^k
    and so on until we reach the bound. For every interval we precompute the minimal
    element in that interval and store its index in a table. The size of the table
    is nlogn. Computation of the minimal element is performed using bottom-up dynamic
    programming in O(nlogn) time.
    Querying is performed by considering two overlapping intervals. We perform a
    table look-up for each of the two intervals and return the index of the smaller
    of the two elements. Querying is done in O(1) time.
    """
    def _preprocess(self):
        """ Precompute a sparse table of queries storing only intervals
        of length 1, 2, 4, 8, ..., 2^k.
        """
        # Precompute a logarithm table. log[n] = k => 2^k <= n < 2^(k+1)
        self._log = [0] * (self._length + 1)
        temp = 1
        for i in range(1, self._length + 1):
            self._log[i] = self._log[i - 1]
            if temp * 2 <= i:
                self._log[i] += 1
                temp *= 2

        # Compute the log of the length of the array.
        self._loglength = self._log[self._length] + 1

        # Precompute a power table. pow[k] = n => 2^k = n
        self._pow = [1] * (self._loglength + 1)
        for i in range(1, self._loglength):
            self._pow[i] = 2 * self._pow[i - 1]

        # Build the table using bottom-up dynamic programming.
        self._table = [[None] * self._loglength for i in range(self._length)]
        for j in range(self._loglength):
            for i in range(self._length):
                if j == 0:
                    self._table[i][j] = i
                elif i + self._pow[j] > self._length:  # break when the interval size is too big
                    break
                else:
                    left = self._table[i][j - 1]
                    right = self._table[i + self._pow[j - 1]][j - 1]
                    self._table[i][j] = left if self._arr[left] <= self._arr[right] else right

    def _query(self, i, j):
        """ An interval [i, j] is formed as the union of two
        intervals [i, i + 2^k -1] u [j - 2^k + 1, j]. The minimum of the
        two intervals is returned.
        """
        if i > j:
            i, j = j, i

        k = self._log[j - i + 1]    # i + 2^k - 1 <= j
        left = self._table[i][k]
        right = self._table[j - self._pow[k] + 1][k]

        return left if self._arr[left] <= self._arr[right] else right


class RMQ_block(RMQ_base):
    """ Abstract class implementing block decomposition stragety.
    The array is split into blocks of size *block_size*. A summarry array is
    formed from the minimal elements of each block. A *summary RMQ* structure is
    constructed over the summary array using the sparse RMQ table strategy.
    For each block a *block RMQ* structure is constructed usimg the RMQ table strategy.
    The time complexity for building the structure depends on the size of each block
    and also on the strategy selected to detect similar blocks.
    Concrete subclasses must implement the method _compute_block_id().

    Querying is performed by splitting the interval into three parts:
        1. The first part of the interval is located in the left edge block
        2. The second part of the interval fully covers the interior blocks
        3. The third part of the interval is located in the right edge block
    We perform table look-up for the summary structure and for each of the edge
    blocks and return the index of the smaller of the three elements.
    Querying is done in O(1) time.
    """
    def _split(self):
        """ Split the array into blocks and build a summary structure. """
        # Size of each block: b = 1/2 logn.
        self._block_size = int(1/2 * math.log2(self._length))

        # Number of blocks: n / b.
        self._block_count = -((-self._length) // self._block_size)  # hack

        # Array storing the minimal element in each block.
        self._summary = [None] * self._block_count

        # Index array storing the index of the minimal element in each block.
        self._index = [None] * self._block_count

        # Array storing the start index and the end index of each block.
        self._info = [None] * self._block_count

        for i in range(self._block_count):
            start = i * self._block_size
            end = min((i + 1) * self._block_size, self._length)
            self._summary[i] = min(self._arr[start:end])
            self._index[i] = self._arr[start:end].index(self._summary[i])
            self._info[i] = (start, end)

    def _preprocess(self):
        """ Construct a high-level RMQ structure over the summary containing
        block minima. Construct block RMQ structures for each block.
        """
        self._split()

        self._summary_RMQ = RMQ_sparse(self._summary)
        self._block_RMQs = {}

        for i in range(self._block_count):
            start, end = self._info[i]
            block_id = self._compute_block_id(self._arr[start:end])

            if block_id not in self._block_RMQs:
                self._block_RMQs[block_id] = RMQ_table(self._arr[start:end])

    def _query(self, i, j):
        """ To answer queries we must query the summary structure and the individual
        edge blocks to retrieve the index of the minimal element.
        Querying each of the summary structure or the individual edge blocks returns
        the relative position of the minimal element. To compute the absolute position
        of this element we must add the offset of the block to the relative position.

        To answer queries we have to consider 3 cases:
          1. Indecies i and j are both in the same block.
            In this case we search the RMQ table for the given block.
          2. Indecies i and j are in consecutive blocks.
            In this case we search the RMQ tables for the two blocks and return the index
            of the smaller of the two element.
          3. Indecies i and j are not in the same block and not in consecutive blocks.
            In this case we search the RMQ tables for the two edge blocks and also the
            sparse RMQ for the summary. We return the index of the smaller of the 3 elements.
        """
        if i > j:
            i, j = j, i

        # Compute the index of the edge blocks containing the query
        left_block = i // self._block_size
        right_block = j // self._block_size

        # Compute the relative positions within the edge blocks
        relative_left = i % self._block_size
        relative_right = j % self._block_size

        # Compute the start index and the end index of the edge blocks
        start_left, end_left = self._info[left_block]
        start_right, end_right = self._info[right_block]

        if left_block == right_block:
            block_id = self._compute_block_id(self._arr[start_left:end_left])
            relative_idx = self._block_RMQs[block_id](relative_left, relative_right)
            return left_block * self._block_size + relative_idx

        # Find minima inside left and right edge blocks.
        left_block_id = self._compute_block_id(self._arr[start_left:end_left])
        right_block_id = self._compute_block_id(self._arr[start_right:end_right])
        relative_idx_left = self._block_RMQs[left_block_id](relative_left, self._block_size - 1)
        relative_idx_right = self._block_RMQs[right_block_id](0, relative_right)

        left_min_idx = left_block * self._block_size + relative_idx_left
        right_min_idx = right_block * self._block_size + relative_idx_right

        if left_block + 1 == right_block:
            return left_min_idx if self._arr[left_min_idx] <= self._arr[right_min_idx] else right_min_idx

        # Find minima in the summary structure.
        summary_idx = self._summary_RMQ(left_block + 1, right_block -1)
        relative_idx = self._index[summary_idx]
        middle_min_idx = summary_idx * self._block_size + relative_idx

        if (self._arr[left_min_idx] <= self._arr[middle_min_idx]
            and self._arr[left_min_idx] <= self._arr[right_min_idx]):
            return left_min_idx
        elif (self._arr[middle_min_idx] <= self._arr[left_min_idx]
            and self._arr[middle_min_idx] <= self._arr[right_min_idx]):
            return middle_min_idx
        else:
            return right_min_idx

    def _compute_block_id(self, block):
        """ Compute an id for each block. Similary blocks must have the same id. """
        raise NotImplementedError("This method must be implemented by the subclass")


class RMQ_1(RMQ_block):
    """ Concrete class implementing block decomposition stragety.
    This class implements an indexing structure for the case when all the elements
    of the array differ by +1 or -1.
    A mapping between b-sized blocks and b-bit integers is used to detect
    similar blocks.
    """
    def __init__(self, arr):
        """ Initialize an instance of the RMQ_1 class.
        Assert that every pair of consecutive elements differs by +/- 1.
        @param arr (List[int]): A list of integers.
        """
        super().__init__(arr)

        for i in range(len(arr) - 1):
            assert(arr[i]-arr[i+1]==1 or arr[i]-arr[i+1]==-1)

    def _compute_block_id(self, block):
        """ Compute an id for each block.
        Since consecutive elements differ by +/- 1, every block is unambiguously
        defined by the sequence of 1 or -1 jumps between consecutive elements.
        Mapping the sequence of jumps to a bit value of 1 or 0 results
        in a (*block_size* - 1)-bit integer number.
        This number is the id of the block.
        @param block (List[int]): An array of integer numbers. Every two
                                  consecutive numbers must differ by 1 or -1.
        @return code (int): A (b-1)-bit integer giving the id of the block,
                            where b is the size of the block.
        """
        binary_code = [0] * len(block)

        for i in range(len(block) - 1):
            if block[i] - block[i + 1] == 1:
                binary_code[i] =  1
            elif block[i] - block[i + 1] == -1:
                binary_code[i] = 0
            else:
                raise ValueError("RMQ must be +/- 1")

        code = "".join(str(bit) for bit in binary_code)
        return int(code, 2)


class RMQ_Fischer_Heun(RMQ_block):
    """ Concrete class implementing block decomposition stragety.
    This class implements an indexing structure for the general case.
    A mapping between b-sized blocks and 2b-bit integers is used to detect
    similar blocks.
    """
    def _compute_block_id(self, block):
        """ For every block build a Cartesian tree using stack-based approach.
        During the build process encode stack pushes as *1* and stack pops as *0*.
        The generated 2b-bit number is the id of the block.
        @param block (List[int]): An array of integer numbers.
        @return code (int): A 2b-bit integer giving the id of the block,
                            where b is the size of the block.
        """
        binary_code = [0] * (2* len(block))
        idx = 0
        Q = deque(maxlen=len(block))  # stack

        for i in range(len(block)):
            while (len(Q) > 0) and (Q[-1] > block[i]):
                Q.pop()
                idx += 1
            Q.append(block[i])
            binary_code[idx] = 1
            idx += 1

        code = "".join(str(bit) for bit in binary_code)
        return int(code, 2)


class RMQ_Index:
    """ Concrete class for RMQ indexing structure.
    The RMQ problem is reduced to the LCA problem by building a Cartesian tree
    for the array. Searching for a minimal element in a subarray amounts to
    finding the least common ancestor of the nodes representing the start and the
    end of that subarray.
    We keep an _index array storing positions of the nodes in the tree.
    The position stored at index *i* corresponds to the array element at index *i*.
    """
    def __init__(self, arr):
        """ Initialize an instance of the RMQ_Index class.
        @param arr (List[int]): A list of integers.
        """
        self._arr = arr
        self._length = len(arr)
        self._tree = BinaryTree()
        self._pos_index = self._tree.build_cartesian_tree(self._arr)
        self._lca = lca.LCA_Index(self._tree)

    def __call__(self, i, j):
        """ To answer queries locate the positions of the nodes storing indecies i and j.
        Find the least common ancestor of these nodes. And return the index stored at that node.
        @param i (int): Element index.
        @param j (int): Element index.
        @return k (int): Element index such that arr[k] = min arr[i...j]
        """
        u = self._pos_index[i]
        v = self._pos_index[j]
        w = self._lca(u, v)
        return w.value()


if __name__ == "__main__":
    print("true")

#