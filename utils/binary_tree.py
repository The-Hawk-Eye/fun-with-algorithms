""" The binary tree data structure is a specialization of a tree and supports
the following additional accessor methods:
    T.left(p): Return the position that represents the left child of p.
    T.right(p): Return the position that represents the right child of p.

The binary tree data structure also supports the following mutator methods:
    T.add_left(p, elem): Create a left child with the given element for node at Position p.
    T.add_right(p, elem): Create a right child with the given element for node at Position p.
    T.build_cartesian_tree(arr): Build a Cartesian Tree for the given array.
"""

from .tree import Tree
from .stack import Stack

class BinaryTree(Tree):
    #---------------- nested Node class ----------------------#
    class _Node:
        """ Lightweight non-public class for storing a node.
        Overwrite the nested Node class.
        """
        __slots__ = "_elem", "_index", "_parent", "_left", "_right"
        def __init__(self, elem, idx, parent=None, left=None, right=None):
            """ Initialize a _Node instance.
            @param elem: Element stored at the node.
            @param idx (int): Integer used to uniquely identify a Node object.
            @param parent (Node): The parent of the node.
            @param left (Node): Left child of the node.
            @param right (Node): Right child of the node.
            """
            self._elem = elem
            self._index = idx
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
    def add_left(self, p, elem):
        """ Create a left child with the given element for node at Position p.
        Raise ValueError if node at Position p already has a left child.
        @param p (Position): Position representing the node in the tree.
        @param elem: Element to be stored at the left child.
        @return child (Position): Return Position representing the new child.
        """
        node = self._validate(p)
        if node._left is not None:
            raise ValueError("Left child exists!")

        left_ch = self._Node(elem, idx=self._curr_idx, parent=node)
        self._curr_idx += 1
        node._left = left_ch
        self._size += 1

        # Invalidate depths and heights after modifying the tree.
        self._depths, self._heights = None, None

        return self._make_position(left_ch)

    def add_right(self, p, elem):
        """ Create a right child with the given element for node at Position p.
        Raise ValueError if node at Position p already has a right child.
        @param p (Position): Position representing the node in the tree.
        @param elem: Element to be stored at the right child.
        @return child (Position): Return Position representing the new child.
        """
        node = self._validate(p)
        if node._right is not None:
            raise ValueError("Right child exists!")

        right_ch = self._Node(elem, idx=self._curr_idx, parent=node)
        self._curr_idx += 1
        node._right = right_ch
        self._size += 1

        # Invalidate depths and heights after modifying the tree.
        self._depths, self._heights = None, None

        return self._make_position(right_ch)

    def add_child(self, p, elem):
        """ Overwrite the _add_child method.
        Try to create a left child with the given element for node at position p.
        If the node already has a left child then try to create a right child.
        Raise ValueError if the node has both a left and a right child.
        @param p (Position): Position representing the node in the tree.
        @param elem: Element to be stored at the child.
        @return child (Position): Return Position representing the new child.
        """
        if self.left(p) is None:
            return self.add_left(p, elem)
        elif self.right(p) is None:
            return self.add_right(p, elem)
        else:
            raise ValueError("The node already has two children!")

    def insert(self, p, elem, left=True):
        """ Overwrite the _insert method.
        Insert a new node at Position p. Attach the subtree rooted at the existing node
        as a child of the new node. Note that the depths of the nodes must be recomputed
        after executing the method _insert.
        @param p (Position): Position representing the node in the tree.
        @param elem: Element to be stored at the new node.
        @param left (bool): If True attach the subtree as the left child of the node.
                            Otherwise attach as the right child of the node.
        @return new_p (Position): Return Position representing the new node.
        """
        node = self._validate(p)
        new_node = self._Node(elem, idx=self._curr_idx, parent=node._parent)
        self._curr_idx += 1
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

        # Invalidate depths and heights after modifying the tree.
        self._depths, self._heights = None, None

        return self._make_position(new_node)

    def build_cartesian_tree(self, arr):
        """ Build a Cartesian Tree for the given array. Each nodes of the tree
        stores the index of the element in the array.
        Build an auxiliary array storing the position of each node in the tree.
        @param arr (List[int]): A list of integers.
        @return pos_index (List[Position]): A list of Positions. pos[i] stores the position
                                            of the node with element the index i.
        """
        # Set the self instance to an empty tree.
        self._root = None
        self._size = 0
        self._curr_idx = 0

        # Maintaining a stack of the nodes in the right spine.
        S = Stack()
        last_pop = None

        # Iterate through the array and insert the new nodes. Store the position of the Node.
        pos_index = [None] * len(arr)
        for i in range(len(arr)):
            while (not S.is_empty()) and (arr[S.top().elem()] > arr[i]):
                last_pop = S.pop()
            if self.is_empty():
                p = self.add_root(i)
            elif last_pop is None:
                p = self.add_right(S.top(), i)
            else:
                p = self.insert(last_pop, i, left=True)

            pos_index[i] = p
            S.push(p)
            last_pop = None

        # Recompute the indices, depths, and heights of the nodes after building the tree.
        self.reindex()

        return pos_index

#