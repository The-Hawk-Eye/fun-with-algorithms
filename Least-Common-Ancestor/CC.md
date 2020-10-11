# Correctness and Complexity


## INTRODUCTION ##
A fundamental algorithmic problem on trees is how to find the Least Common Ancestor (LCA) of a pair of nodes. The LCA of nodes <i>u</i> and <i>v</i> in a tree is the shared ancestor of <i>u</i> and <i>v</i> that is located farthest from the root.  

Given a rooted tree <i>T = (V, p, r)</i>  
<i>LCA<sub>T</sub>(u, v) = w</i>  
where <i>w &isin; { p<sup>(k)</sup>(u) | k &isin; &#8469; } &cup; { p<sup>(k)</sup>(v) | k &isin; &#8469; }</i>, and <i>w</i> has maximum depth from the root  

<i>T</i> can be preprocessed in time <i>O(n)</i> (where <i>n</i> is the number of nodes), to answer <i>LCA</i> queries in time <i>O(1)</i>.  
If an algorithm has preprocessing time <i>f(n)</i> and query time <i>g(n)</i>, we will say that the algorithm has complexity <i>\<f(n), g(n)\></i>. Thus, the solution to the <i>LCA</i> problem has complexity <i>\<O(n), O(1)\></i>.  
 The algorithm presented here is from the paper <i>"The LCA Problem Revisited"</i> by <i>Michael Bender</i> and <i>Martin Farach-Colton</i> from the year 2000.  

This solution to the <i>LCA</i> problem relies heavily on the solution to the <i>RMQ</i> problem.  
The <i>Range Minimum Query</i> (RMQ) problem is the following:  
<i>Given an array A and two indecies i and j (i &le; j), what is the index of the smallest element out of A[i...j]?</i>  
<i>RMQ<sub>A</sub>(i, j) = k &harr; A[k] = min A[i...j]</i>  

The <i>LCA</i> problem can be reduced in <i>O(n)</i> time to a special case of the <i>RMQ</i> problem called the <i>&plusmm;1 RMQ</i>.  
We will show that the solution to the <i>&plusmn;1 RMQ</i> problem has complexity <i>\<O(n), O(1)\></i>.  
Finally, we will show that the <i>RMQ</i> problem can be solved in <i>\<O(n), O(1)\></i> time using <i>Cartesian Trees</i>.  

<!-- Finally, the <i>RMQ</i> problem can be reduced in <i>O(n)</i> time back to the <i>LCA</i> problem. -->

<!-- insert pic -->


## REDUCTION OF <i>LCA</i> TO <i>RMQ</i> IN <i>O(n)</i> TIME ##
The <i>LCA</i> problem can be reduced to the <i>RMQ</i> problem by traversing the tree in an <i>Euler Tour</i>.  

Let <i>E[1...(2n-1)]</i> store the nodes visited in the Euler Tour.  
Let <i>L[1...(2n-1)]</i> store the levels of the nodes visited in the Euler Tour. The level of a node is its distance from the root. <i>L[i]</i> is the level of node <i>E[i]</i>.  
Let <i>R[1...n]</i> store the first occurance of every node in the Euler Tour. <i>R[i] = argmin<sub>j</sub> (E[j] = i)</i>  

![alt text](https://github.com/cacao-macao/fun-with-algorithms/blob/master/Least-Common-Ancestor/img/euler_tour.png)

Let <i>u, v &isin; V</i> and let <i>i<sub>u</sub> = R[u] < i<sub>v</sub> = R[v]</i>  
Let <i>k = RMQ<sub>L</sub>(i<sub>u</sub>, i<sub>v</sub>)</i>  
Then <i>LCA(u, v) = E[k]</i>  
To see why this is the case consider the node <i>w = E[k]</i>.  
  * If this is the first visit to node <i>w</i>, then there must be a node <i>w'</i> from which we descended to visit <i>w</i> for the first time. This means that <i>L[R[w']] < L[k]</i> - contradiction.  
  * If this is the last visit to node <i>w</i>, then there must be a node <i>w'</i> to which we ascend after the visit. This means that <i>L[R[w']] < L[k]</i> - contradiction.  
This means that nodes <i>u</i> and <i>v</i> were visited after the first visit to <i>w</i>, but before the last visit to <i>w</i>. Thus, <i>w</i> is an ancestor of both <i>u</i> and <i>v</i>.  
Now let <i>z</i> be an ancestor of both <i>u</i> and <i>v</i>, and let <i>Last[z] = argmax<sub>j</sub> (E[j] = z)</i> be the last visit to <i>z</i>. We have that <i>R[z] < i<sub>u</sub> < k <i<sub>v</sub> < Last[z]</i>. Thus, node <i>w</i> is visited inside the interval [R[z], Last[z]]  
&rarr; node <i>w</i> is a descendant of node <i>z</i>  
&rarr; node <i>w</i> has the maximum depth from the root.  

Building each of the three arrays takes time <i>O(n)</i>, thus the reduction of <i>LCA</i> to <i>RMQ</i> can be done in <i>O(n)</i> time.


## SOLUTION TO THE <i>RMQ</i> PROBLEM ##
### Two simple algorithms ###
A simple algorithm for evaluating <i>RMQ<sub>A</sub>(i, j)</i> is to just iterate across the elements between <i>i</i> and <i>j</i>, and take the minimum.  
  * <i>O(1)</i> processing time  
  * <i>O(n)</i> query time  

Another simple algorithm is based on the observation that there are only <i>&Theta;(n<sup>2</sup>)</i> possible queries in an array of length <i>n</i>. If we precompute all of them in a table, we can answer <i>RMQ</i> in <i>O(1)</i> time. Naively precomputing each entry requires <i>O(n)</i>, totaling <i>O(n<sup>3</sup>)</i> preprocessing time, which is inefficient. However, we can precompute all subarrays in time <i>&Theta;(n<sup>2</sup>)</i> using dynamic programming.  
<i>RMQ<sub>table</sub>(i, j) = i, if i = j</i>  
<i>RMQ<sub>table</sub>(i, j) = j, if A[j] <= A[RMQ<sub>table</sub>(i, j-1)]</i>  
<i>RMQ<sub>table</sub>(i, j) = A[RMQ<sub>table</sub>(i, j-1)], otherwise</i>  
  * <i>O(n<sup>2</sup>)</i> processing time  
  * <i>O(1)</i> query time  

### Sparse Tables ###
The <i>\<O(n<sup>2</sup>), O(1)\></i> solution gives fast queries because every range we might look up has already been precomputed. But the preprocessing is slow because we have to precompute the minimum of every possible range.  
If we precompute the answers on too many ranges, the preprocessing will be slow. If we precompute the answers on too few ranges, the query time will be slow.  

![alt text](https://github.com/cacao-macao/fun-with-algorithms/blob/master/Least-Common-Ancestor/img/observation.png)

We want to precompute <i>RMQ</i> over <i>o(n<sup>2</sup>)</i> set of ranges such that <i>O(1)</i> query time is supported.  
For each index <i>i</i>, we will compute <i>RMQ</i> for ranges starting at <i>i</i> of size 1, 2, 4, 8,..., 2<sup>k</sup> as long as they fit in the array.  
Any range of the array can be formed as the union of two of these ranges. To see why this is the case consider the query <i>RMQ(i, j)</i>. Let <i>l</i> be such that <i>2<sup>k</sup> &le; j - i + 1 &le; 2<sup>k + 1</sup></i>. Then:  
<i>RMQ(i, j) = min(RMQ(i, i + 2<sup>k</sup> - 1), RMQ(j - 2<sup>k</sup> + 1, j))</i>  
Each range can be looked up in time <i>O(1)</i>. We must precompute a table <i>log[0...n]</i> such that <i>log[i] = k &harr; 2<sup>k</sup> &le; i < 2<sup>k + 1</sup></i>. Now the total query time is <i>O(1)</i>.  
The total number of ranges is <i>O(nlogn)</i>. Again, using dynamic programming we can compute all of them in time <i>O(nlogn)</i>.  
<i>RMQ(i, 0) = i</i>  
<i>RMQ(i, k + 1) = RMQ(i, k), if RMQ(i, k) < RMQ(i + 2<sup>k</sup>, k)</i>
<i>RMQ(i, k + 1) = RMQ(i + 2<sup>k</sup>, k), otherwise</i>  
  * <i>O(nlogn)</i> processing time  
  * <i>O(1)</i> query time  

![alt text](https://github.com/cacao-macao/fun-with-algorithms/blob/master/Least-Common-Ancestor/img/sparse_table.png)

### Block Decomposition ###
We could speed up the algorithm by using <i>block decomposition</i>.  
  * Split the input into blocks of size <i>b</i>  
  * Form an array of the block minima  
  * Construct a "summary" <i>RMQ</i> structure over the block minima  
  * Construct "block" <i>RMQ</i> structures for each block  

Suppose we use a <i>\<p<sub>1</sub>(n), q<sub>1</sub>(n)\></i> time algorithm for the summary <i>RMQ</i> and a <i>\<p<sub>2</sub>(n), q<sub>2</sub>(n)\></i> time algorithm for each block.  
The preprocessing time for this hybrid structure would be: <i>O(n)</i> time to compute the minima of each block, <i>O(p<sub>1</sub>(n/b)</i> time to construct <i>RMQ</i> on the minima, and <i>O((n/b)p<sub>2</sub>(b))</i> time to construct the block <i>RMQ</i> structures.  

![alt text](https://github.com/cacao-macao/fun-with-algorithms/blob/master/Least-Common-Ancestor/img/block_structure.png)

The query time would be: <i>O(q<sub>1</sub>(n/b))</i> time to query the summary <i>RMQ</i>, and <i>O(q<sub>2</sub>(b))</i> time to query the block <i>RMQ</i> structures.  
  * <i>O(n + p<sub>1</sub>(n/b) + (n/b)p<sub>2</sub>(b))</i> processing time  
  * <i>O(q<sub>1</sub>(n/b) + q<sub>2</sub>(b))</i> query time  

Suppose we use the <i>\<O(nlogn), O(1)\></i> sparse table for both the summary and the block <i>RMQ</i> structures with block size of log<i>n</i>. We would have a <i>\<O(n logn logn), O(1)\></i> solution to the <i>RMQ</i> problem.  

![alt text](https://github.com/cacao-macao/fun-with-algorithms/blob/master/Least-Common-Ancestor/img/hybrid_structure.png)

### <i>O(n)</i> time solution to &plusmn;1 RMQ ###
Notice that if we want to build a <i>\<O(n), O(1)\></i> time algorithm for the <i>RMQ</i> structure using block decomposition, we need to have:  
  * <i>p<sub>2</sub>(n) = O(n)</i>  
  * <i>q<sub>2</sub>(n) = O(1)</i>  
It looks like we can't build an optimal <i>RMQ</i> unless we already have one.  

However, there is a key difference between our original problem and the new problem. Our original problem is: <b>solve <i>RMQ</i> on a single array in time <i>\<O(n), O(1)\></i></b>, and the new problem is: <b>solve <i>RMQ</i> on a large number of small arrays with O(1) query time and <i>total</i> processing time O(n)</b>.  

A key observation is that we can use the same block <i>RMQ</i> structure for similar arrays. Given block <i>B<sub>1</sub></i> and <i>B<sub>2</sub></i> of length <i>b</i>, we'll say that <i>B<sub>1</sub></i> and <i>B<sub>2</sub></i> <b>have the same block type</b> (<i>B<sub>1</sub> &sim; B<sub>2</sub></i>) if the following holds:  
<b><i> &forall; 0 &le; i &le; j < b: RMQ<sub>B<sub>1</sub></sub>(i, j) = RMQ<sub>B<sub>2</sub></sub>(i, j)</i></b>  
If we build an <i>RMQ</i> to answer queries on some block <i>B<sub>1</sub></i>, we can reuse that <i>RMQ</i> structure on some other block <i>B<sub>2</sub></i> if <i>B<sub>1</sub> &sim; B<sub>2</sub></i>.

There are two questions we need to answer:  
  * How can we tell when two blocks can share <i>RMQ</i> structures?  
  * How many block types are there, as a function of <i>b</i>?  

In the case of the <i>LCA</i> problem we are solving <i>RMQ</i> on the array <i>L[0...(2n-1)]</i>. However, in this particular case the following holds:  
<i>&forall;i: L[i] - L[i + 1] = &plusmn;1</i>  
This is known as the <i>&plusmn;1 RMQ</i>.  
Every block of the decomposition is unambiguously defined by the sequence of <i>1</i> or <i>-1</i> jumps between consecutive elements. We can assosiate each of the blocks with a <i>(b - 1)</i>-bit number, and thus, the total number of <i>structurally</i> different blocks is: <i>2<sup>b - 1</sup></i>.  
We could precompute a simple <i>RMQ</i> table for every type of block in <i>O(2<sup>b</sup>b<sup>2</sup>)</i> time.  
To preprocess the entire structure in <i>O(n)</i> time we need to choose <i>b</i> such that: <i>(n/b)log(n/b) + 2<sup>b</sup>b<sup>2</sup> &isin; O(n)</i>.  
Choosing <i>b = (logn / 2)</i> we have:  
(n/b)log(n/b) + 2<sup>b</sup>b<sup>2</sup> = 2(n/logn)logn + (1/4)log<sup>2</sup>n&radic;n &isin; O(n)


## <i>RMQ</i> IN <i>O(n)</i> TIME USING CARTESIAN TREES ##