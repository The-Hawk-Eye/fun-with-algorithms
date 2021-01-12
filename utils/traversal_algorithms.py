from .binary_tree import BinaryTree
from .stack import Stack
from .queue import Queue


def breadth_first_traversal(tree):
    """ Breath-first traversal of a tree object.
    @param tree (Tree): A Tree object.
    @yield node (Position): Position representing a node in the tree.
    """
    if tree.is_empty():
        return None

    frontier = Queue()
    frontier.enqueue(tree.root())
    while not frontier.is_empty():
        node = frontier.dequeue()
        yield node

        for child in tree.children(node):
            frontier.enqueue(child)


def depth_first_traversal(tree):
    """ Depth-first traversal of a tree object.
    @param tree (Tree): A Tree object.
    @yield node (Position): Position representing a node in the tree.
    """
    if tree.is_empty():
        return None

    def dfs(node):
        """ Recursive procedure for visiting the nodes of a tree object. """
        # Yield the node.
        yield node

        # Recursively call the procedure for every child.
        for child in tree.children(node):
            for node in dfs(child):
                yield node

    for node in dfs(tree.root()):
        yield node


def build_cartesian_tree(arr):
    """ Build a Cartesian Tree for the given array. Each node of the tree
    stores the index of the element in the array.
    Build an auxiliary array mapping array index to the position in the tree
    storing that element.
    @param arr (List[int]): A list of integers.
    @return T (Tree): A Tree object. Cartesian tree for the given array.
    @return pos_index (List[Position]): A list of Positions. pos[i] stores the position
                                        of the node with element the index i.
    """
    T = BinaryTree()

    # Maintaining a stack of the nodes in the right spine.
    S = Stack()
    last_pop = None

    # Iterate through the array and insert the new nodes. Store the position of the Node.
    pos_index = [None] * len(arr)
    for i in range(len(arr)):
        while (not S.is_empty()) and (arr[S.top().elem()] > arr[i]):
            last_pop = S.pop()
        if T.is_empty():
            p = T.add_root(i)
        elif last_pop is None:
            p = T.add_right(S.top(), i)
        else:
            p = T.insert(last_pop, i, left=True)

        pos_index[i] = p
        S.push(p)
        last_pop = None

    # Recompute the indices, depths, and heights of the nodes after building the tree.
    T.reindex()

    return T, pos_index

#