from collections import deque

def breadth_first_traversal(tree):
	""" Breath-first traversal of a tree object.
	@param tree (Tree): A Tree object.
	@yield node (Position): Position representing a node in the tree.
	"""
	if tree.is_empty():
		return None

	frontier = deque()
	frontier.append(tree.root())
	while len(frontier) > 0:	# frontier not empty
		node = frontier.popleft()
		yield node
		frontier.extend(tree.children(node))


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
