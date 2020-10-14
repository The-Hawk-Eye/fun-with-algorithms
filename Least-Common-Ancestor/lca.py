import sys
sys.path.append("..")

from utils.tree import Tree
from rmq import RMQ_table, RMQ_sparse, RMQ_1


class LCA_index:
	def __init__(self, tree, RMQ_strategy):
		""" Constructs an LCA index for the tree object.
		@param tree (Tree): A tree object.
		"""
		self._tree = tree
		self._visits = []
		self._levels = []
		self._start = [0] * len(tree)

		self._time = 0
		self._reduce(tree.root())
		self._rmq = RMQ_strategy(self._levels)

	def _reduce(self, p):
		""" Reduce the LCA problem to RMQ problem using recursive depth-first traversal.
		This function recursively builds the arrays needed for the RMQ problem. It should
		not be invoked by the user.
		@param p (Position): Position representing the node in the tree.
		"""
		self._visits.append(p)
		self._levels.append(self._tree.depth(p))
		self._start[p.index()] = self._time

		for q in self._tree.children(p):
			self._time += 1
			self._reduce(q)
			self._visits.append(p)
			self._levels.append(self._tree.depth(p))

		self._time += 1

	def __call__(self, p, q):
		""" Given the positions of two nodes in the tree, finds the
		least common ancestor of the two nodes.
		@param p (Position): Position representing a node in the tree.
		@param q (Position): Position representing a node in the tree.
		@return w (Position): Position of the least common ancestor of nodes
							  at positions p and q.
		"""
		idx = self._rmq(self._start[p.index()], self._start[q.index()])
		return self._visits[idx]




if __name__ == "__main__":
	T = Tree()

	_r = T._add_root(33)
	_c = T._add_child(_r, 84)
	_d = T._add_child(_r, 58)
	_e = T._add_child(_c, 93)
	_f = T._add_child(_d, 62)
	_g = T._add_child(_f, 64)
	_h = T._add_child(_f, 63)
	_i = T._add_child(_h, 83)

	lca = LCA_index(T, RMQ_sparse)
	print("visits:")
	for elem in lca._visits:
		print(elem.value(), end=" ")
	print("\nlevels:\n", lca._levels)
	print("start:\n", lca._start)

	for idx in lca._start:
		print(idx, lca._visits[idx].value())

	pos = lca(_c, _h)
	print("LCA(84, 63) = ", pos.value())

	pos = lca(_g, _i)
	print("LCA(64, 83) = ", pos.value())

	pos = lca(_d, _e)
	print("LCA(58, 93) = ", pos.value())

	pos = lca(_r, _i)
	print("LCA(33, 83) = ", pos.value())


	print("RMQ +/- 1")
	lca_2 = LCA_index(T, RMQ_1)
	pos = lca_2(_c, _h)
	print("LCA(84, 63) = ", pos.value())

	pos = lca_2(_g, _i)
	print("LCA(64, 83) = ", pos.value())

	pos = lca_2(_d, _e)
	print("LCA(58, 93) = ", pos.value())

	pos = lca_2(_r, _i)
	print("LCA(33, 83) = ", pos.value())


	my_arr = [31, 41, 59, 26, 53, 58, 97, 93]
	rmq_tab = RMQ_table(my_arr)
	for i in range(len(my_arr)):
		j = 0
		while j < i:
			print("  ", end=" ")
			j += 1
		while j < len(my_arr):
			print(my_arr[rmq_tab._table[i][j]], end=" ")
			j += 1
		print()

	rmq_sp = RMQ_sparse(my_arr)
	for i in range(len(my_arr)):
		for j in range(rmq_sp._loglength):
			try:
				print(my_arr[rmq_sp._table[i][j]], end=" ")
			except:
				print("  ", end=" ")
		print()


	for i in range(len(lca._levels)):
		for j in range(lca._rmq._loglength):
			try:
				print(lca._levels[lca._rmq._table[i][j]], end=" ")
			except:
				print("  ", end=" ")
		print()

