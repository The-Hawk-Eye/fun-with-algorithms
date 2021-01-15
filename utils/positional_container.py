""" The PositionalContainer ADT is defined using the concept
of *position* as an abstraction for a node of a container.
The position object supports the methods:
    p.elem(): Return the element stored at the node at Position p.
    p.index(): Return the index of the node at Position p.

The PositionalContainer ADT supports the following accessor methods:
    C.positions(): Generate an iteration of all positions of the container C.
    C.is_empty(): Return True if the container does not contain C any nodes.
    iter(C): Generate an iteration of the elements at the nodes of the container C.
    len(C): Return the total number of nodes in the container C.

The PositionalContainer ADT also supports the following mutator method:
    C.replace(p, elem): Replace the element at the node at Position p with the new elem.
    C.reindex(): Traverse the container and assign a unique index to each node.
"""


class PositionalContainer:
    #---------------- nested Node class ----------------------#
    class _Node:
        """ Lightweight non-public class for storing a node. """
        __slots__ = "_elem", "_index"
        def __init__(self, elem, idx):
            """ Initialize a _Node instance.
            @param elem: Element stored at the node.
            @param idx (int): Integer used to uniquely identify a Node object.
            """
            self._elem = elem
            self._index = idx

    #----------------- nested Position class ------------------#
    class Position:
        def __init__(self, container, node):
            """ Initialize a Position. Constructor should not be invoked
            by the user.
            @param container (Container): Container object to which the node belongs.
            @param node (Node): Node object.
            """
            self._container = container     # this is used to validate positions by checking
                                            # whether they belong to the given Container structure
            self._node = node

        def elem(self):
            """ Return the elem of the node at this Position. """
            return self._node._elem

        def index(self):
            """ Return the index of the node at this Position. """
            return self._node._index

        def __eq__(self, other):
            """ Return True if other is a Position representing the same location.
            @param other (Position): Position representing a node in the container.
            @return equal (bool): Boolean True or False.
            """
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other):
            """ Return True if other Position does not represent the same location.
            @param other (Position): Position representing a node in the container.
            @return equal (bool): Boolean True or False.
            """
            return not (self == other)

    #------------- container initializer --------------#
    def __init__(self):
        """ Initialize an empty container. """
        raise NotImplementedError("This method must be implemented by the subclass")

    #---------------- public accessors ----------------#
    def positions(self):
        """ Generate an iteration of all positions of the tree."""
        raise NotImplementedError("This method must be implemented by the subclass")

    def is_empty(self):
        """ Return True if the container is empty. """
        return len(self) == 0

    def __iter__(self):
        """ Generate an iteration of all the elements at the nodes of the container. """
        for p in self.positions():
            yield p.elem()

    def __len__(self):
        """ Return the total number of nodes in the container. """
        return self._size

    #---------------- public mutators -----------------#
    def replace(self, p, elem):
        """ Replace the element at the node at Position p with the new elem.
        @param p (Position): Position representing the node in the container.
        @param elem: Element to be stored at the node.
        @return old: Return the old element stored at the node.
        """
        node = self._validate(p)
        old = node._elem
        node._elem = elem
        return old

    def reindex(self):
        """ Traverse the container and assign a unique index to each node. """
        curr_idx = 0
        for p in self.positions():
            p._node._index = curr_idx
            curr_idx += 1
        return curr_idx

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
        return p._node

#