""" A stack is a collection of objects that are inserted and removed
according to the last-in, first-out (LIFO) principle.
The stack data structure supports the following accessor methods:
    S.top(): Return the element at the top of the stack S.
    S.is_empty(): Return True if the stack S is empty.
    len(S): Return the total number of elements in the stack S.

The stack data structure supports the following mutator methods:
    S.push(elem): Add an element to the top of the stack S.
    S.pop(): Remove and return the top element from the stack S.
"""

from .linked_list import DoublyLinkedList


class Stack:
    #--------------- stack initializer ----------------#
    def __init__(self):
        """ Initialize an empty stack. """
        self._container = DoublyLinkedList()

    #---------------- public accessors ----------------#
    def top(self):
        """ Return the element at the top of the stack. """
        return self._container.last().elem()

    def is_empty(self):
        """ Return True if the stack is empty. """
        return self._container.is_empty()

    def __len__(self):
        """ Return the total number of elements in the stack. """
        return len(self._container)

    #---------------- public mutators ----------------#
    def push(self, elem):
        """ Add an element to the top of the stack. """
        self._container.add_last(elem)

    def pop(self):
        """ Remove and return the top element from the stack. """
        return self._container.delete(self._container.last())

#