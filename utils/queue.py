""" A queue is a collection of objects that are inserted and removed
according to the first-in, first-out (FIFO) principle.
The queue data structure supports the following accessor methods:
    Q.front(): Return the element at the front of the queue Q.
    Q.is_empty(): Return True if the queue Q is empty.
    len(Q): Return the total number of elements in the queue Q.

The queue data structure supports the following mutator methods:
    Q.enqueue(elem): Add an element to the back of the queue Q.
    Q.dequeue(): Remove and return the first element from the queue Q.
"""

from .linked_list import DoublyLinkedList


class Queue:
    #--------------- queue initializer ----------------#
    def __init__(self):
        """ Initialize an empty queue. """
        self._container = DoublyLinkedList()

    #---------------- public accessors ----------------#
    def first(self):
        """ Return the element at the front of the queue. """
        return self._container.first().elem()

    def is_empty(self):
        """ Return True if the queue is empty. """
        return self._container.is_empty()

    def __len__(self):
        """ Return the total number of elements in the queue. """
        return len(self._container)

    #---------------- public mutators ----------------#
    def enqueue(self, elem):
        """ Add an element to the back of the queue. """
        self._container.add_last(elem)

    def dequeue(self):
        """ Remove and return the first element from the queue. """
        return self._container.delete(self._container.first())

#