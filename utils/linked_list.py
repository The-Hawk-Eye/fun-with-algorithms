""" The doubly linked list data structure is defined using the concept of *position*
as an abstraction for a node of a list.
The doubly linked list data structure supports the following accessor methods in
addition to the accessor methods supported by the positional container ADT:
    L.first(): Return the Position of the first element of the list.
    L.last(): Return the Position of the last element of the list
    L.before(p): Return the Position just before Position p.
    L.after(p): Return the Position just after Position p.
    L.positions(): Generate a forward iteration of the Positions of the list L.

The doubly linked list data structure supports the following mutator methods in
addition to the mutator methods supported by the positional container ADT:
    L.add_before(p, elem): Add a node storing elem just before Position p.
    L.add_after(p, elem): Add a node storing elem just after Position p.
    L.add_first(elem): Add a node storing elem as the first element of the list.
    L.add_last(elem): Add a node storing elem as the last element of the list.
    L.delete(p): Remove and return the element at Position p.
"""

from .positional_container import PositionalContainer


class DoublyLinkedList(PositionalContainer):
    #--------------- nested Node class ----------------#
    class _Node:
        """ Lightweight non-public class for storing a node. """
        __slots__ = "_elem", "_index", "_prev", "_next"
        def __init__(self, elem, idx, prev=None, next=None):
            """ Initialize a _Node instance.
            @param elem: Element stored in the node.
            @param idx (int): Integer used to uniquely identify a Node object.
            @param next (Node): A reference to the next node in the list.
            @param prev (Node): A reference to the previous node in the list.
            """
            self._elem = elem
            self._index = idx
            self._prev = prev
            self._next = next

    #---------------- list initializer ----------------#
    def __init__(self):
        """ Initialize an empty linked list. """
        self._header = self._Node(None, None, None, None)     # sentinel header node
        self._trailer = self._Node(None, None, None, None)    # sentinel trailer node

        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._size = 0
        self._curr_idx = 0

    #---------------- public accessors ----------------#
    def first(self):
        """ Return the Position of the first element of the list or None if the list is empty. """
        return self._make_position(self._header._next)

    def last(self):
        """ Return the Position of the last element of the list or None if the list is empty. """
        return self._make_position(self._trailer._prev)

    def before(self, p):
        """ Return the Position just before Position p. Return None if p is the first element.
        @param p (Position): Position representing the node in the linked list.
        @return prev (Position): Position representing the previous node in the linked list.
        """
        node = self._validate(p)
        return self._make_position(node._prev)

    def after(self, p):
        """ Return the Position just after Position p. Return None if p is the last element.
        @param p (Position): Position representing the node in the linked list.
        @return next (Position): Position representing the next node in the linked list.
        """
        node = self._validate(p)
        return self._make_position(node._next)

    def positions(self, reverse=False):
        """ Generate a forward iteration of the Positions of the List.
        If reverse is True, generate a backward iteration starting from last.
        @param reverse (bool): If True generate a backward iteration. Default is False.
        @yield cursor (Position): Position representing the node in the list.
        """
        cursor = self.first() if not reverse else self.last()
        while cursor.elem() is not None:
            yield cursor
            cursor = self.after(cursor) if not reverse else self.before(cursor)

    #---------------- public mutators ----------------#
    def add_before(self, elem, p):
        """ Add a node storing elem just before Position p.
        @param elem: Element to be stored in the node.
        @param p (Position): Position representing the node in the linked list.
        @return new_node (Position): Return Position representing the new node.
        """
        node = self._validate(p)
        new_node = self._Node(elem, idx=self._curr_idx, prev=node._prev, next=node)
        self._curr_idx += 1
        node._prev._next = new_node
        node._prev = new_node
        self._size += 1
        return self._make_position(new_node)

    def add_after(self, elem, p):
        """ Add a node storing elem just after Position p.
        @param elem: Element to be stored at the node.
        @param p (Position): Position representing the node in the linked list.
        @return new_node (Position): Return Position representing the new node.
        """
        node = self._validate(p)
        new_node = self._Node(elem, idx=self._curr_idx, prev=node, next=node._next)
        self._curr_idx += 1
        node._next._prev = new_node
        node._next = new_node
        self._size += 1
        return self._make_position(new_node)

    def add_first(self, elem):
        """ Add a node with storing elem as the first element of the list. """
        return self.add_before(elem, self.first())

    def add_last(self, elem):
        """ Add a node with storing elem as the last element of the list. """
        return self.add_after(elem, self.last())

    def delete(self, p):
        """ Remove and return the element at Position p.
        @param p (Position): Position representing the node in the linked list.
        @return elem: Element stored at the node.
        """
        node = self._validate(p)
        node._prev._next = node._next
        node._next._prev = node._prev
        self._size -= 1
        return node._elem

#