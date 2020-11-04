import math


from utils.tree import Tree
from utils.queue import Queue
from utils.traversal_algorithms import depth_first_traversal


class LA_base:
    """ Abstract base class for the LA indexing structure.
    Concrete subclasses must implement the methods _preprocess() and _query().
    """
    def __init__(self, tree):
        """ Initialize an instance of the LA_base class.
        @param tree (Tree): A tree object.
        """
        self._tree = tree
        self._size = len(tree)

        self._tree.reindex()
        self._preprocess()

    def _preprocess(self):
        """ Preprocess the tree. """
        raise NotImplementedError("This method must be implemented by the subclass")

    def _query(self, p, k):
        """ Query the preprocessed structure. Given a position to node u and an integer k
        return the level k ancestor of node u.
        @param p (Position): Position representing a node in the tree.
        @param k (int): An integer giving the level of the ancestor.
        @return ancestor (Position): Position of the level k ancestor of node at position p.
        """
        raise NotImplementedError("This method must be implemented by the subclass")

    def __call__(self, p, k):
        return self._query(p, k)


class LA_table(LA_base):
    """ Concrete class implementing table indexing strategy.
    Every possible query (p, k) is precomputed and the result is stored in a table.
    The size of the table is n^2. Computation of the level ancestor is performed
    using bottom-up dynamic programming in O(n^2) time.
    Querying is performed by a simple table look-up in O(1) time.
    """
    def _preprocess(self):
        """ Precompute all n^2 possible queries and store them in a table. """
        # A 2D table storing all possible queries.
        self._table = {}

        # Build the table using bottom-up dynamic programming.
        for p in self._tree.positions():
            self._table[p.index()] = [p]

            l = 0
            while (l <= self._tree.depth(p)):
                u = self._table[p.index()][l]
                w = self._tree.parent(u)
                self._table[p.index()].append(w)
                l += 1

    def _query(self, p, k):
        """ Perform simple table look-up. """
        if isinstance(p, int):
            if k >= len(self._table[p]):
                return None
            return self._table[p][k]

        # if k > self._tree.depth(p):
        if k >= len(self._table[p.index()]):
            return None
        return self._table[p.index()][k]


class LA_sparse(LA_base):
    """ Concrete class implementing sparse table indexing strategy.
    We perform a long-path decomposition of the tree. Each node belongs to a
    single path. We extend to long paths into ladders by doubling their lengths.
    Decomposition and doublying is porformed in O(n) time.
    For every node v, we precompute the ancestors at levels 1, 2, 4, 8, ..., 2^k
    and so on until we reach the root. We store the results in a table.
    The size of the table is nlogn and is computed in O(nlogn) time.

    To find the level k-th ancestor express k as k = 2^l + d (0 <= d < 2^l).
    Querying is performed by looking up in the table and retrieving the ancestor
    of level 2^l-th power. The answer to the query is the level d-th ancestor of
    the retrieved element. Querying is done in O(1) time.
    """
    def _preprocess(self):
        """ Decompose the tree into paths with maximal lengths. Extend the paths
        into ladders by doubling their length. Precompute a sparse table storing
        ancestors of levels 1, 2, 4, 8, ...., 2^k.
        """
        # Precompute a logarithm table. log[n] = k => 2^k <= n < 2^(k+1)
        self._log = [0] * (self._size + 1)
        temp = 1
        for i in range(1, self._size + 1):
            self._log[i] = self._log[i - 1]
            if temp * 2 <= i:
                self._log[i] += 1
                temp *= 2

        # Compute the log of the size of the tree.
        self._logsize = self._log[self._size] + 1

        # Precompute a power table. pow[k] = n => 2^k = n
        self._pow = [1] * (self._logsize + 1)
        for i in range(1, self._logsize):
            self._pow[i] = 2 * self._pow[i - 1]

        # Build a list of the jump nodes sorted by depth.
        self._build_jump_nodes()

        # Build a list of ladders.
        self._build_ladders()

        # Build a sparse table of ancestors of levels 1, 2, 4, 8, ...., 2^k only for the leaves.
        self._build_sparse_table()

    def _query(self, p, k):
        """ Answering lavel ancestor queries for a node p is performed at three steps. First we find
        the jump-node descendant of p and we precompute the level k. Then we jump to the ancestor
        of level 2^l using the jump pointer. Finally we look inside the ladder of the ancestor of 
        level 2^l.
        """
        if k > self._tree.depth(p):
            return None

        if k == 0:
            return p

        # Find the jump-node descendant of the node and recompute the query level.
        jump = self._jump[p.index()]
        k = k + self._tree.depth(jump) - self._tree.depth(p)

        l = self._log[k]        # k = 2^l + d
        d = k - self._pow[l]

        u = self._table[jump.index()][l]
        w = self._ladders[self._path[u.index()]][self._ind[u.index()] - d]

        return w

    def _build_jump_nodes(self):
        """ Build a list of jump nodes for the tree. Designate the leaves of the tree as
        jump nodes. Sort the list in linear time.
        """
        self._jump_nodes = [p for p in self._tree.positions() if self._tree.is_leaf(p)]
        self._jump_nodes.sort(key=lambda p: self._tree.depth(p), reverse=True)     # Bucket sort should be used !

    def _build_ladders(self):
        """ Build a list of ladders. """
        # List of ladders. Each ladder is a list of nodes.
        self._ladders = [None] * len(self._jump_nodes)

        # Array storing the index of the unique path containing the node.
        self._path = [None] * self._size

        # Index array storing the index of the node in the path which contains it.
        self._ind = [None] * self._size

        # Index array storing a pointer to the jump-node descendant of the node.
        self._jump = [None] * self._size

        # Decompose the tree into paths with maximal lengths.
        marked = {p.index() : False for p in self._tree.positions()}
        for idx, jump in enumerate(self._jump_nodes):
            # Greedy build of a path.
            ladder = []
            curr = jump
            while (curr is not None) and not (marked[curr.index()]):
                ladder.append(curr)
                marked[curr.index()] = True
                self._path[curr.index()] = idx
                self._ind[curr.index()] = len(ladder) - 1
                self._jump[curr.index()] = jump
                curr = self._tree.parent(curr)

            # Double path to build a ladder.
            path_size = len(ladder)
            while (curr is not None) and len(ladder) < 2 * path_size:
                ladder.append(curr)
                curr = self._tree.parent(curr)

            # Reverse the ladder.
            ladder_size = len(ladder)
            for i in range(path_size):
                node = ladder[i]
                self._ind[node.index()] = ladder_size - self._ind[node.index()] - 1
            ladder.reverse()

            # Add ladder to the list of ladders.
            self._ladders[idx] = ladder

    def _build_sparse_table(self):
        """ Build a sparse table of ancestors of levels 1, 2, 4, 8, ...., 2^k only for the leaves. """
        self._table = {}

        for p in self._jump_nodes:
            self._table[p.index()] = [self._tree.parent(p)]       # table[p][0] = parent(p)

            l = 0
            while l < self._logsize:
                u = self._table[p.index()][l]

                if u is None:
                    break

                if self._ind[u.index()] < self._pow[l]:     # incomplete ladder
                    break

                i = self._path[u.index()]                   # u belongs to path_i
                j = self._ind[u.index()]                    # path_i[j] = u
                w = self._ladders[i][j - self._pow[l]]
                self._table[p.index()].append(w)
                l += 1


class LA_macro_micro(LA_sparse):
    """ Concrete class implementing the macro-micro tree strategy.
    We divide the tree into a macro tree and disjoint micro trees. We perform
    ladder decomposition of the tree and designate the macro leaves as jump nodes.
    We enumerate all possible shapes of the micro trees and precompute a simple
    table for every shape.

    To answer level ancestor queries we check wheter the node belongs to the
    macro tree or to one of the micro trees. Querying the macro tree is done
    using the ladder decomposition and querying the micro trees is done using
    table lookup. Querying takes O(1) time.
    """
    def _preprocess(self):
        """ Divide the tree into a marco tree and disjoint micro trees. Build a ladder
        decomposition of the entire tree and compute a sparse table for the jump nodes.
        Enumerate all possible shapes of the micro trees and build a simple table for
        every shape.
        """
        # Size of each micro tree: B = 1/4 logn.
        self._block_size = int(1/4 * math.log2(self._size))

        # Build a list of ladders and a sparse table for the jump nodes.
        super()._preprocess()

        # Decompose the tree into macro tree and micro trees.
        self._micro_macro_decomposition()

        # Build simple tables for the micro trees.
        self._build_micro_tree_tables()

    def _query(self, p, k):
        """ To answer level ancestor queries we first check whether the node is a macro node or
        a micro node. For macro nodes we query the macro structure using ladders and jump ponters.
        For micro nodes we check wheter the level ancestor is a macro node or a micro node. If the
        level ancestor is a macro node we again query the macro structure. If the level ancestor is
        a micro node we query the simple table for the micro tree.
        """
        if self._tree.height(p) > self._block_size:                         # macro node
            return super()._query(p, k)
        else:                                                               # micro node
            root = self._root[p.index()]                                    # root of the micro tree
            if k > (self._tree.depth(p) - self._tree.depth(root)):
                parent = self._tree.parent(root)
                k = k - (self._tree.depth(p) - self._tree.depth(root)) - 1
                return super()._query(parent, k)                            # query the macro tree
            else:
                code, f, f_inv = self._codes[root.index()]
                table = self._micro_tables[code]
                ancestor = table(f[p.index()], k)                           # query the micro tree
                result = f_inv[ancestor.elem()]
                return result

    def _build_jump_nodes(self):
        """ Build a list of jump nodes for the tree.
        Designate the macro leaves (the leaves of the macro tree) as jump nodes.
        Sort the list in linear time.
        """
        self._jump_nodes = []
        Q = Queue()
        Q.enqueue(self._tree.root())

        while not Q.is_empty():
            p = Q.dequeue()

            if self._tree.height(p) > self._block_size:
                for ch in self._tree.children(p):
                    if self._tree.height(ch) <= self._block_size:
                        if p not in self._jump_nodes:
                            self._jump_nodes.append(p)
                    else:
                        Q.enqueue(ch)

        # Bucket sort should be used for sorting!
        self._jump_nodes.sort(key=lambda p: self._tree.depth(p), reverse=True)

    def _micro_macro_decomposition(self):
        """ Build a list of the macro leaves and a list of the micro roots of the tree.
        Store a mapping that associates every micro node with the root of its micro tree.
        """
        # Store the roots of all micro trees.
        self._micro_roots = []

        # A mapping that associates every micro node with the root of its micro tree.
        self._root = {}

        # Index array storing for every micro node a pointer to the root of its micro tree.
        self._root = [None] * self._size
        for p in depth_first_traversal(self._tree):
            if self._tree.height(p) <= self._block_size:            # micro node
                parent = self._tree.parent(p)
                if self._tree.height(parent) > self._block_size:    # root of a micro tree
                    self._micro_roots.append(p)
                    self._root[p.index()] = p
                else:
                    self._root[p.index()] = self._root[parent.index()]

    def _build_micro_tree_tables(self):
        """ Encode every micro tree. Build a simple table for the micro trees with
        different shapes (different codes).
        """
        # A mapping that associates micro tree encoding with its corresponding table.
        self._micro_tables = {}

        # A mapping that stores the encoding of each micro tree.
        self._codes = {}

        # For every micro tree compute a simle table to answer LA queries.
        for p in self._micro_roots:
            code, f, f_inv = self._encode(p)            # encode the micro tree
            self._codes[p.index()] = code, f, f_inv
            if code not in self._micro_tables:          # build a simple table if needed
                repr_tree = self._decode(code)
                self._micro_tables[code] = LA_table(repr_tree)

    def _encode(self, p):
        """ Given a position encode the subtree rooted at that node.
        @param p (Position): Position representing the micro root of the micro tree.
        @return code (int): A 2b-bit integer giving the id of the subtree,
                            where b is the size of the subtree.
        @return f (Dict): A mapping that associates every node of the micro tree with a node
                          of the representative tree.
        @return f_inv (Dict): An inverse mapping.
        """
        binary_code = [1]
        f = {}
        f_inv = {}
        idx = 0

        def dfs(q):
            nonlocal idx
            f[q.index()] = idx
            f_inv[idx] = q
            idx += 1

            for ch in self._tree.children(q):
                binary_code.append(0)
                dfs(ch)
                binary_code.append(1)
        dfs(p)
        code = "".join(str(bit) for bit in binary_code)
        return int(code, 2), f, f_inv

    def _decode(self, code):
        """ Given a binary code build a tree corresponding to that code.
        @param code (int):  A 2b-bit number encoding a tree of size b.
        @return tree (Tree): A Tree object corresponding to the binary encoding.
        """
        binary_code = [int(bit) for bit in "{0:b}".format(code)]
        binary_code = binary_code[1:]

        # Assert the binary code is a valid encoding of a tree.
        zeros = len([x for x in binary_code if x == 0])
        ones = len([x for x in binary_code if x == 1])
        assert(zeros == ones)

        tree = Tree()
        elem = 0
        cursor = tree.add_root(elem)
        for bit in binary_code:
            if bit == 0:
                elem += 1
                cursor = tree.add_child(cursor, elem)
            elif bit == 1:
                cursor = tree.parent(cursor)

        return tree

#