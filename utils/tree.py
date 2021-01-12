""" The tree data structure is defined using the concept of *position*
as an abstraction for a node of a tree.
The tree data structure supports the following accessor methods in addition
to the accessor methods supported by the positional container ADT:
    T.root(): Return the Position of the root of the tree T.
    T.parent(p): Return the Position of the parent of Position p.
    T.num_children(p): Return the number of children of Position p.
    T.children(p): Generate an iteration of the children of Position p.
    T.depth(p): Return the depth of the node at Position p.
    T.height(p): Return the height of the node at Position p.
    T.is_root(p): Return True if Position p is the root of T.
    T.is_leaf(p): Return True if Position p does not have any children.
    T.positions(): Generate an iteration of all positions of tree T.

The tree data structure also supports the following mutator methods in addition
to the mutator methods supported by the positional container ADT:
    T.add_root(elem): Place a node with the given element at the root of an empty tree.
    T.add_child(p, elem): Create a new child with the given element for node at Position p.
    T.insert(p, elem): Insert a new node at Position p. Attach the subtree rooted at the
                       existing node as a child of the new node.
"""

from .positional_container import PositionalContainer


class Tree(PositionalContainer):
    #---------------- nested Node class ----------------------#
    class _Node:
        """ Lightweight non-public class for storing a node.
        Overwrite the nested Node class.
        """
        __slots__ = "_elem", "_index", "_parent", "_children"
        def __init__(self, elem, idx, parent=None, children=None):
            """ Initialize a _Node instance.
            @param elem: Element stored at the node.
            @param idx (int): Integer used to uniquely identify a Node object.
            @param parent (Node): The parent of the node.
            @param children (List[Node]): A list of Nodes representing
                                              the children of the node.
            """
            self._elem = elem
            self._index = idx
            self._parent = parent
            self._children = children if children is not None else []

    #---------------- tree initializer ----------------#
    def __init__(self):
        """ Initialize an empty tree. """
        self._root = None
        self._size = 0
        self._curr_idx = 0

        self._depths = None
        self._heights = None

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
        """ Return the depth of the node at Position p. Return None if the depth is
        not computed.
        @param p (Position): Position representing the node in the tree.
        @return depth (int): The depth of the node from the root of the tree.
        """
        if self._depths is None:
            return None
        return self._depths[p.index()]

    def height(self, p):
        """ Return the height of the node at Position p. Return None if the height is
        not computed.
        @param p (Position): Position representing the node in the tree.
        @return height (int): The height of the node in the tree.
        """
        if self._heights is None:
            return None
        return self._heights[p.index()]

    def is_root(self, p):
        """ Return True if Position p represents the root of the tree. """
        return self.root() == p

    def is_leaf(self, p):
        """ Return True if Position p dos not have any children. """
        return self.num_children(p) == 0

    def positions(self):
        """ Generate an iteration of all positions of the tree.
        @yield p (Position): Position representing the node in the tree.
        """
        def expand(p):
            yield p
            for ch in self.children(p):
                for _c in expand(ch):
                    yield _c
        return expand(self.root())

    #---------------- public mutators ----------------#
    def add_root(self, elem):
        """ Place a node with the given element at the root of an empty tree.
        Raise ValueError if the tree is not empty.
        @param elem: Element to be stored at the node.
        @return root (Position): Return Position representing the root of the tree.
        """
        if self._root is not None:
            raise ValueError("Root exists")
        self._root = self._Node(elem, idx=0)
        self._size = 1
        self._curr_idx = 1
        self._depths, self._heights = None, None
        return self._make_position(self._root)

    def add_child(self, p, elem):
        """ Create a new child with the given element for node at Position p.
        @param p (Position): Position representing the node in the tree.
        @param elem: Element to be stored at the child.
        @return child (Position): Return Position representing the new child.
        """
        node = self._validate(p)
        child = self._Node(elem, idx=self._curr_idx, parent=node)
        self._curr_idx += 1
        node._children.append(child)
        self._size += 1

        # Invalidate depths and heights after modifying the tree.
        self._depths, self._heights = None, None

        return self._make_position(child)

    def insert(self, p, elem):
        """ Insert a new node at Position p. Attach the subtree rooted at the existing
        node as a child of the new node. Note that the depths of the nodes must be
        recomputed after executing the method _insert.
        @param p (Position): Position representing the node in the tree.
        @param elem: Element to be stored at the new node.
        @return new_p (Position): Return Position representing the new node.
        """
        node = self._validate(p)
        new_node = self._Node(elem, idx=self._curr_idx, parent=node._parent)
        self._curr_idx += 1
        node._parent = new_node
        new_node._children.append(node)
        self._size += 1

        # Invalidate depths and heights after modifying the tree.
        self._depths, self._heights = None, None

        return self._make_position(new_node)

    def reindex(self):
        """ Traverse the tree and assign a unique index to each node. Compute the depths
        and the heights of all nodes and store them in dictionaries.
        """
        super().reindex()
        self._depths, self._heights = None, None
        for p in self.positions():
            self._compute_depth(p)
            self._compute_height(p)

    #---- private methods - should not be invoked by the user ----#
    def _compute_depth(self, p):
        if self._depths is None:
            self._depths = {self.root().index() : 0}
        if p.index() not in self._depths:
            depth = 1 + self._compute_depth(self.parent(p))
            self._depths[p.index()] = depth
        return self._depths[p.index()]

    def _compute_height(self, p):
        if self._heights is None:
            self._heights = {}
        if p.index() not in self._heights:
            if self.is_leaf(p):
                height = 0
            else:
                height = 1 + max(self._compute_height(ch) for ch in self.children(p))
            self._heights[p.index()] = height
        return self._heights[p.index()]

#