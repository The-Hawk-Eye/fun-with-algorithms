# Correctness and Complexity


## INTRODUCTION ##
Given a rooted tree <i>T = (V, p, r)</i>, a node <i>u</i> and an integer <i>k</i>, the goal is to find the <i>k-th</i> ancestor of node <i>u</i>:  

<i>LA<sub>T</sub>(u, k) = p<sup>k</sup>(u)</i>  

where <i>p<sup>n</sup>(u) = p(p<sup>n-1</sup>(u))</i> if <i>n > 0</i>  
and <i>p<sup>0</sup>(u) = u</i>  

The <i>Level Ancestor</i> problem is to preprocess a given rooted tree T to support level ancestor queries. Both the preprocessing time and the query time must be optimized.  

![la problem](img/la_problem.png)  

<i>T</i> can be preprocessed in time <i>O(n)</i> (where <i>n</i> is the number of nodes), to answer <i>LA</i> queries in time <i>O(1)</i>.  
If an algorithm has preprocessing time <i>f(n)</i> and query time <i>g(n)</i>, we will say that the algorithm has complexity <i>\<f(n), g(n)\></i>. Thus, the solution to the <i>LA</i> problem has complexity <i>\<O(n), O(1)\></i>.  
 The algorithm presented here is from the paper <i>"The LA Problem Simplified"</i> by <i>Michael Bender</i> and <i>Martin Farach-Colton</i> from the year 2003.  


## SOLUTION TO THE <i>LA</i> PROBLEM ##
### Table Solution ###
A simple algorithm is based on the observation that there are only <i>&Theta;(n<sup>2</sup>)</i> possible queries in a tree of size <i>n</i>. If we precompute all of them in a table, we can answer <i>LA</i> in <i>O(1)</i> time.

For every node <i>v &in; V</i> we have:  
<i>LA<sub>table</sub>[v][0] = v</i>  
<i>LA<sub>table</sub>[v][i + 1] = p(LA<sub>table</sub>[v][i])</i> if <i>LA<sub>table</sub>[v][i] &ne; NULL</i>  

Answering a query requires one simple table lookup.     
  * <i>O(n<sup>2</sup>)</i> processing time  
  * <i>O(1)</i> query time  

### Path Decomposition ###
To solve the <i>LA</i> problem we will decompose the tree into paths. To understand why this is advantageous, let us consider a single path of the tree. Solving the <i>LA</i> problem on a single path of length <i>m</i> can be done by maintaining an array <i>Path[0...m-1]</i>, where the nodes of the path are stored in top-to-bottom order from root to leaf. Suppose node <i>u</i> is stored at position <i>i</i>, then to answer <i>LA(u, k)</i> (for <i>k &le; i</i>) we simply return <i>Path[i - k]</i>.  

Looking for an optimal solution, the tree must be decomposed into paths with maximal lengths. We will find a <i>long-path decomposition</i> of the tree <i>T</i> by greedily decomposing the tree into disjoint paths. At each step we find the longest root-leaf path in <i>T</i> and remove it from the tree. This removal breaks the tree into subtrees <i>T<sub>1</sub> , T<sub>2</sub> , .... Recursively split these subtrees by removing their longest root-leaf paths. Each removed path is stored as an array in bottom-up path order (from leaf to root).  

To find a long-path decomposition of the tree <i>T</i> in linear time we use the following procedure:  
  1. Compute the depths of the nodes of the tree. This can be done in <i>O(n)</i> time using simple breadth-first traversal.  
  2. Build a list of the leaves of the tree sorted by depths in descending order <i>L = [l<sub>0</sub> , l<sub>1</sub> , ..., l<sub>k</sub>]</i>. This can be done in <i>O(n)</i> time using bucket sort.  
  3. Iteratively build longest path arrays starting with each of the leaves:  
  		3.1. Starting at leaf <i>l<sub>i</sub></i> traverse the tree upwards  
  		3.2. Mark every visited node  
  		3.3. Add every visited node to the path array  
  		3.4. Stop when reaching a node that is already marked, or when reaching the root  
  4. Store the path arrays in an array of arrays <i>Paths</i>  
  5. For every node store the number of the path array to which it belongs:  
  		<i>path(v) = i &rarr; v &in; Paths<sub>i</sub></i>  
  6. For every node store the position at which it occurs in the path array:  
  		<i>ind(v) = j &rarr; Paths<sub>path(v)</sub>[j] = v</i>  

To answer level ancestor queries we move upwards jumping from path to path:  
<i>LA(v, k) = Paths<sub>path(v)</sub>[ind(v) - k]</i> if <i>k &le; ind(v)</i>  
<i>LA(v, k) = LA(p(Paths<sub>path(v)</sub>[0]), k - ind(v) - 1)</i>, otherwise  

The complexity of this procedure depends on the number of paths we traverse. Given a node <i>v</i>, let <i>u = p(Paths<sub>path(v)</sub>[0])</i>. Then we have the following:  
<i>|Paths<sub>path(v)</sub>| + 1 &le; |Paths<sub>path(u)</sub>|</i>  
Since we used greedy decomposition the node <i>u</i> must belong to a longer path than the node <i>v</i>.  

Let <i>v<sub>0</sub> = v<i>, 
<i>v<sub>1</sub> = p(Paths<sub>v<sub>0</sub></sub>[0])</i>, 
<i>v<sub>2</sub> = p(Paths<sub>v<sub>1</sub></sub>[0])</i>, ..., 
v<sub>k</sub> be the nodes for which the querying procedure has been recursively called. Then we have the following:  
  * <i>Paths<sub>path(v<sub>i</sub>)</sub> &cup; Paths<sub>path(v<sub>j</sub>)</sub> = &empty;</i>  
  * <i>Paths<sub>path(v<sub>i</sub>)</sub> + 1 &le; Paths<sub>path(v<sub>i + 1</sub>)</sub></i>  
  * <i>&Sum;<sub>0 &le; i &le; k</sub> |Paths<sub>path(v<sub>i</sub>)</sub>| = n</i>  

<i>
Paths<sub>path(v<sub>i</sub>)</sub> + 1 &le; Paths<sub>path(v<sub>i + 1</sub>)</sub>  
&rarr; Paths<sub>path(v<sub>0</sub>)</sub> + i &le; Paths<sub>path(v<sub>i</sub>)</sub>  
&rarr; &Sum; |Paths<sub>path(v<sub>i</sub>)</sub>| &ge; &Sum; (|Paths<sub>path(v<sub>0</sub>)</sub>| + i) &ge; &Sum; i  
&rarr; &Sum;<sub>0 &le; i &le; k</sub> &le; n  
</i>

In the worst case the "&le;" sign is an "=" sign and we have that querying can be done in <i>O(&sqrt;n)</i> time.  
  * <i>O(n)</i> processing time  
  * <i>O(&sqrt;n)</i> query time  

![path decomposition](img/path_decomposition.png)  


