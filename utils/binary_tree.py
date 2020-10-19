""" The binary tree ADT is defined using the concept of *position* as an
abstraction for a node of a tree. The position object supports
the method:
    p.value(): Return the value of the node at Position p.
    p.index(): Return the index of the node at Position p.

The binary tree ADT is a specialization of a tree and supports the following
additional accessor methods:
    T.left(p): Return the position that represents the left child of p.
    T.right(p): Return the position that represents the right child of p.

The binary tree ADT also supports the following mutator methods:
    T.add_left(p, val): Create a left child with the given value for node at Position p.
    T.add_right(p, val): Create a right child with the given value for node at Position p.
    T.build_cartesian_tree(arr): Build a Cartesian Tree for the given array.
"""

from collections import deque
from tree import Tree

class BinaryTree(Tree):
    #---------------- nested Node class ----------------------#
    class _Node:
        """ Lightweight non-public class for storing a node.
        Overwrite the nested Node class.
        """
        __slots__ = "_value", "_index", "_depth", "_parent", "_left", "_right"
        def __init__(self, value, idx, depth, parent=None, left=None, right=None):
            """ Initialize a _Node instance.
            @param value: Value stored by the node.
            @param idx (int): Integer used to uniquely identify a Node object.
            @param depth (int): Depth of the node from the root of the tree.
            @param parent (Node): The parent of the node.
            @param left (Node): Left child of the node.
            @param right (Node): Right child of the node.
            """
            self._value = value
            self._index = idx
            self._depth = depth
            self._parent = parent
            self._left = left
            self._right = right

    #---------------- public accessors ----------------#
    def left(self, p):
        """ Return the position of the left child of p.
        Return None if p has no left child.
        @param p (Position): Position representing the node in the tree.
        @return left_ch (Position): Position of the left child of p.
        """
        node = self._validate(p)
        left_ch = self._make_position(node._left)
        return left_ch

    def right(self, p):
        """ Return the position of the right child of p.
        Return None if p has no right child.
        @param p (Position): Position representing the node in the tree.
        @return right_ch (Position): Position of the right child of p.
        """
        node = self._validate(p)
        right_ch = self._make_position(node._right)
        return right_ch

    def num_children(self, p):
        """ Overwrite the num_children method. """
        node = self._validate(p)
        count = 0
        if node._left is not None:      # left child exists
            count += 1
        if node._right is not None:     # right child exists
            count += 1
        return count

    def children(self, p):
        """ Overwrite the children method. """
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)

    #---------------- public mutators ----------------#
    def add_left(self, p, val):
        """ Create a left child with the given value for node at Position p.
        Raise ValueError if node at Position p already has a left child.
        @param p (Position): Position representing the node in the tree.
        @param val: Value to be stored at the left child.
        @return child (Position): Return Position representing the new child.
        """
        node = self._validate(p)
        if node._left is not None:
            raise ValueError("Left child exists!")

        left_ch = self._Node(val, idx=self._size, depth=self.depth(p) + 1, parent=node)
        node._left = left_ch
        self._size += 1
        return self._make_position(left_ch)

    def add_right(self, p, val):
        """ Create a right child with the given value for node at Position p.
        Raise ValueError if node at Position p already has a right child.
        @param p (Position): Position representing the node in the tree.
        @param val: Value to be stored at the right child.
        @return child (Position): Return Position representing the new child.
        """
        node = self._validate(p)
        if node._right is not None:
            raise ValueError("Right child exists!")

        right_ch = self._Node(val, idx=self._size, depth=self.depth(p) + 1, parent=node)
        node._right = right_ch
        self._size += 1
        return self._make_position(right_ch)

    def add_child(self, p, val):
        """ Overwrite the _add_child method.
        Try to create a left child with the given value for node at position p.
        If the node already has a left child then try to create a right child.
        Raise ValueError if the node has both a left and a right child.
        @param p (Position): Position representing the node in the tree.
        @param val: Value to be stored at the child.
        @return child (Position): Return Position representing the new child.
        """
        if self.left(p) is None:
            return self.add_left(p, val)
        elif self.right(p) is None:
            return self.add_right(p, val)
        else:
            raise ValueError("The node already has two children!")

    def build_cartesian_tree(self, arr):
        """ Build a Cartesian Tree for the given array. Each nodes of the tree
        stores the index of the element in the array.
        Build an auxiliary array storing the position of each node in the tree.
        @param arr (List[int]): A list of integers.
        @return pos_index (list[Position]): A list of Positions. pos[i] stores the position
                                            of the node with value the index i.
        """
        # Set the self instance to an empty tree.
        self._root = None
        self._size = 0

        # Maintaining a stack of the nodes in the right spine.
        Q = deque(maxlen=len(arr))  # stack
        last_pop = None

        # Iterate through the array and insert the new nodes. Store the position of the Node.
        pos_index = [None] * len(arr)
        for i in range(len(arr)):
            while (len(Q) > 0) and (arr[Q[-1].value()] > arr[i]):
                last_pop = Q.pop()
            if self.is_empty():
                p = self.add_root(i)
            elif last_pop is None:
                p = self.add_right(Q[-1], i)
            else:
                p = self._insert(last_pop, i, left=True)

            pos_index[i] = p
            Q.append(p)
            last_pop = None

        # Recompute the depths of the nodes after building the tree.
        self._compute_depths()

        return pos_index

    #---- private methods - should not be invoked by the user ----#
    def _insert(self, p, val, left=True):
        """ Overwrite the _insert method.
        Insert a new node at Position p. Attach the subtree rooted at the existing node
        as a child of the new node. Note that the depths of the nodes must be recomputed
        after executing the method _insert.
        @param p (Position): Position representing the node in the tree.
        @param val: Value to be stored at the new node.
        @param left (bool): If True attach the subtree as the left child of the node.
                            Otherwise attach as the right child of the node.
        @return new_p (Position): Return Position representing the new node.
        """
        node = self._validate(p)
        new_node = self._Node(val, idx=self._size, depth=node._depth, parent=node._parent)
        if left:
            new_node._left = node
        else:
            new_node._right = node
        self._size += 1

        if p == self.root():
            self._root = new_node
        else:
            parent = node._parent
            if parent._left == node:
                parent._left = new_node
            else:
                parent._right = new_node

        node._parent = new_node
        return self._make_position(new_node)