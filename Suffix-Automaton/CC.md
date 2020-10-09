# Correctness and Complexity


## INTRODUCTION ##
A suffix automaton for a given string <i>w</i> is a minimal <b>DFA</b> (deterministic finite automaton) that accepts all the suffixes of the string <i>w</i>. For a string of length <b>n</b> it only requires <b><i>O(n)</i></b> memory and it can also be built in <b><i>O(n)</i></b> time. The algorithm was discovered in 1983 by <i>Blumer, Blumer, Haussler, Ehrenfeucht, Chen and Seiferas</i> and was presented in their paper <i>The smallest automaton recognizing the subwords of a text</i>. An important property of a suffix automaton is, that it contains information about all substrings of the string <i>w</i>. This is due to the following theorem:  
<i>Given two strings w and x, <b>x is a substring of w</b> if and only if <b>x is a prefix of a suffix of w</b>.</i>  
Any path starting at the initial state <b><i>s<sub>0</sub></i></b> forms a substring of <i>w</i>. And conversely every substring of <i>w</i> corresponds to a certain path starting at <b><i>s<sub>0</sub></i></b>.  


## NOTATION ##
&Sigma; - nonempty alphabet  
&Sigma;* - the set of all words over &Sigma;  
&epsilon; - the empty word  
<i>Suffix(w) = { &beta; &isin; &Sigma;* | &exist; &alpha; &isin; &Sigma;* : &alpha;&beta; = w }</i>  

A suffix automaton is a minimal DFA over the language <i>L = Suffix(w)</i>. From Nerode's theorem it follows that the number of states of the minimal DFA is equal to the number of equivalence classes in the relation <i>R<sub>L</sub></i>, where:  
<i>{&alpha;, &beta;} &isin; R<sub>L</sub> (&alpha; &equiv;<sub>L</sub> &beta;) &harr; &forall; z &isin; &Sigma;* : &alpha;z &isin; L &harr; &beta;z &isin; L</i>  

### End positions <b><i>end_pos</i></b> ###
Let <i>w</i> = a<sub>1</sub>a<sub>2</sub>...a<sub>n</sub> (a<sub>i</sub> &isin; &Sigma;) and let &alpha; &ne; &epsilon; &isin; &Sigma;*  
define: <i><b>end_pos<sub>w</sub>(&alpha;)</b> = { i | &alpha; = a<sub>i-|&alpha;|+1</sub>...a<sub>i</sub> }</i>  
<i>end_pos<sub>w</sub>(&alpha;)</i> is the set of all positions in the string <i>w</i>, in which the occurrences of &alpha; end  
<i>end_pos<sub>w</sub>(&epsilon;) = { 0, 1, 2, ..., |w| }</i>  

Two strings &alpha;, &beta; &isin; &Sigma;* are <b>end-equivalent on w</b> if and only if <i>end_pos<sub>w</sub>(&alpha;) = end_pos<sub>w</sub>(&beta;)</i>  
End-equivalence will be denoted by &equiv;<sub>w</sub> , i.e. &alpha; &equiv;<sub>w</sub> &beta; &harr; <i>end_pos<sub>w</sub>(&alpha;) = end_pos<sub>w</sub>(&beta;)</i>  

<b><i>Example:</i></b>
<pre>	<i>w = a b c b c</i>  
	<i>   0 1 2 3 4 5</i>  
    	<i>end_pos<sub>w</sub>(bc) = end_pos<sub>w</sub>(c) = {3, 5}</i>  
    	<i>bc ≡<sub>w</sub> c</i></pre>  

<b><i>Corollary:</i></b> The end-equivalence relation is equivalent to Nerode's relation <i>R<sub>L</sub></i> for the language <i>L = Suffix(w)</i>:  
&alpha; &equiv;<sub>w</sub> &beta; &harr; &alpha; &equiv;<sub>Suffix(w)</sub> &beta;  
<b><i>Proof:</i></b> Let <i>w</i> = a<sub>1</sub>a<sub>2</sub>...a<sub>n</sub> (a<sub>i</sub> &isin; &Sigma;) and let &alpha;, &beta;, z &isin; &Sigma;* . Then &alpha;z &isin; <i>Suffix(w)</i> &harr; &alpha;z = a<sub>n-|&alpha;z|+1</sub>...a<sub>n</sub>  
&rarr; &alpha; = a<sub>n-|&alpha;z|+1</sub>...a<sub>n-|z|</sub> and z = a<sub>n-|z|+1</sub>...a<sub>n</sub>  
&rarr; &alpha; = a<sub>i-|&alpha;|+1</sub>...a<sub>i</sub> and i = n - |z|  
But &alpha; &equiv;<sub>Suffix(w)</sub> &beta; &harr; &forall; z &isin; &Sigma;*  : &alpha;z &isin; <i>Suffix(w)</i> &harr; &beta;z &isin; <i>Suffix(w)</i>  
&harr; &forall; i: &alpha; = a<sub>i-|&alpha;|+1</sub>...a<sub>i</sub> &harr; &beta; = a<sub>i-|&beta;|+1</sub>...a<sub>i</sub>  
&harr; <i>end_pos<sub>w</sub>(&alpha;) = end_pos<sub>w</sub>(&beta;)</i>

<b><i>Properties:</i></b>  
Let &alpha;, &beta; &isin; &Sigma;* be subwords of <i>w</i> with |&alpha;| &le; |&beta;|, then:
  <i>
  1. end_pos<sub>w</sub>(&alpha;) &cap; end_pos<sub>w</sub>(&beta;) &ne; &empty; &rarr; &alpha; is a suffix of &beta;
  2. &alpha; is a suffix of &beta; &rarr; end_pos<sub>w</sub>(&beta;) &sube; end_pos<sub>w</sub>(&alpha;)
  3. We have either end_pos<sub>w</sub>(&alpha;) &sube; end_pos<sub>w</sub>(&beta;) or end_pos<sub>w</sub>(&alpha;) &cap; end_pos<sub>w</sub>(&beta;) = &empty;
  </i>

### Equivalence classes <b><i>[α]<sub>w</sub></i></b> and Representatives <b><i>r(α)</i></b> ###
Let &alpha; be an infix of <i>w</i>. Denote by [&alpha;]<sub>w</sub> the equivalence class of &alpha; with respect to the relation &equiv;<sub>w</sub> and denote by <b><i>r(&alpha;)</i></b> the longest word in the equivalence class [&alpha;]<sub>w</sub>. We say that <i>r(&alpha;)</i> canonically represents the equivalence class [&alpha;]<sub>w</sub>  
By definition <i>r(&epsilon;) = &epsilon;</i> 
<p></p>  

<b><i>Lemma:</i></b>  
Let &alpha; be an infix of <i>w</i>, then:  
  1. If there is a letter a &isin; &Sigma;, such that every occurance of &alpha; in <i>w</i> is preceeded by a, then &alpha; does not represent the equivalence class [&alpha;]<sub>w</sub>
  2. If &alpha; is a prefix of w, then &alpha; is the longest word in [&alpha;]<sub>w</sub>
  3. If there are letters x, y &isin; &Sigma;, x &ne; y and both x&alpha; and y&alpha; are infixes of <i>w</i>, then &alpha; canonically represents the equivalence class [&alpha;]<sub>w</sub>  
  4. &alpha; = r(&alpha;) &harr; &alpha; is a prefix of <i>w</i> or &alpha; occurs in two distinct left contexts

<b><i>Proof:</i></b>
  1. Let a preceed every occurance of &alpha; in <i>w</i>. Then for every i &isin; end_pos(&alpha;) we have w<sub>i-|&alpha;|</sub> = a  
  &rarr; i &isin; <i>end_pos(a&alpha;)</i>  
  &rarr; <i>end_pos(&alpha;) &sube; end_pos(a&alpha;)</i>  
  And since &alpha; is a suffix of a&alpha we have that <i>end_pos(a&alpha;) &sube; end_pos(&alpha;)</i> (by <i>Property 2.</i>)  
  &rarr; <i>end_pos(&alpha;) = end_pos(a&alpha;)</i>  
  It follows that &alpha; &equiv;<sub>w</sub> a&alpha; and |&alpha;| < |a&alpha;| &rarr; &alpha; &ne; r(&alpha;)
  2. Let |&alpha;| = i. Since &alpha; is a prefix of <i>w</i> we have &alpha; = a<sub>1</sub>...a<sub>i</sub> and i &isin; <i>end_pos(&alpha;)</i>.  
  Suppose &beta; &equiv;<sub>w</sub> &alpha; &rarr; i &isin; <i>end_pos(&beta;)</i> &rarr; |&beta;| &le; |a<sub>1</sub>...a<sub>i</sub>| = i = |&alpha;|
  3. Let x, y &isin; &Sigma;, x &ne; y and both x&alpha; and y&alpha; are infixes of <i>w</i>. Let i and j be such that:  
  i &isin; <i>end_pos(x&alpha;)</i>  
  j &isin; <i>end_pos(y&alpha;)</i>  
  Since &alpha; is a suffix of both x&alpha; and y&alpha; we have that i, j &isin; <i>end_pos(&alpha;)</i>  
  Let &beta; &equiv;<sub>w</sub> &alpha;, then i, j &isin; <i>end_pos(ß)</i>. Assume |&beta;| > |&alpha;| &rarr; |&beta;| &ge; |&alpha;| + 1 = |x&alpha;| = |y&alpha;|  
  &rarr; x&alpha; is a suffix of &beta; and y&alpha; is a suffix of &beta; &rarr; x = y - contradiction  

### Suffix links <b><i>slink</i></b> ###
The automaton <i>A<sub>w</sub> (&Sigma;, Q<sub>w</sub>, s<sub>0</sub>, F<sub>w</sub>, &delta;<sub>w</sub>)</i> with:  
<i>Q<sub>w</sub> = { r(&alpha;) | &alpha; is an infix of w }</i>  
<i>&delta;<sub>w</sub>(&alpha;, a) = r(&alpha;a), if &alpha;a is an infix of w</i>  
<i>F<sub>w</sub> = { &alpha; &isin; Q<sub>w</sub> | &alpha; is a suffix of w }</i>  
is a minimal DFA over the language L = Suffix(w).  
The states of the automaton are exactly the equivalence classes with respect to the relation &equiv;<sub>w</sub>  
For each state we will store the length of the longest word in the equivalence class: <b><i>len([&alpha;]<sub>w</sub>) = |r(&alpha;)|</i></b>  
For each state we will also store a pointer called a <b><i>suffix link</i></b> that points to the longest suffix of <i>w</i> that is in another equivalence class: <b><i>slink(&alpha;)</i></b> is the longest suffix of &alpha; such that <i>slink(&alpha;) &ne;<sub>w</sub> &alpha;</i>  

<b><i>Lemma:</b></i> <i>( Q<sub>w</sub> , slink, s<sub>0</sub> ) is a rooted tree.</i>  
<b><i>Proof:</b></i> We only need to show that <i>slink(&alpha;) &isin; Q<sub>w</sub></i> (i.e. every node has a parent). Since <i>slink(&alpha;)</i> is a suffix of &alpha; from <i>Property 2.</i> we have that <i>end_pos(&alpha;) &sube; end_pos(slink(&alpha;))</i>. And since <i>&alpha; &ne;<sub>w</sub> slink(&alpha;)</i>, we have that <i>end_pos(&alpha;) &ne; end_pos(slink(&alpha;))</i>.  
Let &alpha; = x•a•slink(&alpha;), x &isin; &Sigma;* , &alpha; &isin; &Sigma; and let <i>i &isin; end_pos(slink(α))\end_pos(α)</i>.  
If <i>i = |slink(&alpha;)|</i> &rarr; <i>slink(&alpha;)</i> is a prefix of w &rarr; <i>slink(&alpha;) &isin; Q<sub>w</sub></i>  
If <i>i &ne; |slink(&alpha;)|</i> &rarr; w<sub>i-|slink(&alpha;)|</sub> &ne; a &rarr; <i>slink(&alpha;)</i> appears in two different left contexts &rarr; <i>slink(α) &isin; Q<sub>w</sub></i>  

![alt text](https://github.com/cacao-macao/fun-with-algorithms/blob/master/Suffix-Automaton/img/suffix_links.png)


## CONSTRUCTION IN LINEAR TIME <b><i>O(n)</i></b> ##
The algorithm will be online, i.e. we will add the characters of the string one by one, and modify the automaton accordingly in each step. The whole task boils down to implementing the process of <b>adding one character <i>a</i></b> to the end of the current string <b><i>w</i></b>.  
<b><i>Lemma:</i></b> Let <i>w</i> &isin; &Sigma;* and a &isin; &Sigma;. Then <i>Q<sub>wa</sub> = Q<sub>w</sub> &cup; { [wa]<sub>wa</sub>, [slink(wa)]<sub>wa</sub> }</i>  
<b><i>Proof:</i></b>
  1. <i>Q<sub>w</sub> &cup; { [wa]<sub>wa</sub>, [slink(wa)]<sub>wa</sub> } &sube; Q<sub>wa</sub></i>  
    * Let [&alpha;] &isin; <i>Q<sub>w</sub></i>. Then, either &alpha; is a prefix of <i>w</i> and thus &alpha; is a prefix of <i>wa</i>, or there exist x, y &isin; &Sigma;: x &ne; y & x&alpha;, y&alpha; are infixes of <i>w</i> and thus x&alpha;, y&alpha; are infixes of <i>wa</i> &rarr; [&alpha;] &isin; <i>Q<sub>wa</sub></i>
	* <i>w</i>a is a prefix of <i>w</i>a &rarr; <i>wa &isin; Q<sub>wa</sub></i>
	* <i>slink(wa)</i> is well defined &rarr; <i>slink(wa) &isin; Q<sub>wa</sub></i>
  2. <i>Q<sub>wa</sub> &sube; Q<sub>w</sub> &cup; { [wa]<sub>wa</sub>, [slink(wa)]<sub>wa</sub> }</i>  
  Let &alpha; &isin; &Sigma;* : &alpha; = r(&alpha;) & [&alpha;] &isin; <i>Q<sub>wa</sub>\Q<sub>w</sub></i>  
	* <i>end_pos<sub>w</sub>(&alpha;)</i> = &empty;  
    &alpha; &isin; <i>Q<sub>wa</sub></i> &rarr; <i>end_pos<sub>wa</sub>(&alpha;)</i> &ne; &empty;  
    { 0, 1, 2,..., |w| } &cup; <i>end_pos<sub>wa</sub>(&alpha;)</i> = &empty; &rarr; <i>end_pos<sub>wa</sub>(&alpha;)</i> = { |w|+1 } &rarr; &alpha; &equiv;<sub>wa</sub> <i>wa</i> &rarr; &alpha; = <i>wa</i>
	* <i>end_pos<sub>w</sub>(&alpha;)</i> &ne; &empty;  
    For any &sigma; &isin; &Sigma;*: &sigma; is an infix of <i>w</i>, we have:  
    <i>end_pos<sub>wa</sub>(&sigma;) = end_pos<sub>w</sub>(&sigma;) &cup; { |w| + 1 }</i>, if &sigma; is a suffix of <i>wa</i>  
    <i>end_pos<sub>wa</sub>(&sigma;) = end_pos<sub>w</sub>(&sigma;)</i>, otherwise   
    Let &beta; = [&alpha;]<sub>w</sub> &rarr; <i>end_pos<sub>w</sub>(&beta;) = end_pos<sub>w</sub>(&alpha;)</i>  
    Since &alpha; &notin; <i>Q<sub>w</sub></i> &rarr; &alpha; is a suffix of &beta; &rarr; <i>end_pos<sub>wa</sub>(&beta;) &sube; end_pos<sub>wa</sub>(&alpha;)</i>  
    Since &alpha; &isin; <i>Q<sub>wa</sub></i> &rarr; &alpha; = [&alpha;]<sub>wa</sub> &ne; &beta; &rarr; <i>end_pos<sub>wa</sub>(&beta;) &ne; end_pos<sub>wa</sub>(&alpha;)</i>  
    This implies that <i>end_pos<sub>wa</sub>(&alpha;)\end_pos<sub>wa</sub>(&beta;) = { |w| + 1 }</i> &rarr; &alpha; is a suffix of <i>wa</i> and &beta; is not a suffix of <i>wa</i>  
    Since &alpha; &ne;<sub>wa</sub> <i>wa</i> (because &alpha; = [&alpha;]<sub>wa</sub>), we get that <i>|slink(wa)|</i> &ge; |&alpha;| and &alpha; is a suffix of <i>slink(wa)</i>  
    &rarr; <i>end_pos<sub>wa</sub>(slink(wa)) &sube; end_pos<sub>wa</sub>(&alpha;) &rarr; end_pos<sub>w</sub>(slink(wa)) &sube; end_pos<sub>w</sub>(&alpha;)</i>  
    But <i>end_pos<sub>w</sub>(&alpha;) = end_pos<sub>w</sub>(&beta;)</i> and from <i>Property 1.</i> we get that <i>slink(wa)</i> is a suffix of &beta;  
    &rarr; <i>end_pos<sub>w</sub>(&beta;) &sube; end_pos<sub>w</sub>(slink(wa))</i> (from <i> Property 2.</i>)  
    &rarr; <i>end_pos<sub>w</sub>(&alpha;) &sube; end_pos<sub>w</sub>(slink(wa))</i>  
    &rarr; <i>end_pos<sub>w</sub>(&alpha;) = end_pos<sub>w</sub>(slink(wa))</i>  
    &rarr; <i>end_pos<sub>wa</sub>(&alpha;) = end_pos<sub>wa</sub>(slink(wa))</i>  
    &rarr; [&alpha;]<sub>wa</sub> = <i>[slink(wa)]<sub>wa</sub></i>  

Now let us consider adding a character <i>a</i> to the end of the current string <i>w</i>. We add the new state <i>[wa]<sub>wa</sub></i> but which states have a transition to the new state? Obviously a transition from <i>[w]<sub>w</sub></i> to <i>[wa]<sub>wa</sub></i> with the letter <i>a</i> has to be added to the automaton. Additionally, every suffix <i>w<sub>i</sub></i> of <i>w</i> which represents an equivalence class must have a transition to <i>[wa]<sub>wa</sub></i> with the letter <i>a</i>. In order to do that we traverse the suffix links from <i>[w]<sub>w</sub></i> until we reach <i>s<sub>0</sub></i> and for every state <i>[w<sub>i</sub>]<sub>w</sub></i> that we visit we add a transition with the letter <i>a</i> to the state <i>[wa]<sub>wa</sub></i>. In the end we update the suffix link of <i>wa</i> to be <i>slink(wa) = s<sub>0</sub></i>.  
A special case arises if at some point we visit a state <i>[w<sub>k</sub>]<sub>w</sub></i> that already has a transition with the letter <i>a</i>. This means that <i>w<sub>k</sub></i> is the longest suffix of <i>w</i> that when extended with the letter <i>a</i> appears as a proper infix (or prefix) of <i>wa</i>. It also implies that after extending <i>w</i> with <i>a</i> the string <i>w<sub>k</sub> • a</i> occurs in two distinct left contexts &harr; <b><i>slink([wa]<sub>wa</sub>) = [w<sub>k</sub> • a]<sub>wa</sub></i></b>  
The last statement follows from the following: Suppose <i>slink(wa) = &alpha;a</i> and <i>|&alpha;a| > |w<sub>k</sub> • a|</i>. This means that <i>&alpha;a</i>, and equivalently &alpha;, occurs in two distinct left contexts with <i>|&alpha;| > |w<sub>k</sub>|</i> and <i>[&alpha;]<sub>w</sub></i> has a transition with the letter <i>a</i> - contradiction with the fact that <i>[w<sub>k</sub>]<sub>w</sub></i> is the first state that has a transition with the letter <i>a</i>.

<pre>
FindStem(q<sub>w</sub>, q<sub>wa</sub>, a) {
	q = q<sub>w</sub>
	while (q is defined && &delta;(q, a) is not defined):
		&delkta;(q, a) = q<sub>wa</sub>
		q = slink(q)
	return q
}
</pre>

Suppose &delta;<sub>w</sub>(w<sub>k</sub>, a) = &beta;. We have to consider two cases:
  * &beta; = [w<sub>k</sub> • a]<sub>w</sub>  
  In this case we can simply assign <i>slink([wa]<sub>wa</sub>)</i> = [w<sub>k</sub> • a]<sub>wa</sub>
  * &beta; &ne; [w<sub>k</sub> • a]<sub>w</sub>  
  In this case, since after extending <i>w</i> with the letter <i>a</i> the string <i>w<sub>k</sub> • a</i> occurs in two distinct left contexts, a new state, [w<sub>k</sub> • a]<sub>wa</sub>, has to be created. All transitions of state [&beta;]<sub>w</sub> have to be copied to the new state [w<sub>k</sub> • a]<sub>wa</sub>. For any transition <i>x &ne; a</i> of state [&beta;]<sub>w</sub> we have the following:  
  <i>end_pos<sub>wa</sub>([&beta;x]<sub>wa</sub>) = end_pos<sub>wa</sub>(&beta;x) = end_pos<sub>wa</sub>(&alpha;x) = end_pos([&alpha;x]<sub>wa</sub>)</i>  
  The creation of a new state also requires updating the suffix link chain. Since <i>slink([wa]<sub>wa</sub>) = [w<sub>k</sub> • a]<sub>wa</sub></i>, this implies that &beta; is not a suffix of <i>wa</i>. Suppose &beta; = x • w<sub>k</sub> • a, x &isin; &Sigma;* and suppose that <i>slink([&beta;]<sub>w</sub>) = &sigma;</i>. We have the following:  
  <i>end_pos<sub>wa</sub>(w<sub>k</sub> • a) = end_pos<sub>w</sub>(w<sub>k</sub> • a) &cup; { |w| + 1 } = end_pos<sub>w</sub>(&beta;) &cup; {|w| + 1} = end_pos<sub>wa</sub>(&beta;) U {|w| + 1}</i>  
  <i>end_pos<sub>w</sub>(&sigma;) &sub; end_pos<sub>w</sub>(&beta;) = end_pos<sub>w</sub>(w<sub>k</sub> • a) &rarr; end_pos<sub>wa</sub>(&sigma;) &sub; end_pos<sub>wa</sub>(w<sub>k</sub> • a)</i>  
  From this we can conclude that the following update has to be made to the suffix chain:  
  <i>slink([w<sub>k</sub> • a]<sub>wa</sub>) = slink([&beta;]<sub>w</sub>)</i> and <i>slink([&beta;]<sub>wa</sub>) = [w<sub>k</sub> • a]<sub>wa</sub></i>  
  Finally we need to follow the suffix chain from [w<sub>k</sub>]<sub>w</sub> all the way up to <i>s<sub>0</sub></i> and whenever there is a transition with the letter <i>a</i> to state [&beta;]<sub>w</sub> we have to redirect it to state [w<sub>k</sub> • a]<sub>wa</sub>. To see why this is the case consider a state [&alpha;]<sub>w</sub>:  
  &delta;<sub>w</sub>(&alpha;, a) = &beta;. The string &alpha;a is a suffix of all the strings that belong to the equivalence class [&beta;]<sub>w</sub> and in particular &alpha;a is a suffix of <i>w<sub>k</sub> • a</i>. This implies <i>end_pos<sub>w</sub>(&alpha;a) = end_pos<sub>w</sub>(w<sub>k</sub> • a)</i>. After extending <i>w</i> with the letter <i>a</i> we have <i>end_pos<sub>wa</sub>(&alpha;a) = end_pos<sub>w</sub>(&alpha;a) &cup; {|w| + 1} = end_pos<sub>wa</sub>(w<sub>k</sub> • a)</i> and thus &delta;<sub>wa</sub>(&alpha;, a) = <i>w<sub>k</sub> • a</i>  
  <b><i>Lemma:</i></b> No other transitions need to be modified.  

<pre>
ModifyTree(p, q<sub>wa</sub>, a) { // p is the result from the function FindStem
	if p is not defined:
		slink(q<sub>wa</sub>) = s<sub>0</sub>
		return NULL
	suf = &delta;(p, a)
	if (len(suf) == len(p) + 1):	// suf represents the class [suf]<sub>w</sub>
		slink(q<sub>wa</sub>) = suf
		return NULL
	clone = new State
	len(clone) = len(p) + 1
	CopyTransitions(suf, clone)

	slink(clone) = slink(suf)
	slink(suf) = clone
	slink(q<sub>wa</sub>) = clone
	return clone
}
</pre>

<pre>
CopyTransitions(source, dest) {
	for a &isin; &Sigma;: &delta;(source, a) is defined:
		&delta;(dest, a) = &delta;(source, a)
}
</pre>

<pre>
RedirectTransitions(p, clone ,a) {
	if p is not defined || clone is not defined:
		return
	suf = &delta;(p, a)
	while p is defined && &delta;(p, a) = suf:
		&delta;(p, a) = clone
		p = slink(p)
}
</pre>

As stated, building the suffix automaton requires adding the characters one by one and modifying the automaton accordingly in each step.
After constructing the complete suffix automaton for the entire string <i>w</i> we need to mark all terminal states. The only accpeting states are those equivalence classes that include suffixes of <i>w</i>. To do this, we take the state corresponding the entire string and follow its suffix links until we reach the initial state. We mark all visited states as terminal.

<pre>
BuildSuffixAutomaton(w) {
	s<sub>0</sub> = new State
	len(s<sub>0</sub>) = 0
	q = s<sub>0</sub>
	
	for i = 1 to |w| do:
		q<sub>wa</sub> = new State
		len(q<sub>wa</sub>) = i
		p = FindStem(q, q<sub>wa</sub>, w[i])
		clone = ModifyTree(p, q<sub>wa</sub>, w[i])
		RedirectTransitions(p, clone, w[i])
		q = q<sub>wa</sub>

	while q is defined:
		mark q as final
		q = slink(q)
}
</pre>


## COMPLEXITY ##

### Linearity of the number of states ###
To show that the number of states of the automaton is <b><i>O(n)</i></b> we will use the following statement:  
<b><i>Lemma:</i></b> Let <i>Φ</i> be a set of subsets of the set <i>{1, 2, ..., n}</i>. For every <i>S<sub>1</sub> , S<sub>2</sub> &isin; Φ</i> we have either <i>S<sub>1</sub> &cap; S<sub>2</sub> = &empty;</i> or <i>S<sub>1</sub> &sub; S<sub>2</sub> and S<sub>1</sub> &ne; S<sub>2</sub></i> . Then <i>|Φ| ≤ 2n</i>.  
<b><i>Proof:</i></b> Let <i>Φ' = Φ U {1, 2, ..., n}</i> and let <i>S = Φ \ {{&empty;}, {1, 2, ..., n}}</i>. Then there exists <i>S' &sub; Φ': S &sub; S'</i>. Denote by <i>p(S)</i> the smallest set such that: <i>S &sub; p(S)</i> and <i>S &ne; p(S)</i>. In a sense <i>p(S)</i> is the parent of <i>S</i>, it exists and it is unique.  
It follows that <i>(Φ' \ {&empty;}, p, {1, 2, ..., n})</i> is a rooted tree with root <i>{1, 2, ..., n}</i>, parent fuction <i>p</i> and set of states <i>Q = Φ' \ {&emtpy;}</i>. We will use the following notation:  
<i>L = {S &sub; Φ' \ {&empty;} | S doesn't have any children}</i> is the set of leafs  
<i>V<sup>1</sup> = {S &sub; Φ' \ {&empty;} | S has only one child}</i>  
<i>V<sup>≥2</sup> = {S &sub; Φ' \ {&empty;} | S has more than one child} = Φ' \ {{&empty;}, L, V<sup>1</sup>}</i>  
The number of edges in the tree is <i>|E| = |Φ' \ {&empty;}| - 1</i>. On the other hand we have:  
<i>
|E| = &sum;<sub>v &isin; Q</sub>(# of children of v) = &sum;<sub>v &isin; L</sub>(# of children of v) + &sum;<sub>v &isin; V<sup>1</sup></sub>(# of children of v) + &sum;<sub>v &isin; V<sup>≥2</sup></sub>(# of children of v)  
&rarr; |E| ≥ 0 + |V<sup>1</sup>| + 2|V<sup>≥2</sup>|  
&rarr; |Φ' \ {&empty;}| - 1 &ge; |V<sup>1</sup>| + 2|V<sup>≥2</sup>|  
&harr; |L| + |V<sup>1</sup>| + |V<sup>≥2</sup>| - 1 &ge; |V<sup>1</sup>| + 2|V<sup>≥2</sup>|  
&harr; |L| - 1 &ge; |V<sup>≥2</sup>|  
&rarr; |Φ' \ {&empty;}| &le; |L| + |V<sup>1</sup>| + |L| - 1 &le; 2(|L| + |V<sup>1</sup>|) - 1   
</i>

We will use the following strategy to find the cardinality of each of the sets <i>L</i> and <i>V<sup>1</sup></i>:
  * For every <i>S &sub; L</i> we pick an arbitrary element <i>f(S) &isin; S</i> to represent the set  
  For any <i>S<sub>1</sub> , S<sub>2</sub> &sub; L</i> we have <i>S<sub>1</sub> &cap; S<sub>2</sub> = &empty; → f(S<sub>1</sub>) &ne; f(S<sub>2</sub>)</i>
  * For every <i>S &sub; V<sup>1</sup></i> let <i>child(S)</i> denote the only child of <i>S</i>. We pick an arbitrary element <i>f(S) &isin; S \ child(S)</i>  
  Suppose <i>f(S<sub>1</sub>) = f(S<sub>2</sub>)</i> for some <i>S<sub>1</sub></i> and <i>S<sub>2</sub></i>.
  If <i>S<sub>2</sub> &sub; L</i> then, since  S<sub>1</sub> &cap; S<sub>2</sub> &ne; &empty;, <i>S<sub>2</sub></i> must be in the subtree of <i>S<sub>1</sub> &rarr; S<sub>2</sub> &sub; child(S<sub>1</sub>) &rarr; f(S<sub>1</sub>) &isin; child(S<sub>1</sub>)</i> - contradiction.
  If <i>S<sub>2</sub> &sub; V<sup>1</sup></i> again since S<sub>1</sub> &cap; S<sub>2</sub> &ne; &empty; one of the sets must be in the subtree of the other, implying <i>f(S<sub>1</sub>) &isin; child(S<sub>1</sub>)</i> or <i>f(S<sub>2</sub>) &isin; child(S<sub>2</sub>)</i> and leading to contradiction.  

<i></i>
It follows that <i>f: {L &cup; V<sup>1</sup>} &rarr; {1, 2, ..., n}</i> is an injective function &rarr; <i>|L &cup; V<sup>1</sup>| &le; n</i>  
&rarr; <i>|Φ' \ {&empty;}| &le; 2(|L| + |V<sup>1</sup>|) - 1 &le; 2n - 1</i>  
&rarr; <i>|Φ'| &le; 2n</i>  

<b><i>Corollary:</i></b> The number of states of the suffix automaton for the string <i>w</i> is at most <i>2|w|</i>.  
<b><i>Proof:</i></b> The number of states of the automaton is equal to the equivalence classes in the relation <i>R<sub>Suffix(w)</sub></i> which is equivalent to the end-equivalence relation <i>&equiv;<sub>w</sub></i>  
&alpha; &equiv;<sub>w</sub> &beta; &rarr; <i>end_pos<sub>w</sub>(&alpha;) = end_pos<sub>w</sub>(&beta;)</i>  
The equivalence classes in the end-equivalence relation satisfy the preconditions of the previous Lemma. This implies that <i>ind(&equiv;<sub>w</sub>) &le; 2|w|</i>  

### Linearity of the number of transitions ###
We will show that the number of transitions of the suffix automaton for the string <i>w</i> does not exceed <b><i>3|w|</i></b>. Let &alpha; &isin; <i>Q<sub>w</sub></i> , |&alpha;| ≥ 1, then it follows that &alpha; = &beta;a, for some &beta; &isin; &Sigma;* and <i>a</i> &isin; &Sigma;, and &beta; &isin; <i>Q<sub>w</sub></i>. Indeed, if &alpha; is a prefix of <i>w</i> then &beta; is also a prefix of <i>w</i>. And if &alpha; occurs in two distinct left contexts then &beta; also occurs in two distinct left contexts. Let us denote by <i>p(&alpha;) = &beta;</i> the parrent of &alpha;, then <i>T = (Q<sub>w</sub>, p, s<sub>0</sub>)</i> forms a rooted tree. The tree <i>T</i> is a spannig tree of the automaton and consists of <i>|Q<sub>w</sub> - 1|</i> transitions.  

Now let <i>S<sub>w</sub> = { <&beta;, a, &alpha;> | &delta;<sub>w</sub>(&beta;, a) = &alpha; and p(&alpha;) &ne; &beta; }</i> denote the set of all the remaining transitions. For every &alpha; &isin; <i>Q<sub>w</sub></i> denote by &sigma;(&alpha;) the longest string such that &alpha;•&sigma;(&alpha;) is a suffix of <i>w</i>. Then for every element of the set <i>S<sub>w</sub></i> the string &beta;•a•&sigma;(&alpha;) corresponds to a unique suffix of the string <i>w</i>. Indeed, suppose <&beta;<sub>1</sub>, a<sub>1</sub>, &alpha;<sub>1</sub>>, <&beta;<sub>2</sub>, a<sub>2</sub>, &alpha;<sub>2</sub>> &isin; <i>S<sub>w</sub></i> and &beta;<sub>1</sub>•a<sub>1</sub>•&sigma;(&alpha;<sub>1</sub>) = &beta;<sub>2</sub>•a<sub>2</sub>•&sigma;(&alpha;<sub>2</sub>). Then &beta;<sub>1</sub>•a<sub>1</sub> is a prefix of &beta;<sub>2</sub>•a<sub>2</sub> or &beta;<sub>2</sub>•a<sub>2</sub> is a prefix of &beta;<sub>1</sub>•a<sub>1</sub>. WLOG we can assume that &beta;<sub>1</sub>•a<sub>1</sub> is a prefix of &beta;<sub>2</sub>•a<sub>2</sub>. Then &beta;<sub>1</sub>•a<sub>1</sub> &ne; &beta;<sub>2</sub>•a<sub>2</sub> otherwise <&beta;<sub>1</sub>, a<sub>1</sub>, &alpha;<sub>1</sub>> = <&beta;<sub>2</sub>, a<sub>2</sub>, &alpha;<sub>2</sub>>. This means that &beta;<sub>1</sub>•a<sub>1</sub> is a a proper prefix of &beta;<sub>2</sub>•a<sub>2</sub>, implying that &beta;<sub>1</sub>•a<sub>1</sub> is an ancestor of &beta;<sub>2</sub> in <i>T<sub>w</sub></i>. This means that <i>p(&beta;<sub>2</sub>) = &beta;<sub>1</sub></i> and that <&beta;<sub>1</sub>, a<sub>1</sub>, &alpha;<sub>1</sub>> &notin; <i>S<sub>w</sub></i> - contradiction.  
This implies that <i>|S<sub>w</sub>| &le; |w|</i> and we get <i>|&delta;<sub>w</sub>| = |Q<sub>w</sub>| - 1 + |S<sub>w</sub>| &le; 2|w| + |w| = 3|w|</i>.

### Linearity of the algorithm ###
Consider the for-loop that builds the suffix automaton. We have the following actions:
  * adding a new state
  * adding new transitions insidue function <i>FindStem</i>
  * adding new transitions and new states inside function <i>ModifyTree</i>
  * modifying existing transitions inside function <i>RedirectTransitions</i>

Since the total number of states is <i>Q<sub>w</sub> &le; 2|w|</i> and the total number of transitions is |&delta;<sub>w</sub>| ≤ 3|<i>w</i>|, then the total number of steps for executing the first three actions is <i>O(|w|)</i>. It remains to show that the total number of modifications of the existing transitions is <i>O(|w|)</i>.  

Let <i>SC<sub>w</sub>(&alpha;) = { slink<sup>k</sup>(&alpha;) | k is an ineger }</i> be the set of all suffix pointers traversed starting at the state [&alpha;]<sub>w</sub>.  

<b><i>Lemma:</i></b> After extending the string <i>w</i> with the letter <i>a</i> the number of modifications of existing transitions does not exceed <i>1 + |SC<sub>w</sub>(w)| - |SC<sub>wa</sub>(wa)|</i>.  
<b><i>Proof:</i></b> The function <i>RedirectTransitions</i> modifies the transition of state <i>[w<sub>k</sub>]<sub>w</sub></i>. It also modifies the transitions of all states &alpha; such that &alpha; &isin; <i>SC<sub>w</sub>(w<sub>k</sub>)</i> and &delta;<sub>w</sub>(&alpha;, a) = [w<sub>k</sub> • a]<sub>w</sub>. This means that &alpha; &notin; <i>SC<sub>wa</sub>(wa)</i>. In other words the function modifies the transitions of all states &alpha; such that &alpha; &isin; <i>SC<sub>w</sub>(w<sub>k</sub>)</i> and &alpha; &notin; <i>SC<sub>wa</sub>(wa)</i>. This implies that the number of modifications is:  
<i>1 + |{ &alpha; &isin; SC<sub>w</sub>(w<sub>k</sub>) | &alpha; &notin; SC<sub>wa</sub>(wa) }| = 1 + |SC<sub>w</sub>(w<sub>k</sub>)| - |SC<sub>wa</sub>(wa)| &le; 1 + |SC<sub>w</sub>(w)| - |SC<sub>wa</sub>(wa)|  

Thus, the total number of modifications of existing transitions is:  
<i>&sum;<sub>0 ≤ i < |w|</sub> (1 + |SC<sub>w<sub>i</sub></sub>(w<sub>i</sub>)| - |SC<sub>w<sub>i + 1</sub></sub>(w<sub>i + 1</sub>)| = |w| + |SC<sub>w<sub>0</sub></sub>(w<sub>0</sub>)| - |SC<sub>w</sub>(w)| &le; |w| + 1 &in; O(|w|)</i>