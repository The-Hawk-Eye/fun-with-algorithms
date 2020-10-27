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
        self._table = [[None] for i in range(self._size)]

        # Build the table using bottom-up dynamic programming.
        for p in self._tree.positions():
            self._table[p.index()][0] = p

            l = 0
            parent = self._tree.parent(p)
            while (l < self._size - 1) and (parent is not None):
                u = self._table[p.index()][l]
                w = self._tree.parent(u)
                self._table[p.index()].append(w)

                l += 1
                parent = self._tree.parent(w)

    def _query(self, p, k):
        """ Perform simple table look-up. """
        if k > self._tree.depth(p):
        # if k >= len(self._table[p.index()]):
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
        into ladders by doubling their length. Precompute a sparse table storying
        ancestors of levels 1, 2, 4, 8, ...., 2^k.
        """
        self._tree._reindex()

        # Build a list of leaves and sort in linear time.
        self._leaves = [p for p in self._tree.positions() if self._tree.is_leaf(p)]
        self._leaves.sort(key=lambda p: self._tree.depth(p))     # Bucket sort should be used !

        # List of ladders. Each ladder is a list of nodes.
        self._ladders = [None] * len(self._leaves)

        # Array storing the index of the unique path containing the node.
        self._path = [None] * self._size

        # Index array storing the index of the node in the path which contains it.
        self._ind = [None] * self._size

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

        # Build a list of ladders.
        marked = {p.index() : False for p in self._tree.positions()}
        for idx, leaf in enumerate(self._leaves):
            # Greedy build of a path.
            ladder = []
            curr = leaf
            while (curr is not None) and not (marked[curr.index()]):
                ladder.append(curr)
                marked[curr.index()] = True
                self._path[curr.index()] = idx
                self._ind[curr.index()] = len(ladder)
                curr = self._tree.parent(curr)

            # Double path to build a ladder.
            path_size = len(ladder)
            while (curr is not None) and len(ladder) < 2 * path_size:
                ladder.append(curr)
                curr = self._tree.parent(curr)

            # Reverse the ladder.
            ladder_size = len(ladder)
            for i in range(path_size):
                node = ladder[i].index()
                self._ind[node] = ladder_size - self._ind[node] - 1
            ladder.reverse()

            # Add ladder to the list of ladders.
            self._ladders[idx] = ladder

        # Build a sparse table of ancestors of levels 1, 2, 4, 8, ...., 2^k
        self._table = [None] * self._size
        for p in self._tree.positions():
            self._table[p.index()] = [p]

            l = 0
            while l < self._logsize:
                u = self._table[p.index()][l]

                if self._ind[u.index()] + 1 < self._pow[l]:     # incomplete ladder
                    break

                w = self._ladders[self._path[u.index()]][self._ind[u.index()] - self._pow[l] + 1]
                self._table[p.index()].append(w)
                l += 1

    def _query(self, p, k):
        if k > self._tree.depth(p):
            return None

        l = self._log[k]        # k = 2^l + d
        d = k - self._pow[l]

        u = self._table[p.index()][l]
        w = self._ladders[self._path[u.index()]][self._ind[u.index()] - d]

        return w

#