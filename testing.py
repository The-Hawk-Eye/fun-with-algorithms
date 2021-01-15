import time
import random
random.seed(0)
from collections import deque

import Least_Common_Ancestor.rmq as rmq
import Least_Common_Ancestor.lca as lca
import Level_Ancestor.la as la
from utils.tree import Tree
from utils.binary_tree import BinaryTree
from utils.linked_list import DoublyLinkedList
from utils.queue import Queue
from utils.traversal_algorithms import breadth_first_traversal


def generate_random_array(size):
    arr = [None] * size
    for i in range(size):
        arr[i] = random.randint(0, MAX_VAL)

    return arr


def generate_random_tree(size):
    T = Tree()
    T.add_root(random.randint(0, MAX_VAL))
    frontier = deque()
    frontier.append(T.root())

    while len(T) < size:
        p = frontier.popleft()
        num_children = random.randint(1, min(4, size - len(T)))
        for _ in range(num_children):
            T.add_child(p, random.randint(0, MAX_VAL))
        frontier.extend(T.children(p))

    return T


class random_position_generator:
    def __init__(self, T):
        self.tree_height = T.height(T.root())
        self.candidates = [[] for i in range(self.tree_height + 1)]
        for p in T.positions():
            self.candidates[T.height(p)].append(p)

    def generate_random_position(self):
        if random.random() > 0.5:
            node_height = random.randint(0, self.tree_height)
        else:
            node_height = 0
        return random.choice(self.candidates[node_height])



def print_tree(T):
    print("size of Tree: {}".format(len(T)))
    frontier = deque()
    frontier.append(T.root())

    print("root: ", end="")
    while len(frontier) > 0:
        p = frontier.popleft()

        if isinstance(p, T.Position):
            print(p.elem())
            frontier.append("{} has {} children:".format(p.elem(), T.num_children(p)))
            frontier.extend(T.children(p))
        else:
            print(p)



def check_rmq_correctness(RMQ):
    sizes = [10, 100, 1000, 10000]
    trials = 200

    for size in sizes:
        arr = generate_random_array(size)
        rmq_index = RMQ(arr)

        for trial in range(trials):
            start_idx = random.randint(0, size-1)
            end_idx = random.randint(start_idx, size-1)

            min_idx = rmq_index(start_idx, end_idx)
            _min_idx = start_idx + arr[start_idx:end_idx+1].index(min(arr[start_idx:end_idx+1]))

            if min_idx != _min_idx:
                raise Exception("{} not correctly implemented".format(RMQ.__name__))

    print("{} implemented correctly!".format(RMQ.__name__))



def check_rmq_complexity(RMQ):
    if RMQ.__name__ == "RMQ_table":
        sizes = [2000, 4000, 8000]#, 16000] # x2
    else:
        sizes = [1000, 8000, 64000]#, 512000, 4096000] # x8

    print("\n{}".format(RMQ.__name__))
    print("{:10}   {:10}".format("size", "time"))
    for size in sizes:
        arr = generate_random_array(size)

        tic = time.time()
        rmq_index = RMQ(arr)
        toc = time.time()
        print("{:<10}   {:<10.6}".format(size, toc-tic))



def check_lca_correctness(LCA):
    sizes = [10, 100, 1000, 10000]
    trials = 200

    for size in sizes:
        T = generate_random_tree(size)
        lca_index = LCA(T)
        R = random_position_generator(T)


        for trial in range(trials):
            u = R.generate_random_position()
            v = R.generate_random_position()
            ancestor = lca_index(u, v)


            p_u = u
            p_v = v
            while p_u != p_v:
                if (T.depth(p_u) < T.depth(p_v)):
                    p_v = T.parent(p_v)
                elif (T.depth(p_v) < T.depth(p_u)):
                    p_u = T.parent(p_u)
                else:
                    p_v = T.parent(p_v)
                    p_u = T.parent(p_u)

            if ancestor != p_u:
                raise Exception("{} not correctly implemented".format(LCA.__name__))

    print("{} implemented correctly!".format(LCA.__name__))


def check_lca_complexity(LCA):
    sizes = [1000, 8000, 64000]#, 512000, 4096000] # x8

    print("\n{}".format(LCA.__name__))
    print("{:10}   {:10}".format("size", "time"))
    for size in sizes:
        T = generate_random_tree(size)

        tic = time.time()
        lca_index = LCA(T)
        toc = time.time()
        print("{:<10}   {:<10.6}".format(size, toc-tic))



def check_la_correctness(LA):
    sizes = [10, 100, 1000, 10000]
    trials = 200

    for size in sizes:
        T = generate_random_tree(size)
        la_index = LA(T)
        R = random_position_generator(T)

        for trial in range(trials):
            v = R.generate_random_position()
            k = random.randint(0, size - 1)
            ancestor = la_index(v, k)

            p = v
            for i in range(k):
                if p is not None:
                    p = T.parent(p)
                else:
                    break

            if ancestor != p:
                raise Exception("{} not correctly implemented".format(LA.__name__))

    print("{} implemented correctly!".format(LA.__name__))


def check_la_complexity(LA):
    if LA.__name__ == "LA_table":
        sizes = [2000, 4000, 8000]#, 16000] # x2
    else:
        sizes = [1000, 8000, 64000]#, 512000, 4096000] # x8

    print("\n{}".format(LA.__name__))
    print("{:10}   {:10}".format("size", "time"))
    for size in sizes:
        T = generate_random_tree(size)

        tic = time.time()
        la_index = LA(T)
        toc = time.time()
        print("{:<10}   {:<10.6}".format(size, toc-tic))



if __name__ == "__main__":
    MAX_VAL = 1000000


    rmq_solutions = [rmq.RMQ_table, rmq.RMQ_sparse, rmq.RMQ_Fischer_Heun, rmq.RMQ_Index]
    for rmq_strategy in rmq_solutions:
        check_rmq_correctness(rmq_strategy)

    for rmq_strategy in rmq_solutions:
        check_rmq_complexity(rmq_strategy)


    print()
    check_lca_correctness(lca.LCA_Index)
    check_lca_complexity(lca.LCA_Index)


    print()
    la_solutions = [la.LA_macro_micro, la.LA_table, la.LA_sparse, la.LA_macro_micro]
    for la_strategy in la_solutions:
        check_la_correctness(la_strategy)

    for la_strategy in la_solutions:
        check_la_complexity(la_strategy)

