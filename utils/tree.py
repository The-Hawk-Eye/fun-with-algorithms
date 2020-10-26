""" The tree data structure is defined using the concept of *position*
as an abstraction for a node of a tree.
The tree data structure supports the following accessor methods in addition
to the accessor methods supported by the positional container ADT:
    T.root(): Return the Position of the root of the tree T.
    T.parent(p): Return the Position of the parent of Position p.
    T.num_children(p): Return the number of children of Position p.
    T.children(p): Generate an iteration of the children of Position p.
    T.depth(p): Return the depth of the node at Position p.
    T.is_root(p): Return True if Position p is the root of T.
    T.is_leaf(p): Return True if Position p does not have any children.
    T.positions(strategy): Generate an iteration of all positions of tree T
                           using the given strategy for tree traversal.

The tree data structure also supports the following mutator methods in addition
to the mutator methods supported by the positional container ADT:
    T.add_root(elem): Place a node with the given element at the root of an empty tree.
    T.add_child(p, elem): Create a new child with the given element for node at Position p.
    T.replace(p, elem): Replace the element at the node at Position p with the new elem.
"""

from .positional_container import PositionalContainer
from .traversal_algorithms import breadth_first_traversal

class Tree(PositionalContainer):
    #---------------- nested Node class ----------------------#
    class _Node:
        """ Lightweight non-public class for storing a node.
        Overwrite the nested Node class.
        """
        __slots__ = "_elem", "_index", "_depth", "_parent", "_children"
        def __init__(self, elem, idx, depth, parent=None, children=None):
            """ Initialize a _Node instance.
            @param elem: Element stored at the node.
            @param idx (int): Integer used to uniquely identify a Node object.
            @param depth (int): Depth of the node from the root of the tree.
            @param parent (Node): The parent of the node.
            @param children (List[Node]): A list of Nodes representing
                                              the children of the node.
            """
            self._elem = elem
            self._index = idx
            self._depth = depth
            self._parent = parent
            self._children = children if children is not None else []

    #---------------- tree initializer ----------------#
    def __init__(self):
        """ Initialize an empty tree. """
        self._root = None
        self._size = 0

    #---------------- public accessors ----------------#
    def root(self):
        """ Return Position representing the root of the tree. """
        return self._make_position(self._root)

    def parent(self, p):
        """ Return Position representing the parent of the node at Position p.
        @param p (Position): Position representing the node in the tree.
        @returns parent (Position): Position representing the parent of that node.
        """
        node = self._validate(p)
        return self._make_position(node._parent)

    def num_children(self, p):
        """ Return the number of children of the node at Position p.
        @param p (Position): Position representing the node in the tree.
        @return num (int): The number of children of that node.
        """
        node = self._validate(p)
        return len(node._children)

    def children(self, p):
        """ Generate an iteration of Position representing the children of p.
        @param p (Position): Position representing the node in the tree.
        @yield child (Position): Yields a position representing a child of that node.
        """
        node = self._validate(p)
        for child in node._children:
            yield self._make_position(child)

    def depth(self, p):
        """ Return the depth of the node at Position p.
        @param p (Position): Position representing the node in the tree.
        @return depth (int): The depth of the node from the root of the tree.
        """
        node = self._validate(p)
        return node._depth

    def is_root(self, p):
        """ Return True if Position p represents the root of the tree. """
        return self.root() == p

    def is_leaf(self, p):
        """ Return True if Position p dos not have any children. """
        return self.num_children(p) == 0

    def positions(self, strategy=breadth_first_traversal):
        """ Generate an iteration of all positions of the tree.
        @param strategy (func): A function implementing the strategy for tree traversal.
                                Default is breadth-first traversal.
        @yield p (Position): Position representing the node in the tree.
        """
        for p in strategy(self):
            yield p

    #---------------- public mutators ----------------#
    def add_root(self, elem):
        """ Place a node with the given element at the root of an empty tree.
        Raise ValueError if the tree is not empty.
        @param elem: Element to be stored at the node.
        @return root (Position): Return Position representing the root of the tree.
        """
        if self._root is not None:
            raise ValueError("Root exists")
        self._root = self._Node(elem, idx=0, depth=0)
        self._size = 1
        return self._make_position(self._root)

    def add_child(self, p, elem):
        """ Create a new child with the given element for node at Position p.
        @param p (Position): Position representing the node in the tree.
        @param elem: Element to be stored at the child.
        @return child (Position): Return Position representing the new child.
        """
        node = self._validate(p)
        child = self._Node(elem, idx=self._size, depth=self.depth(p) + 1, parent=node)
        node._children.append(child)
        self._size += 1
        return self._make_position(child)

    #---- private methods - should not be invoked by the user ----#
    def _insert(self, p, elem):
        """ Insert a new node at Position p. Attach the subtree rooted at the existing
        node as a child of the new node. Note that the depths of the nodes must be recomputed
        after executing the method _insert.
        @param p (Position): Position representing the node in the tree.
        @param elem: Element to be stored at the new node.
        @return new_p (Position): Return Position representing the new node.
        """
        node = self._validate(p)
        new_node = self._Node(elem, idx=self._size, depth=node._depth, parent=node._parent)
        node._parent = new_node
        new_node._children.append(node)
        self._size += 1
        return self._make_position(new_node)

    def _compute_depths(self):
        """ Traverse the tree in a breadth first manner and compute the depth
        of each node from the root of the tree.
        """
        for p in breadth_first_traversal(self):
            node = self._validate(p)
            if p == self.root():
                node._depth = 0
            else:
                parent = self.parent(p)
                parent_node = self._validate(parent)
                node._depth = parent_node._depth + 1

#