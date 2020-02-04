#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <list>
#include <unordered_set>
#include <unordered_map>
#include <chrono>

#include "Tree.hpp"

typedef std::unordered_map<treeNode, std::vector<treeNode> > table;
typedef struct naiveStruct {
	std::unordered_map<treeNode, std::vector<treeNode> > naiveTable;
	std::unordered_map<treeNode, int> depths;
} naiveStruct;
naiveStruct BuildNaiveIndex(const tree&);
treeNode NaiveSearch(treeNode, int, const naiveStruct &);


typedef struct pathDecompStruct {
	std::unordered_map<treeNode, int> pathIndex;	// gives the index of the path the node belongs to
	std::unordered_map<treeNode, int> nodeIndex;	// gives the index of the node inside the path it belongs to
	std::vector<std::vector<treeNode> > paths;
	std::unordered_map<treeNode, treeNode> parents;
} pathDecompStruct;
pathDecompStruct BuildPathDecompIndex(const tree &);
treeNode PathDecompSearch(treeNode, int, const pathDecompStruct &);



typedef struct stairDecompStruct {
	std::unordered_map<treeNode, int> pathIndex;	// gives the index of the path the node belongs to
	std::unordered_map<treeNode, int> nodeIndex;	// gives the index of the node inside the stair it belongs to
	std::vector<std::vector<treeNode> > stairs;
	std::unordered_map<treeNode, treeNode> parents;
} stairDecompStruct;
stairDecompStruct BuildStairDecompIndex(const tree &);
treeNode StairDecompSearch(treeNode, int, const stairDecompStruct &);


typedef struct stairStruct {
	std::unordered_map<treeNode, int> pathIndex;	// gives the index of the path the node belongs to
	std::unordered_map<treeNode, int> nodeIndex;	// gives the index of the node inside the stair it belongs to
	std::vector<std::vector<treeNode> > stairs;
	std::unordered_map<treeNode, treeNode> parents;
	std::unordered_map<treeNode, int> depths;
	std::unordered_map<treeNode, std::vector<treeNode> > jump;

	std::vector<int> power;	// pow[k] = 2^k
	std::vector<int> deg;	// deg[d] = k -> 2^k <= d < 2^(k+1)
} stairStruct;
stairStruct BuildStairIndex(const tree &);
treeNode StairSearch(treeNode, int, const stairStruct &);
treeNode StairSearchLeaf(treeNode, int, const stairStruct &);



int main()
{
	// loads the data from 'file_path' into the tree;
	const char * file_path = "Root_Tree_rev002.txt";
	treeNode node, parent;
	std::ifstream myFile(file_path);
	std::vector<treeNode> nodes;
	std::unordered_map<treeNode, treeNode> parents;
	while (myFile >> node >> parent) {
		nodes.push_back(node);
		parents[node] = parent;
	}

	tree T(nodes, parents);
	T.print();

	node = 23;
	int ancestorLevel = 5;

	using namespace std::chrono;
	auto beginBuild = high_resolution_clock::now();
	naiveStruct naiveIndex = BuildNaiveIndex(T);
	auto endBuild = high_resolution_clock::now();
	auto timeToBuild = duration_cast<milliseconds>(endBuild - beginBuild);//.count();
	std::cout << "Time to build Naive Index: " << timeToBuild.count() << std::endl;

	auto beginSearch = high_resolution_clock::now();
	parent = NaiveSearch(node, ancestorLevel, naiveIndex);
	auto endSearch = high_resolution_clock::now();
	auto timeToSearch = duration_cast<milliseconds>(endSearch - beginSearch);//.count();
	std::cout << "Time to search in Naive Index: " << timeToSearch.count() << std::endl;
	std::cout << "The parent of level " << ancestorLevel << " of node " << node << " is: " << parent << std::endl;



	beginBuild = high_resolution_clock::now();
	pathDecompStruct pathDecompIndex = BuildPathDecompIndex(T);
	endBuild = high_resolution_clock::now();
	timeToBuild = duration_cast<milliseconds>(endBuild - beginBuild);//.count();
	std::cout << "Time to build path decomposition index: " << timeToBuild.count() << std::endl;

	beginSearch = high_resolution_clock::now();
	parent = PathDecompSearch(node, ancestorLevel, pathDecompIndex);
	endSearch = high_resolution_clock::now();
	timeToSearch = duration_cast<milliseconds>(endSearch - beginSearch);//.count();
	std::cout << "Time to search in path decomposition index: " << timeToSearch.count() << std::endl;
	std::cout << "The parent of level " << ancestorLevel << " of node " << node << " is: " << parent << std::endl;





	beginBuild = high_resolution_clock::now();
	stairDecompStruct stairDecompIndex = BuildStairDecompIndex(T);
	endBuild = high_resolution_clock::now();
	timeToBuild = duration_cast<milliseconds>(endBuild - beginBuild);//.count();
	std::cout << "Time to build stair decomposition index: " << timeToBuild.count() << std::endl;

	beginSearch = high_resolution_clock::now();
	parent = StairDecompSearch(node, ancestorLevel, stairDecompIndex);
	endSearch = high_resolution_clock::now();
	timeToSearch = duration_cast<milliseconds>(endSearch - beginSearch);//.count();
	std::cout << "Time to search in stair decomposition index: " << timeToSearch.count() << std::endl;
	std::cout << "The parent of level " << ancestorLevel << " of node " << node << " is: " << parent << std::endl;





	beginBuild = high_resolution_clock::now();
	stairStruct stairIndex = BuildStairIndex(T);
	endBuild = high_resolution_clock::now();
	timeToBuild = duration_cast<milliseconds>(endBuild - beginBuild);//.count();
	std::cout << "Time to build stair index: " << timeToBuild.count() << std::endl;

	beginSearch = high_resolution_clock::now();
	parent = StairSearch(node, ancestorLevel, stairIndex);
	endSearch = high_resolution_clock::now();
	timeToSearch = duration_cast<milliseconds>(endSearch - beginSearch);//.count();
	std::cout << "Time to search in stair index: " << timeToSearch.count() << std::endl;
	std::cout << "The parent of level " << ancestorLevel << " of node " << node << " is: " << parent << std::endl;



	return 0;
}










/*
 Naive indexing:
 	Building a table storing all level ancestors for every node.
 	In the worst case the table requires O(N^2) time to build and O(N^2) memory to maintain.
 Naive search:
 	Searching is done by a simple table look-up.
 	Search is done in O(1) time.
*/
naiveStruct BuildNaiveIndex(const tree& T) {
	naiveStruct naiveIndex;
	std::vector<treeNode> nodes = T.GetNodes();
	std::unordered_map<treeNode, treeNode> parents = T.GetParents();
	std::unordered_map<treeNode, int> depths = T.GetDepths();
	for (treeNode node: nodes) {
		naiveIndex.depths[node] = depths[node];
		treeNode parent = node;
		while (parent != -1) {
			naiveIndex.naiveTable[node].push_back(parent);
			parent = parents[parent];
		}
	}
	return naiveIndex;
}

treeNode NaiveSearch(treeNode node, int ancestorLevel, const naiveStruct& naiveIndex) {
	auto findDepth = naiveIndex.depths.find(node);
	int maxAncestorLevel = findDepth->second;
	if (ancestorLevel > maxAncestorLevel) {
		return -1;
	}

	auto findParents = naiveIndex.naiveTable.find(node);
	treeNode ancestor = (findParents->second)[ancestorLevel];
	return ancestor;
}










/*
 Path decomposition index:
 	The tree is decomposed into paths. (array of arrays)
 	Path decomposition is done using greedy by length. (sorting the leafs by depth)
 	Every node belongs to only one path. Every path is an array of elements equal to its length.
 	For every node we store the number of the path it belongs to. (path[node] = i <-> node belongs to path_i)
 	For every node we store the index at which it is stored. (index[node] = k <-> path_i[k] = node)
 	The elements are stored in reversed order (path_i[index[node] - 1] = p(node), path_i[index[node] - 2] = p(p(node))).
 	The index requires O(N) time to build and O(N) memory to store.
 Path decomposition search:
 	Search is done by jumping up from path to path.
 	We find the path the node belongs to and the index at which the node is stored.
 	If the ancestorLevel is smaller than index[node] at which the node is stored
 	then the ancestor belongs to the same path and we can find it by accesing path_i[index[node] - ancestorLevel].
	If the ancestorLevel is greater than index[node] at which the node is stored
	then we access the end of the current path by path_i[0] and take the parent of the node that is at the end.
	The new node lies on a new path and is the (ancestorLevel - index[node] -1) child of the ancestor we search.
 	After that we recursevely call the search function for the new node and the new ancestor level.
 	In the worst case search takes O(sqrt(N)) time.
*/
pathDecompStruct BuildPathDecompIndex(const tree& T) {
	pathDecompStruct pathDecompIndex;

	std::vector<treeNode> nodes = T.GetNodes();
	std::unordered_map<treeNode, treeNode> parents = T.GetParents();
	std::unordered_map<treeNode, int> depths = T.GetDepths();
	std::unordered_map<treeNode, int> heights = T.GetHeights();
	treeNode root = T.GetRoot();
	int treeHeight = T.GetTreeHeight();
	int numNodes = T.GetNumNodes();

	pathDecompIndex.parents = parents;

	/* sorting leafs in linear time */
	std::vector<std::list<treeNode> > leafs(treeHeight + 1);
	for (treeNode node: nodes) {
		if (heights[node] == 0) {
			int depth = depths[node];
			leafs[depth].push_back(node);
		}
	}

	std::list<treeNode> sortedLeafs;
	for (int index = 0; index <= treeHeight; index++) {
		while (!leafs[index].empty()) {
			sortedLeafs.push_front(leafs[index].front());
			leafs[index].pop_front();
		}
	}
	// end

	/* building array of paths. each path is an array */
	int numPaths = sortedLeafs.size();
	pathDecompIndex.paths.resize(numPaths);
	std::vector<treeNode> mark(numNodes, 0);	// initialize all nodes to 'non-marked'
	int currentPathIndex = 0;
	int currentNodeIndex = 0;
	for (treeNode leaf: sortedLeafs) {
		/* creating the max path for 'leaf' */
		std::vector<treeNode> currentPath;
		treeNode currentNode = leaf;
		do {
			mark[currentNode] = 1;
			currentPath.push_back(currentNode);
			pathDecompIndex.pathIndex[currentNode] = currentPathIndex;
			currentNode = parents[currentNode];
		} while ((currentNode != -1) && mark[currentNode] == 0);

		/* reversing the array */
		currentNodeIndex = 0;
		for (auto iterator = currentPath.rbegin(); iterator != currentPath.rend(); iterator++) {
			treeNode node = *iterator;
			pathDecompIndex.paths[currentPathIndex].push_back(node);
			pathDecompIndex.nodeIndex[node] = currentNodeIndex;
			currentNodeIndex++;
		}
		currentPathIndex++;
	}
	// end

	return pathDecompIndex;
}

treeNode PathDecompSearch(treeNode node, int ancestorLevel, const pathDecompStruct& pathDecompIndex) {
	auto findNodeIndex = pathDecompIndex.nodeIndex.find(node);
	int nodeIndex = findNodeIndex->second;

	auto findPathIndex = pathDecompIndex.pathIndex.find(node);
	int pathIndex = findPathIndex->second;

	if (nodeIndex > ancestorLevel) {	// ancestor resides in the same path as the node
		return pathDecompIndex.paths[pathIndex][nodeIndex - ancestorLevel];
	}

	treeNode newNode = pathDecompIndex.paths[pathIndex][0];
	auto findParent = pathDecompIndex.parents.find(newNode);
	newNode = findParent->second;
	int newAncestorLevel = ancestorLevel - nodeIndex - 1;
	return PathDecompSearch(newNode, newAncestorLevel, pathDecompIndex);
}









/*
 Stairs Decomposition Index:
 	The tree is decomposed into paths. (array of arrays)
 	Path decomposition is done using greedy by length. (sorting the leafs by depth)
 	Every node belongs to only one path.
 	For every node we store the number of the path it belongs to. (path[node] = i <-> node belongs to path_i)
 	After that every path is doubled creating a stair.
 	For every node we store the index at which it is stored in the stair created by doubling its path. (index[node] = k <-> stair_i[k] = node)
 	The elements are stored in reversed order (stair_i[index[node] - 1] = p(node), stair_i[index[node] - 2] = p(p(node))).
 	The index requires O(N) time to build and O(N) memory to store.
 Stair decomposition search:
 	Search is done by jumping up from stair to stair.
 	We find the path the node belongs to and the index at which the node is stored.
 	If the ancestorLevel is smaller than index[node] at which the node is stored
 	then the ancestor belongs to the same stair and we can find it by accesing stair_i[index[node] - ancestorLevel].
	If the ancestorLevel is greater than index[node] at which the node is stored
	then we access the end of the current stair by stair_i[0] and take the parent of the node that is at the end.
	The new node lies on a new stair and is the (ancestorLevel - index[node] -1) child of the ancestor we search.
 	After that we recursevely call the search function for the new node and the new ancestor level.
 	In the worst case search takes O(logN) time.
*/
stairDecompStruct BuildStairDecompIndex(const tree& T) {
	stairDecompStruct stairDecompIndex;

	std::vector<treeNode> nodes = T.GetNodes();
	std::unordered_map<treeNode, treeNode> parents = T.GetParents();
	std::unordered_map<treeNode, int> depths = T.GetDepths();
	std::unordered_map<treeNode, int> heights = T.GetHeights();
	treeNode root = T.GetRoot();
	int treeHeight = T.GetTreeHeight();
	int numNodes = T.GetNumNodes();

	stairDecompIndex.parents = parents;

	/* sorting leafs in linear time */
	std::vector<std::list<treeNode> > leafs(treeHeight + 1);
	for (treeNode node: nodes) {
		if (heights[node] == 0) {
			int depth = depths[node];
			leafs[depth].push_back(node);
		}
	}

	std::list<treeNode> sortedLeafs;
	for (int index = 0; index <= treeHeight; index++) {
		while (!leafs[index].empty()) {
			sortedLeafs.push_front(leafs[index].front());
			leafs[index].pop_front();
		}
	}
	// end

	/* building array of stairs. each stair is an array */
	int numStairs = sortedLeafs.size();
	stairDecompIndex.stairs.resize(numStairs);
	std::vector<treeNode> mark(numNodes, 0);	// initialize all nodes to 'non-marked'
	int currentPathIndex = 0;
	int currentNodeIndex = 0;
	for (treeNode leaf: sortedLeafs) {
		/* creating the max path for 'leaf' */
		std::vector<treeNode> currentPath;
		treeNode currentNode = leaf;
		do {
			mark[currentNode] = 1;
			currentPath.push_back(currentNode);
			stairDecompIndex.pathIndex[currentNode] = currentPathIndex;
			currentNode = parents[currentNode];
		} while ((currentNode != -1) && mark[currentNode] == 0);

		/* doubling the path */
		int pathLength = currentPath.size();
		int i = 1;
		while ((currentNode != -1) && (i <= pathLength)) {
			currentPath.push_back(currentNode);
			currentNode = parents[currentNode];
			i++;
		}
		int stairLength = currentPath.size();

		/* reversing the array */
		currentNodeIndex = 0;
		for (i = stairLength - 1; i >=0 ; i--) {
			treeNode node = currentPath[i];
			stairDecompIndex.stairs[currentPathIndex].push_back(node);
			if (i < pathLength) {
				stairDecompIndex.nodeIndex[node] = currentNodeIndex + (stairLength - pathLength);	// the node index is ofset by (stairLength - pathLength)
				currentNodeIndex++;				
			}
		}
		currentPathIndex++;
	}
	// end

	return stairDecompIndex;
}

treeNode StairDecompSearch(treeNode node, int ancestorLevel, const stairDecompStruct& stairDecompIndex) {
	auto findNodeIndex = stairDecompIndex.nodeIndex.find(node);
	int nodeIndex = findNodeIndex->second;

	auto findPathIndex = stairDecompIndex.pathIndex.find(node);
	int pathIndex = findPathIndex->second;

	if (nodeIndex > ancestorLevel) {	// ancestor resides in the same path as the node
		return stairDecompIndex.stairs[pathIndex][nodeIndex - ancestorLevel];
	}

	treeNode newNode = stairDecompIndex.stairs[pathIndex][0];
	auto findParent = stairDecompIndex.parents.find(newNode);
	newNode = findParent->second;
	int newAncestorLevel = ancestorLevel - nodeIndex - 1;
	return StairDecompSearch(newNode, newAncestorLevel, stairDecompIndex);
}









/*
 StairIndex:
 	The tree is decomposed into paths. (array of arrays)
 	Path decomposition is done using greedy by length. (sorting the leafs by depth)
 	Every node belongs to only one path.
 	For every node we store the number of the path it belongs to. (path[node] = i <-> node belongs to path_i)
 	After that every path is doubled creating a stair.
 	For every node we store the index at which it is stored in the stair created by doubling its path. (index[node] = k <-> stair_i[k] = node)
 	The elements are stored in reversed order (stair_i[index[node] - 1] = p(node), stair_i[index[node] - 2] = p(p(node))).

 	For every node we store an array jump[node][k] giving the ancestor of level 2^k. (jump[node][k] = p(p(p(...p(node)))) )
 																											2^k times
 	The index requires O(NlongN) time to build and O(NlogN) memory to store.
 	We will actually store the array ancestor only for the leafs. This will guarantee O(V + L*logV) complexity. (V nodes and L leafs)

 Stair Search:
 	We find the deepest leaf from the subtree T[node] rooted at node. (find pathIndex[node] and output the last element of that path)
 	That leaf is (ancestorLevel + height[node]) steps away from the ancestor we look for.
 	The new search query is: search(node, level) = search(leaf, level+height[node]).
 	We represent the number ancestorLevel as: ancestorLevel = 2^k + ancestorLevel'
 	with 0 < ancestrorLevel' < 2^k. (k may be 0)
 	The node jump[leaf][k] is the 2^k level ancestor of the leaf.
 	The ancestor we are looking for is the ancestorLevel' ancestor of jump[leaf][k].
 	(p^(d)[node] = p^(2^k + d')[leaf] = p^(d')[p^(2^k)[leaf]] = p^(d')[jump[leaf][k]])
 	The stair of jump[leaf][k] is longer than 2^(k+1), and since ancestorLevel' < 2^k we get that the ancestor is on that stair.
 	The ancestor is stair[jump[leaf][k]][ancestorLevel'].
 	Search is done in O(1) time.
*/
stairStruct BuildStairIndex(const tree& T) {
	stairStruct stairIndex;

	std::vector<treeNode> nodes = T.GetNodes();
	std::unordered_map<treeNode, treeNode> parents = T.GetParents();
	std::unordered_map<treeNode, int> depths = T.GetDepths();
	std::unordered_map<treeNode, int> heights = T.GetHeights();
	treeNode root = T.GetRoot();
	int treeHeight = T.GetTreeHeight();
	int numNodes = T.GetNumNodes();

	stairIndex.parents = parents;
	stairIndex.depths = depths;

	/* sorting leafs in linear time */
	std::vector<std::list<treeNode> > leafs(treeHeight + 1);
	for (treeNode node: nodes) {
		if (heights[node] == 0) {
			int depth = depths[node];
			leafs[depth].push_back(node);
		}
	}

	std::list<treeNode> sortedLeafs;
	for (int index = 0; index <= treeHeight; index++) {
		while (!leafs[index].empty()) {
			sortedLeafs.push_front(leafs[index].front());
			leafs[index].pop_front();
		}
	}
	// end

	/* building array of stairs. each stair is an array */
	int numStairs = sortedLeafs.size();
	stairIndex.stairs.resize(numStairs);
	std::vector<treeNode> mark(numNodes, 0);	// initialize all nodes to 'non-marked'
	int currentPathIndex = 0;
	int currentNodeIndex = 0;
	for (treeNode leaf: sortedLeafs) {
		/* creating the max path for 'leaf' */
		std::vector<treeNode> currentPath;
		treeNode currentNode = leaf;
		do {
			mark[currentNode] = 1;
			currentPath.push_back(currentNode);
			stairIndex.pathIndex[currentNode] = currentPathIndex;
			currentNode = parents[currentNode];
		} while ((currentNode != -1) && mark[currentNode] == 0);

		/* doubling the path */
		int pathLength = currentPath.size();
		int i = 1;
		while ((currentNode != -1) && (i <= pathLength)) {
			currentPath.push_back(currentNode);
			currentNode = parents[currentNode];
			i++;
		}
		int stairLength = currentPath.size();

		/* reversing the array */
		currentNodeIndex = 0;
		for (i = stairLength - 1; i >=0 ; i--) {
			treeNode node = currentPath[i];
			stairIndex.stairs[currentPathIndex].push_back(node);
			if (i < pathLength) {
				stairIndex.nodeIndex[node] = currentNodeIndex + (stairLength - pathLength);	// the node index is ofset by (stairLength - pathLength)
				currentNodeIndex++;				
			}
		}
		currentPathIndex++;
	}
	// end

	/* building and array of ancestors for each leaf */
	stairIndex.power.resize(numNodes);
	stairIndex.deg.resize(numNodes);
	stairIndex.power[0] = 1;
	int deg = 0;
	for (int i = 1; i <= numNodes; i++) {
		stairIndex.power[i] = 2 * stairIndex.power[i - 1];
		if (i >= stairIndex.power[deg + 1]) {
			deg++;
		}
		stairIndex.deg[i] = deg;
	}

	for (treeNode leaf: sortedLeafs) {
		int k = 0;
		treeNode ancestor = parents[leaf];
		while (true) {
			stairIndex.jump[leaf].push_back(ancestor);	// ancestor of level 2^k
			int pathIndex = stairIndex.pathIndex[ancestor];	// the path of this ancestor is at least 2^k long
			int nodeIndex = stairIndex.nodeIndex[ancestor];	// the corresponding stair is at least 2^(k+1) long
			if (nodeIndex < stairIndex.power[k]) {	// in this case the stair contains the root and this stair is shortar than 2^(k+1)
				break;	// no more ancestors of type 2^k;
			} else {
				ancestor = stairIndex.stairs[pathIndex][nodeIndex - stairIndex.power[k]];	// ancestor = p^(2^k)[ancestor] = p^(2^(k+1))[leaf]
				k++;
			}
		}
	}
	// end

	return stairIndex;
}

treeNode StairSearch(treeNode node, int ancestorLevel, const stairStruct& stairIndex) {
	auto getPathIndex = stairIndex.pathIndex.find(node);
	int pathIndex = getPathIndex->second;

	int stairSize = stairIndex.stairs[pathIndex].size();
	treeNode leaf = stairIndex.stairs[pathIndex][stairSize - 1];

	auto getDepth = stairIndex.depths.find(leaf);
	int leafDepth = getDepth->second;

	getDepth = stairIndex.depths.find(node);
	int nodeDepth = getDepth->second;

	ancestorLevel += (leafDepth - nodeDepth);
	return StairSearchLeaf(leaf, ancestorLevel, stairIndex);
}

treeNode StairSearchLeaf(treeNode leaf, int ancestorLevel, const stairStruct& stairIndex) {
	if (ancestorLevel == 0) {
		return leaf;
	}

	int k = stairIndex.deg[ancestorLevel];	// 2^k <= ancestorLevel < 2^(k+1)
	ancestorLevel -= stairIndex.power[k];

	auto getAncestor = stairIndex.jump.find(leaf);
	if ((getAncestor->second).size() < k) {
		return -1;
	}
	
	treeNode ancestor = (getAncestor->second)[k];	// jump[leaf][k] = p^(2^k)[leaf]

	auto getPathIndex = stairIndex.pathIndex.find(ancestor);
	int pathIndex = getPathIndex->second;
	auto getNodeIndex = stairIndex.nodeIndex.find(ancestor);
	int nodeIndex = getNodeIndex->second;

	if (nodeIndex < ancestorLevel) {
		return -1;
	}

	ancestor = stairIndex.stairs[pathIndex][nodeIndex - ancestorLevel];
	return ancestor; 
}