import time
import random
import sys
sys.path.append("..")

from collections import deque
from utils.tree import Tree
import rmq

class LCA_Index:
    def __init__(self, tree):
        """ Constructs an LCA index for the tree object.
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


if __name__ == "__main__":
    random.seed(0)

    def generate_random_tree(size):
        """ Generate a tree of given size. Every node has a random number
        of children (between 1 and 3 children). """
        MAX_VAL = 100000
        T = Tree()
        frontier = deque()

        root = T._add_root(random.randint(0, MAX_VAL))
        frontier.append(root)
        while len(T) < size:
            # Pop first node from frontier.
            node = frontier.popleft()

            # Add random number of children to node.
            num_children = min(random.randint(1, 3), size - len(T))
            for i in range(num_children):
                value = random.randint(1, MAX_VAL)
                T._add_child(node, value)

            # Add node children to frontier.
            frontier.extend(T.children(node))
        return T

    def get_random_position(T):
        """ Walk along the tree in a beam-search manner. Stop at a random node. """
        p = T.root()
        while True:
            # If reached a leaf, return the node.
            if T.is_leaf(p):
                return p

            # 25% chance to stop and return the current node.
            flag = random.randint(0, 3)
            if not flag:
                return p

            # Continue in-deapth search at a random child.
            child_idx = random.randint(0, T.num_children(p) - 1)
            p = list(T.children(p))[child_idx]

        return p

    def find_parent_naive(T, p, q):
        """ Find least common ancestor naively. """
        while p != q:
            if T.depth(p) < T.depth(q):
                q = T.parent(q)
            elif T.depth(p) > T.depth(q):
                p = T.parent(p)
            else:
                p = T.parent(p)
                q = T.parent(q)
        return p

    def check_correctness(LCA):
        sizes = [10, 100, 1000, 10000, 100000]
        trials = 200

        for size in sizes:
            T = generate_random_tree(size)
            lca = LCA(T)
            for i in range(trials):
                p = get_random_position(T)
                q = get_random_position(T)
                w = lca(p, q)
                u = find_parent_naive(T, p, q)
                if w != u:
                    raise Exception("%s not implemented correctly!" % (lca.__class__.__name__))

        print("%s implementation is correct!" % (lca.__class__.__name__))

    check_correctness(LCA_Index)