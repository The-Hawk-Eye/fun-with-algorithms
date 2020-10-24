""" The tree ADT is defined using the concept of *position* as an
abstraction for a node of a tree. The position object supports
the method:
    p.value(): Return the value of the node at Position p.
    p.index(): Return the index of the node at Position p.

The tree ADT supports the following accessor methods:
    T.root(): Return the Position of the root of the tree T.
    T.parent(p): Return the Position of the parent of Position p.
    T.num_children(p): Return the number of children of Position p.
    T.children(p): Generate an iteration of the children of Position p.
    T.depth(p): Return the depth of the node at Position p.
    T.is_root(p): Return True if Position p is the root of T.
    T.is_leaf(p): Return True if Position p does not have any children.
    T.is_empty(): Return True if tree T does not contain any nodes.
    T.positions(strategy): Generate an iteration of all positions of tree T
                           using the given strategy for tree traversal.
    iter(T): Generate an iteration of the values of the nodes of tree T.
    len(T): Return the total number of nodes in the tree T.

The tree ADT also supports the following mutator methods:
    T.add_root(val): Place a node with the given value at the root of an empty tree.
    T.add_child(p, val): Create a new child with the given value for node at Position p.
    T.replace(p, val): Replace the value of the node at Position p with the new value.
"""

from .traversal_algorithms import breadth_first_traversal

class Tree:
    #---------------- nested Node class ----------------------#
    class _Node:
        """ Lightweight non-public class for storing a node. """
        __slots__ = "_value", "_index", "_depth", "_parent", "_children"
        def __init__(self, value, idx, depth, parent=None, children=None):
            """ Initialize a _Node instance.
            @param value: Value stored by the node.
            @param idx (int): Integer used to uniquely identify a Node object.
            @param depth (int): Depth of the node from the root of the tree.
            @param parent (Node): The parent of the node.
            @param children (List[Node]): A list of Nodes representing
                                              the children of the node.
            """
            self._value = value
            self._index = idx
            self._depth = depth
            self._parent = parent
            self._children = children if children is not None else []

    #----------------- nested Position class ------------------#
    class Position:
        def __init__(self, container, node):
            """ Initialize a Position. Constructor should not be invoked
            by the user.
            @param container (Tree): Tree object to which the node belongs.
            @param node (Node): Node object.
            """
            self._container = container     # this is used to check whether two positions
                                            # represent nodes in the same container structure
            self._node = node

        def value(self):
            """ Return the value of the node at this Position. """
            return self._node._value

        def index(self):
            """ Return the index of the node at this Position. """
            return self._node._index

        def __eq__(self, other):
            """ Return True if other is a Position representing the same location.
            @param other (Position): Position representing a node in the tree.
            @return equal (bool): Boolean True or False.
            """
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other):
            """ Return True if other Position does not represent the same location.
            @param other (Position): Position representing a node in the tree.
            @return equal (bool): Boolean True or False.
            """
            return not (self == other)

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

    def is_empty(self):
        """ Return True if the tree is empty. """
        return len(self) == 0

    def positions(self, strategy=breadth_first_traversal):
        """ Generate an iteration of all positions of the tree.
        @param strategy (func): A function implementing the strategy for tree traversal.
                                Default is breadth-first traversal.
        @yield p (Position): Position representing the node in the tree.
        """
        for p in strategy(self):
            yield p

    def __iter__(self):
        """ Generate an iteration of all the values of the nodes of the tree. """
        for p in self.positions():
            yield p.value()

    def __len__(self):
        """ Return the total number of nodes in the tree. """
        return self._size

    #---------------- public mutators ----------------#
    def add_root(self, val):
        """ Place a node with the given value at the root of an empty tree.
        Raise ValueError if the tree is not empty.
        @param val: Value to be stored at the node.
        @return root (Position): Return Position representing the root of the tree.
        """
        if self._root is not None:
            raise ValueError("Root exists")
        self._root = self._Node(val, idx=0, depth=0)
        self._size = 1
        return self._make_position(self._root)

    def add_child(self, p, val):
        """ Create a new child with the given value for node at Position p.
        @param p (Position): Position representing the node in the tree.
        @param val: Value to be stored at the child.
        @return child (Position): Return Position representing the new child.
        """
        node = self._validate(p)
        child = self._Node(val, idx=self._size, depth=self.depth(p) + 1, parent=node)
        node._children.append(child)
        self._size += 1
        return self._make_position(child)

    def replace(self, p, val):
        """ Replace the value of the node at Position p with the new value.
        @param p (Position): Position representing the node in the tree.
        @param val: Value to be stored at the node.
        @return old: Return the old value stored at the node.
        """
        node = self._validate(p)
        old = node._value
        node._value = val
        return old

    #---- private methods - should not be invoked by the user ----#
    def _make_position(self, node):
        """ Return Position instance for given node (or None if no node). """
        return self.Position(self, node) if node is not None else None

    def _validate(self, p):
        """ Return associated node, if Position is valid. """
        if not isinstance(p, self.Position):
            raise TypeError("p must be proper Position type")
        if p._container is not self:
            raise ValueError("p does not belong to this container")
        if p._node._parent is p._node:  # convention for deprecated nodes
            raise ValueError("p is no longer valid")
        return p._node

    def _insert(self, p, val):
        """ Insert a new node at Position p. Attach the subtree rooted at the existing
        node as a child of the new node. Note that the depths of the nodes must be recomputed
        after executing the method _insert.
        @param p (Position): Position representing the node in the tree.
        @param val: Value to be stored at the new node.
        @return new_p (Position): Return Position representing the new node.
        """
        node = self._validate(p)
        new_node = self._Node(val, idx=self._size, depth=node._depth, parent=node._parent)
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