import sys
sys.path.append("../utils/")
sys.setrecursionlimit(10000)

from tree import Tree
import rmq

class LCA_Index:
    def __init__(self, tree):
        """ Initialize an LCA index for the tree object.
        @param tree (Tree): A tree object.
        """
        self._tree = tree
        self._visits = []
        self._levels = []
        self._start = [0] * len(tree)

        self._time = 0
        self._reduce(tree.root())
        self._rmq = rmq.RMQ_1(self._levels)

    def _reduce(self, p):
        """ Reduce the LCA problem to RMQ problem using recursive depth-first traversal.
        This function recursively builds the arrays needed for the RMQ problem. It should
        not be invoked by the user.
        @param p (Position): Position representing the node in the tree.
        """
        self._visits.append(p)
        self._levels.append(self._tree.depth(p))
        self._start[p.index()] = self._time

        for q in self._tree.children(p):
            self._time += 1
            self._reduce(q)
            self._visits.append(p)
            self._levels.append(self._tree.depth(p))

        self._time += 1

    def __call__(self, p, q):
        """ Given the positions of two nodes in the tree, finds the
        least common ancestor of the two nodes.
        @param p (Position): Position representing a node in the tree.
        @param q (Position): Position representing a node in the tree.
        @return w (Position): Position of the least common ancestor of nodes
                              at positions p and q.
        """
        idx = self._rmq(self._start[p.index()], self._start[q.index()])
        return self._visits[idx]