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
To solve the <i>LA</i> problem we will decompose the tree into paths. To understand why this is advantageous let us consider a single path of the tree. Solving the <i>LA</i> problem on a single path of length <i>m</i> can be done by maintaining an array <i>Path[0...m-1]</i>, where the nodes of the path are stored in top-to-bottom order from root to leaf. Suppose node <i>u</i> is stored at position <i>i</i>, then to answer <i>LA(u, k)</i> (for <i>k &le; i</i>) we simply return  
<i>Path[i - k]</i>.  

Looking for an optimal solution, the tree must be decomposed into paths with maximal lengths. We will find a <i>long-path decomposition</i> of the tree <i>T</i> by greedily decomposing the tree into disjoint paths. At each step we find the longest root-leaf path in <i>T</i> and remove it from the tree. This removal breaks the tree into subtrees <i>T<sub>1</sub> , T<sub>2</sub></i> , .... Recursively split these subtrees by removing their longest root-leaf paths. Each removed path is stored as an array in top-to-bottom path order (from root to leaf).  

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

Let <i>v<sub>0</sub> = v</i>, 
<i>v<sub>1</sub> = p(Paths<sub>v<sub>0</sub></sub>[0])</i>, 
<i>v<sub>2</sub> = p(Paths<sub>v<sub>1</sub></sub>[0])</i>, ..., 
v<sub>k</sub> be the nodes for which the querying procedure has been recursively called. Then we have the following:  
  * <i>Paths<sub>path(v<sub>i</sub>)</sub> &cap; Paths<sub>path(v<sub>j</sub>)</sub> = &empty;</i>  
  * <i>Paths<sub>path(v<sub>i</sub>)</sub> + 1 &le; Paths<sub>path(v<sub>i + 1</sub>)</sub></i>  
  * <i>&Sum;<sub>0 &le; i &le; k</sub> |Paths<sub>path(v<sub>i</sub>)</sub>| &le; n</i>  

<i>Paths<sub>path(v<sub>i</sub>)</sub> + 1 &le; Paths<sub>path(v<sub>i + 1</sub>)</sub></i>  
<i>&rarr; Paths<sub>path(v<sub>0</sub>)</sub> + i &le; Paths<sub>path(v<sub>i</sub>)</sub></i>  
<i>&rarr; &Sum; |Paths<sub>path(v<sub>i</sub>)</sub>| &ge; &Sum; (|Paths<sub>path(v<sub>0</sub>)</sub>| + i) &ge; &Sum; i</i>  
<i>&rarr; &Sum;<sub>0 &le; i &le; k</sub> i &le; n</i>  

In the worst case the "&le;" sign is an "=" sign and we have that querying can be done in <i>O(&radic;n)</i> time.  
  * <i>O(n)</i> processing time  
  * <i>O(&radic;n)</i> query time  

![path decomposition](img/path_decomposition.png)  

### Ladder Algorithm ###
For the path decomposition we had the following relation:  
<i>Paths<sub>path(v<sub>i</sub>)</sub> + 1 &le; Paths<sub>path(v<sub>i + 1</sub>)</sub></i>  

With this relation we achieved <i>O(&radic;n)</i> query time. To achieve <i>O(log n)</i> query time we must have the following relation:  
<i>Paths<sub>path(v<sub>i</sub>)</sub> * 2 &le; Paths<sub>path(v<sub>i + 1</sub>)</sub></i>  

Then:  
<i>Paths<sub>path(v<sub>0</sub>)</sub> * 2<sup>i</sup> &le; Paths<sub>path(v<sub>i</sub>)</sub></i>  
<i>&Sum; |Paths<sub>path(v<sub>i</sub>)</sub>| &ge; &Sum; (|Paths<sub>path(v<sub>0</sub>)</sub>| * 2<sup>i</sup>) &ge; &Sum;<sub>0 &le; i &le; k</sub> 2<sup>i</sup></i>  

And we have <i>k &in; O(log n)</i>  

For this reason we extend the long paths into <i>Ladders</i>: for every path <i>Paths<sub>i</sub></i> we build a ladder <i>Ladders<sub>i</sub></i> by doubling the path. Each path is extended upward by adding the immediate ancestors at the top of the path to the array. Extending the paths into ladders naively requires <i>O(n)</i> time.  

Again for every node we store the following information:   
  * <i>path(v) = i &rarr; v &in; Ladders<sub>i</sub></i>  
  * <i>ind(v) = j &rarr; Ladders<sub>path(v)</sub>[j] = v</i>  

We could again answer level ancestor queries by jumping from ladder to ladder. However, for every node <i>v</i> we could store in a sparse table every <i>2<sup>l</sup> -th</i> ancestor of that node. Then, to answer the level ancestor query <i>LA(v, k)</i>, we compute <i>d</i> and <i>l</i> such that:  
<i>k = 2<sup>l</sup> + d</i>  
<i> 0 &le; d < 2<sup>l</sup></i>  
Let <i>u = p<sup>2<sup>l</sup></sup>(v)</i>, then <i>p<sup>k</sup>(v) = p<sup>d</sup>(u)</i>. Thus, we have:  
<i>LA(v, k) = Ladder<sub>path(u)</sub>[ind(u) - d]</i>

To see why this is the case let <i>h<sub>v</sub> = height(v)</i> be the number of nodes in the longest downward path from node <i>v</i> to a leaf. Node <i>v</i> belongs to path <i>Paths<sub>path(v)</sub></i>. Since this path was build greedily it has at least <i>h<sub>v</sub></i> nodes. Thus, the array <i>Ladder<sub>path(v)</sub></i> has at least <i>2 * h<sub>v</sub></i> elements, and also this array contains at least <i>h<sub>v</sub></i> ancestors of <i>v</i>. Now, since node <i>u = p<sup>2<sup>l</sup></sup>(v)</i>, then <i>h<sub>u</sub> = height(u) &ge; 2<sup>l</sup></i>. Also <i>Ladder<sub>path(u)</sub></i> contains at least <i>h<sub>u</sub></i> ancestors of node <i>u</i>, and in particular it contains <i>p<sup>d</sup>(u)</i>.  

What is more, instead of storing a sparse table for every node, we could store a sparse table only for the leaves of the tree. These nodes will be called <i>jump nodes</i>. To answer level ancestor queries we must also store a pointer from every node to its jump node descendant.  
Let <i>j<sub>v</sub> = jump(v)</i> be the jump node to which node <i>v</i> points. Then:  
<i>LA(v, k) = LA(j<sub>v</sub>, k + depth(j<sub>v</sub>) - depth(v))</i>  

The sparse table has <i>O(Llog n)</i> entries, where <i>L</i> is the number of leaves. To build the table in <i>O(Llog n)</i> time we will build it bottom up. For every leaf <i>v</i> do the following:  
  1. Allocate an array <i>p<sub>v</sub>[0, 1, ..., logn]</i>  
  2. Initialize <i>p<sub>v</sub>[0] = v</i>  
  3. The <i>2<sup>l + 1</sup></i> level ancestor of <i>v</i> is stored in the ladder of the <i>2<sup>l</sup></i> level ancestor of <i>v</i>  
        <i>p<sup>2<sup>l + 1</sup></sup>(v) = p<sup>2<sup>l</sup></sup>(p<sup>2<sup>l</sup></sup>(v))</i>  
        <i>u = p<sub>v</sub>[l]</i>  
        <i>d = 2<sup>l</sup> - 1</i>  
        <i>p<sub>v</sub>[l + 1] = p(Ladders<sub>path(u)</sub>[ind(u) - d])</i>  

  * <i>O(n + Llog n)</i> processing time  
  * <i>O(1)</i> query time  

![ladder decomposition](img/ladder_decomposition.png) 

### The Macro-Micro-Tree Algorithm ###
In the previous algorithm computing the ladders takes linear time. The bottleneck is computing the sparse table. It takes <i>O(Llog n)</i> time. To achieve linear boundary of the algorithm the tree must have <i>O(n / log n)</i> leaves.  

To speed up the algorithm we will use a <i>micro-macro division</i> of the tree. A micro-macro divison partitions the nodes of a tree into a <i>macro</i> tree and <i>micro</i> trees, where each micro tree is a connected subtree of the original tree.

![macro micro tree](img/macro_micro_tree.png)  

Let <i>T = (V, p r)</i> be a rooted tree and let <i>B &in; &#8469;</i>. Let us consider a micro-macro division of <i>T</i> such that all micro trees contain at most <i>B</i> nodes:  
  1. A <i>micro node</i> is any node <i>v</i> such that <i>h<sub>v</sub> &le; B</i>.  
  2. A <i>macro node</i> is any node <i>v</i> such that <i>h<sub>v</sub>  > B</i>.  
  3. A <i>micro tree</i> is a subtree <i>T<sub>v</sub></i> rooted at node <i>v</i> such that:  
      <i>|T<sub>v</sub>| &le; B</i>  
      <i>p(v)</i> is a macro node  
  4. A <i>macro leaf</i> is a macro node such that every child of that node is a micro node.  

The idea here is to compute a sparse table for all macro leaves, and to compute a simple naive table for all micro trees. However, building a table for every micro tree would not work because there are too many micro trees. Instead we will enumerate all possible shapes of trees of size at most <i>B</i> and build a simple table for them.  

Considering this micro-macro division of <i>T</i> we can easily show that the number of macro leaves is at most <i>n / B</i>, where <i>n</i> is the number of nodes in <i>T</i>. Since every macro leaf <i>l</i> is a macro node we have that <i>|T<sub>l</sub>| > B</i>. Also, for every two macro leaves <i>l<sub>i</sub></i> and <i>l<sub>j</sub></i> we have that <i>T<sub>l<sub>i</sub></sub> &cap; T<sub>l<sub>i</sub></sub> = &empty;</i>. Then:  

<i>kB &le; &sum; |T<sub>l<sub>i</sub></sub>| = |&#8899; L<sub>l<sub>i</sub></sub>| &le; n</i>  
<i>k &le; n / B</i>  

We can also show that the number of possible shapes of trees of size at most <i>B</i> is no more than <i>4<sup>B</sup></i>. Performing a depth-first traversal on a tree of size <i>m</i> and enumerating every down-traversal as 0 (from parent to child) and every up-traversal as 1 (from child to parent), the shape of the tree is uniquely determined by the <i>2(m-1)-pattern</i> of 0s and 1s. Thus, there are no more than <i>2<sup>2(m - 1)</sup></i> possible shapes for trees with size <i>m</i>. The total number of possible shapes of trees of size at most <i>B</i> is:  
<i>&sum;<sub>1 &le; m &le; B</sub> 2<sup>2(m - 1)</sup> = &sum; <sub>0 &le; m &le; B-1</sub> 4<sup>m</sup> = (4<sup>B</sup> - 1) / 3 < 4<sup>B</sup></i>  

For the total preprocessing time we have the following:  
<i>O(n / B * log n + 4<sup>B</sup> * B<sup>2</sup>)</i>  
Thus we must have:  
  * <i>n / B * log n &in; O(n)</i>  
  * <i>4<sup>B</sup> * B<sup>2</sup> &in; O(n)</i>  

From the first equation we can see that <i>B &ge; c * log n</i> for some constant <i>c</i>.  
Substituting in the second equation we have:  
<i>4<sup>c log n</sup> * (c log n)<sup>2</sup> &in; O(n)</i>  
<i>n<sup>2c</sup> * c<sup>2</sup> * log<sup>2</sup> n &in; O(n)</i>  

Choosing <i>c < 1/2</i> we can see that we have an asymptotically tight bound.  
For example if <i>c = 1/4</i> we have <i>O(&radic;n log<sup>2</sup> n)</i> processing time.  

Querying the structure is performed at two steps. Given a query <i>LA<sub>T</sub>(v, k)</i> first we check whether the height of node <i>v</i> is greater or smaller than the value <i>B</i>.  
  * If <i>h<sub>v</sub> > B</i> then <i>v</i> is a macro node belonging to <i>T<sub>macro</sub></i> and we store a pointer to one of the macro leaves <i>l<sub>v</sub> = leaf(v)</i>. Having <i>l<sub>v</sub></i> we can simply use the ladder decomposition algorithm.  
  * If <i>h<sub>v</sub> &le; B</i> then <i>v</i> is a micro node and we store a pointer to the root of the micro tree <i>T<sub>micro<sub>i</sub></sub></i> that it belongs to (<i>r<sub>v</sub> = root(v)</i>).  
  In case <i>k > depth(v) - depth(r<sub>v</sub>)</i> we can again use the ladder decomposition algorithm. Otherwise <i>k &le; depth(v) - depth(r<sub>v</sub>)</i> and the level <i>k</i> ancestor of node <i>v</i> is located inside the micro tree <i>T<sub>micro<sub>i</sub></sub></i>. Now we simply find the simple table associated with that tree and perform a table lookup.

In conclusion the complexity of the algorithm is:  
  * <i>O(n + Llog n)</i> processing time  
  * <i>O(1)</i> query time  


## ENCODING MICRO TREES ##
As noted above every micro tree is uniquely encoded by the sequence of down-traversals and up-traversals performed on a depth-first traversal. We will now show that the number of shapes is <i>&Theta;(4<sup>B</sup>)</i>.  
As before we will encode every down-traversal as 0 and every up-traversal as 1. Let <i>w(T)</i> be the bit sequence of 0s and 1s corresponding to traversing the tree <i>T</i>. Since a depth-first traversal starts at the root of the tree and ends at the root of the tree, we must have the same number of down-traversals and up-traversals. Considering a tree with <i>n</i> nodes, we have <i>n-1</i> down-traversals and <i>n-1</i> up-traversals.  
Thus, we can visualise <i>w(T)</i> as a path starting from <i>(0, 0)</i> and ending at <i>(n-1, n-1)</i> with <i>(n-1) &rarr;</i> and <i>(n-1) &#8593;</i>.  
It is important to note that the number of down-traversals is always greater than or equal to the number of up-traversals. Thus, the path representing <i>w(T)</i> does not cross the diagonal <i>y = x</i>, i.e. the path does not contain any points of the type <i>(k, k+1)</i>.  
Call any path starting from <i>(0, 0)</i> and ending at <i>(n-1, n-1)</i> <i>"good"</i> if the path has <i>(n-1)</i> &rarr; and <i>(n-1)</i> &#8593;, and does not contain any point of the type <i>(k, k+1)</i>. Call the path <i>"bad"</i> if it cointains points of the type <i>(k, k+1)</i>.  

![micro tree encoding](img/micro_tree_encoding.png)  

The total number of paths starting from <i>(0, 0)</i> and ending at <i>(n-1, n-1)</i> is <i>C<sub>n-1</sub><sup>2(n-1)</sup>. We have <i>2(n-1)</i> positions and we have to choose <i>(n-1)</i> of them and place &rarr; on these positions.  
Thus the number of good paths is:  

![#good](https://latex.codecogs.com/svg.latex?\text{good}=C_{n-1}^{2(n-1)}-\text{bad})  

Every "bad" path can be modified in the following way:  
  1. Leave the path unchanged until the first time it crosses a point of the type <i>(k, k+1)</i>.  
  2. After that change every &rarr; with &#8593; and every &#8593; with &rarr;.  

The modified path has <i>k + ((n-1) - (k-1)) = n-2</i> &rarr; and <i>k+1 + ((n-1) - k) = n</i> &#8593;. Thus, every modified path starts at <i>(0, 0)</i> and ends at <i>(n-2, n)</i>.  
We can see that every path starting at <i>(0, 0)</i> and ending at <i>(n-2, n)</i> can be modified using the reversed procedure and the result would be a path starting at <i>(0, 0)</i> and ending at <i>(n-1, n-1)</i>. Thus, the number of <i>"bad"</i> paths is exactly equal to the total number of paths starting from <i>(0, 0)</i> and ending at <i>(n-2, n)</i>.  

![#bad](https://latex.codecogs.com/svg.latex?\text{bad}=C_{n-2}^{2(n-1)})  
![#good](https://latex.codecogs.com/svg.latex?\text{good}=C_{n-1}^{2(n-1)}-C_{n-2}^{2(n-1)})  

![compute #good](https://latex.codecogs.com/svg.latex?\text{good}=\frac{(2(n-1))!}{(n-1)!(n-1)!}-\frac{(2(n-1))!}{(n-2)!n!}=\frac{(2(n-1))!}{(n-1)!(n-1)!}\left(1-\frac{n-1}{n}\right))  
![compute #good cont](https://latex.codecogs.com/svg.latex?\text{good}=\frac{1}{n}\binom{(2(n-1))}{n-1})  
