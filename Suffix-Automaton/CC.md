# Correctness and Complexity

## Introduction ##
A suffix automaton for a given string <i>w</i> is a minimal <b>DFA</b> (deterministic finite automaton) that accepts all the suffixes of the string <i>w</i>. For a string of length <b>n</b> it only requires <b><i>O(n)</i></b> memory and it can also be built in <b><i>O(n)</i></b> time. The algorithm was discovered in 1983 by <i>Blumer, Blumer, Haussler, Ehrenfeucht, Chen and Seiferas</i> and was presented in their paper <i>The smallest automaton recognizing the subwords of a text</i>. An important property of a suffix automaton is, that it contains information about all substrings of the string <i>w</i>. This is due to the following theorem:  
<i>Given two strings w and x, <b>x is a substring of w</b> if and only if <b>x is a prefix of a suffix of w</b>.</i>  
Any path starting at the initial state <b><i>s<sub>0</sub></i></b> forms a substring of <i>w</i>. And conversely every substring of <i>w</i> corresponds to a certain path starting at <b><i>s<sub>0</sub></i></b>.

## Notation ##
<i>Σ</i> - nonempty alphabet  
<i>ε</i> - the empty word  
<i>Σ*</i> - the set of all words over <i>Σ</i>  
<i>Suffix(w) = { ß c Σ* | exists α: αß = w }</i>  
  
A suffix automaton is a minimal DFA over the language <i>L = Suffix(w)</i>. From Nerode's theorem it follows that the number of states of the minimal DFA is equal to the number of equivalence classes in the relation <i>R<sub>L</sub></i>, where:  
<i>{α, ß} c R<sub>L</sub> (α ≡<sub>L</sub> ß) ↔ for every z c Σ*: αz c L ↔ ßz c L</i>  

### End positions <b><i>end_pos</b></i> ###
Let <i>w</i> = a<sub>1</sub>a<sub>2</sub>...a<sub>n</sub> <i>(a<sub>i</sub> ε Σ)</i> and <i>α ╪ ε c Σ*</i>  
define: <i><b>end_pos<sub>w</sub>(α)</b> = { i | α = a<sub>i-|α|+1</sub>...a<sub>i</sub> }</i>  
<i>end_pos<sub>w</sub>(α)</i> is the set of all positions in the string <i>w</i>, in which the occurrences of <i>α</i> end  
<i>end_pos<sub>w</sub>(ε) = { 0, 1, 2, ..., |w| }</i>

two strings <i>α, ß c Σ*</i> are <b>end-equivalent on w</b> if and only if <i>end_pos<sub>w</sub>(α) = end_pos<sub>w</sub>(ß)</i>  
end-equivalence will be denoted by <i>≡<sub>w</sub></i> , i.e. <i>α ≡<sub>w</sub> ß ↔ end_pos<sub>w</sub>(α) = end_pos<sub>w</sub>(ß)</i>  

<b><i>Example:</b></i>
<pre>	<i>w = a b c b c</i>  
	<i>   0 1 2 3 4 5</i>  
    	<i>end_pos<sub>w</sub>(bc) = end_pos<sub>w</sub>(c) = {3, 5}</i>  
    	<i>bc ≡<sub>w</sub> c</i></pre>  

<b><i>Corollary:</i></b> The end-equivalence relation is equivalent to Nerode's relation <i>R<sub>L</sub></i> for the language <i>L = Suffix(w)</i>:  
<i>α ≡<sub>w</sub> ß ↔ α ≡<sub>Suffix(w)</sub> ß</i>  
<b><i>Proof:</i></b> Let <i>w = a<sub>1</sub>a<sub>2</sub>...a<sub>n</sub> (a<sub>i</sub> ε Σ) and α, ß, z c Σ*</i>. Then <i>αz c Suffix(w) ↔ αz = a<sub>n-|αz|+1</sub>...a<sub>n</sub>  
→ α = a<sub>n-|αz|+1</sub>...a<sub>n-|z|</sub> and z = a<sub>n-|z|+1</sub>...a<sub>n</sub>  
→ α = a<sub>i-|α|+1</sub>...a<sub>i</sub> and i = n - |z|</i>  
But <i> α ≡<sub>Suffix(w)</sub> ß ↔ for every z c Σ*: αz c Suffix(w) ↔ ßz c Suffix(w)  
↔ for every i: α = a<sub>i-|α|+1</sub>...a<sub>i</sub> ↔ ß = a<sub>i-|ß|+1</sub>...a<sub>i</sub>  
↔ end_pos<sub>w</sub>(α) = end_pos<sub>w</sub>(ß)</i>

<b><i>Properties:</i></b>  
Let <i>α, ß c Σ*</i> be subwords of <i>w</i> with |α| ≤ |ß|, then:
1. end_pos<sub>w</sub>(α) ∩ end_pos<sub>w</sub>(ß) ╪ Ø → α is a suffix of ß
2. α is a suffix of ß → end_pos<sub>w</sub>(ß) c end_pos<sub>w</sub>(α)
3. We have either end_pos<sub>w</sub>(α) c end_pos<sub>w</sub>(ß) or end_pos<sub>w</sub>(α) ∩ end_pos<sub>w</sub>(ß) = Ø

### Equivalence classes <b><i>[α]<sub>w</sub></i></b> and Representatives <b><i>r(α)</i></b> ###
Let α be an infix of <i>w</i>. Denote by <i>[α]<sub>w</sub></i> the equivalence class of α with respect to the relation ≡<sub>w</sub> and denote by <b><i>r(α)</i></b> the longest word in the equivalence class <i>[α]<sub>w</sub></i>. We say that <i>r(α)</i> canonically represents the equivalence class <i>[α]<sub>w</sub></i>  
By definition <i>r(ε) = ε</i> 
<p></p>  

<b><i>Lemma:</i></b>  
Let α be an infix of <i>w</i>, then:  
1. If there is a letter a c Σ, such that every occurance of α in w is preceeded by a, then α does not represent the equivalence class [α]<sub>w</sub>
2. If α is a prefix of w, then α is the longest word in [α]<sub>w</sub>
3. If there are letters x, y c Σ, x ╪ y and both xα and yα are infixes of w, then α canonically represents the equivalence class [α]<sub>w</sub>  
4. α = r(α) ↔ α is a prefix of w or it occurs in two distinct left contexts

<b><i>Proof:</i></b>
1. Let a preceed every occurance of α in w. Then for every i c end_pos(α) we have w<sub>i-|α|</sub> = a  
→ i c end_pos(aα)  
→ end_pos(α) c end_pos(aα)  
And since α is a suffix of aα we have that end_pos(aα) c end_pos(α) (by Property 2.)  
→ end_pos(α) = end_pos(aα)  
It follows that α ≡<sub>w</sub> aα and |α| < |aα| → α ╪ r(α)
2. Let |α| = i. Since α is a prefix of w we have α = a<sub>1</sub>...a<sub>i</sub> and i c end_pos(α).  
Suppose ß ≡<sub>w</sub> α → i c end_pos(ß) → |ß| ≤ |a<sub>1</sub>...a<sub>i</sub>| = i = |α|
3. Let x, y c Σ, x ╪ y and both xα and yα are infixes of w. Let i and j be such that:  
i c end_pos(xα)  
j c end_pos(yα)  
Since α is a suffix of both xα and yα we have that i, j c end_pos(α)
Let ß ≡<sub>w</sub> α, then i, j c end_pos(ß). Assume |ß| > |α| → |ß| ≥ |α| + 1 = |xα| = |yα|  
→ xα is a suffix of ß and yα is a suffix of ß → x = y - contradiction  

### Suffix links <b><i>slink</i></b> ###
The automaton <i>A<sub>w</sub> ( Σ, Q<sub>w</sub>, s<sub>0</sub>, F<sub>w</sub>, δ<sub>w</sub>)</i> with:  
<i>Q<sub>w</sub> = { r(α) | α is an infix of w }</i>  
<i>δ<sub>w</sub>(α, a) = r(αa), if αa is an infix of w</i>  
<i>F<sub>w</sub> = { α c Q<sub>w</sub> | α is a suffix of w }</i>  
is a minimal DFA over the language L = Suffix(w).  
The states of the automaton are exactly the equivalence classes with respect to the relation ≡<sub>w</sub>  
For each state we will store the length of the longest word in the equivalence class: <b><i>len([α]<sub>w</sub>) = |r(α)|</i></b>  
For each state we will also store a pointer called a <b><i>suffix link</i></b> that points to the longest suffix of w that is in another equivalence class: <b><i>slink(α)</i></b> is the longest suffix of α: <i>slink(α) ╪<sub>w</sub> α</i>  

<b><i>Lemma:</b></i> <i>( Q<sub>w</sub> , slink, s<sub>0</sub> ) is a rooted tree.</i>  
<b><i>Proof:</b></i> We only need to show that <i>slink(α) c Q<sub>w</sub></i>. Since <i>slink(α)</i> is a suffix of α from Property 2. we have that <i>end_pos(α) c end_pos(slink(α))</i>. And since <i>α ╪ slink(α)</i>, we have that <i>end_pos(α) ╪ end_pos(slink(α))</i>.  
Let <i>α = x•a•slink(α), x c Σ*, a c Σ</i> and let <i>i c end_pos(slink(α))\end_pos(α)</i>.  
If <i>i = |slink(α)|</i> → <i>slink(α)</i> is a prefix of w → <i>slink(α) c Q<sub>w</sub></i>  
If <i>i ╪ |slink(α)|</i> → <i>w<sub>i-|slink(α)|</sub> ╪ a</i> → <i>slink(α)</i> appears in two different left contexts → <i>slink(α) c Q<sub>w</sub></i>  

![alt text](https://github.com/ThreeChuchura/fun-with-algorithms/blob/master/Suffix-Automaton/img/suffix_links.png)

## Construction in linear time <b>O(n)</b> ##
The algorithm will be online, i.e. we will add the characters of the string one by one, and modify the automaton accordingly in each step. The whole task boils down to implementing the process of <b>adding one character <i>a</i></b> to the end of the current string <b><i>w</i></b>.  
<b><i>Lemma:</i></b> Let <i>w c Σ*</i> and <i>a c Σ</i>. Then <i>Q<sub>wa</sub> = Q<sub>w</sub> U { [wa]<sub>wa</sub>, [slink(wa)]<sub>wa</sub> }</i>  
<b><i>Proof:</i></b>
1. <i>Q<sub>w</sub> U { [wa]<sub>wa</sub>, [slink(wa)]<sub>wa</sub> } c Q<sub>wa</sub></i>
	* Let [α] c Q<sub>w</sub>: then either α is a prefix of w → α is a prefix of wa, or there exist x, y c Σ, x ╪ y and xα, yα are infixes of w → xα, yα are infixes of wa
	* wa is a prefix of wa → wa c Q<sub>wa</sub>
	* slink(wa) is well defined → slink(wa) c Q<sub>wa</sub>
2. <i>Q<sub>wa</sub> c Q<sub>w</sub> U { [wa]<sub>wa</sub>, [slink(wa)]<sub>wa</sub> }</i>  
Let <i>α c Σ*: α = r(α)</i> and <i>[a] c Q<sub>wa</sub>\Q<sub>w</sub></i>
	* <i>end_pos<sub>w</sub>(α) = Ø</i>  
<i>α c Q<sub>wa</sub> → end_pos<sub>wa</sub>(α) ╪ Ø</i>  
<i>{ 0, 1, 2,..., |w| } ∩ end_pos<sub>wa</sub>(α) = Ø → end_pos<sub>wa</sub>(α) = { |w|+1 } → α ≡<sub>wa</sub> wa → α = wa</i>
	* <i>end_pos<sub>w</sub>(α) ╪ Ø</i>  
For any <i>σ c Σ*</i>: σ is an infix of <i>w</i>, we have:  
<i>end_pos<sub>wa</sub>(σ) = end_pos<sub>w</sub>(σ) U { |w| + 1 }</i>, if σ is a suffix of <i>wa</i>  
<i>end_pos<sub>wa</sub>(σ) = end_pos<sub>w</sub>(σ)</i>, otherwise   
Let <i>ß = [α]<sub>w</sub> → end_pos<sub>w</sub>(ß) = end_pos<sub>w</sub>(α)</i>  
Since <i>α ¢ Q<sub>w</sub> → α is a suffix of ß → end_pos<sub>wa</sub>(ß) c end_pos<sub>wa</sub>(α)</i>  
Since <i>α c Q<sub>wa</sub> → α = [α]<sub>wa</sub> ╪ ß → end_pos<sub>wa</sub>(ß) ╪ end_pos<sub>wa</sub>(α)</i>  
This implies that <i>end_pos<sub>wa</sub>(α)\end_pos<sub>wa</sub>(ß) = { |w| + 1 }</i> → α is a suffix of wa and ß is not a suffix of wa  
Since <i>α ╪<sub>wa</sub> wa</i>, we get that <i>|slink(wa)| ≥ |α|</i> and α is a suffix of <i>slink(wa)</i>  
<i>→end_pos<sub>wa</sub>(slink(wa)) c end_pos<sub>wa</sub>(α) → end_pos<sub>w</sub>(slink(wa)) c end_pos<sub>w</sub>(α)</i>  
and from Property 2. we get <i>end_pos<sub>w</sub>(α) c end_pos<sub>w</sub>(slink(wa))</i>  
<i>→ end_pos<sub>w</sub>(slink(wa)) = end_pos<sub>w</sub>(α) → end_pos<sub>wa</sub>(slink(wa)) = end_pos<sub>wa</sub>(α) → [α]<sub>wa</sub> = [slink(wa)]<sub>wa</sub></i>  

Now let us consider adding a character <i>a</i> to the end of the current string <i>w</i>. We add the new state <i>[wa]<sub>wa</sub></i> but which states have a transition to the new state? Obviously a transition from <i>[w]<sub>w</sub></i> to <i>[wa]<sub>wa</sub></i> with the letter <i>a</i> has to be added to the automaton. Additionally, every suffix <i>w<sub>i</sub></i> of <i>w</i> which represents an equivalence class must have a transition to <i>[wa]<sub>wa</sub></i> with the letter <i>a</i>. In order to do that we traverse the suffix links from <i>[w]<sub>w</sub></i> until we reach <i>s<sub>0</sub></i> and for every state <i>[w<sub>i</sub>]<sub>w</sub></i> that we visit we add a transition with the letter <i>a</i> to the state <i>[wa]<sub>wa</sub></i>. In the end we update the suffix link of <i>wa</i> to be <i>slink(wa) = s<sub>0</sub></i>.  
A special case arises if at some point we visit a state <i>[w<sub>k</sub>]<sub>w</sub></i> that already has a transition with the letter <i>a</i>. This means that <i>w<sub>k</sub></i> is the longest suffix of <i>w</i> that when extended with the letter <i>a</i> appears as a proper infix (or prefix) of <i>wa</i>. It also implies that after extending <i>w</i> with <i>a</i> the string <i>w<sub>k</sub> • a</i> occurs in two distinct left contexts → <b><i>slink([wa]<sub>wa</sub>) = [w<sub>k</sub> • a]<sub>wa</sub></i></b>  
The last statement follows from the following: Suppose <i>slink(wa) = αa</i> and <i>|αa| > |w<sub>k</sub> • a|</i>. This means that <i>αa</i>, and equivalently <i>α</i>, occurs in two distinct left contexts with <i>|α| > |w<sub>k</sub>|</i> and <i>[α]<sub>w</sub></i> has a transition with the letter <i>a</i> - contradiction.

<pre>
FindStem(q<sub>w</sub>, q<sub>wa</sub>, a) {
	q = q<sub>w</sub>
	while (q is defined && δ(q, a) is not defined):
		δ(q, a) = q<sub>wa</sub>
		q = slink(q)
	return q
}
</pre>

Suppose <i>δ<sub>w</sub>(w<sub>k</sub>, a) = ß</i>. We have to consider two cases:
* <i>ß = [w<sub>k</sub> • a]<sub>w</sub></i>  
In this case we can simply assign <i>slink([wa]<sub>wa</sub>) = [w<sub>k</sub> • a]<sub>wa</sub></i>
* <i>ß ╪ [w<sub>k</sub> • a]<sub>w</sub></i>  
In this case, since after extending <i>w</i> with the letter <i>a</i> the string <i>w<sub>k</sub> • a</i> occurs in two distinct left contexts, a new state, <i>[w<sub>k</sub> • a]<sub>wa</sub></i>, has to be created. All transitions of state <i>[ß]<sub>w</sub></i> have to be copied to the new state <i>[w<sub>k</sub> • a]<sub>wa</sub></i>. For any transition <i>x ╪ a</i> of state <i>[ß]<sub>w</sub></i> we have the following:  
<i>end_pos<sub>wa</sub>([ßx]<sub>wa</sub>) = end_pos<sub>wa</sub>(ßx) = end_pos<sub>wa</sub>(αx) = end_pos([αx]<sub>wa</sub>)</i>  
The creation of a new state also requires updating the suffix link chain. Since <i>slink([wa]<sub>wa</sub>) = [w<sub>k</sub> • a]<sub>wa</sub></i>, this implies that ß is not a suffix of <i>wa</i>. Suppose <i>ß = x • w<sub>k</sub> • a, x c Σ*</i> and suppose that <i>slink([ß]<sub>w</sub>) = σ</i>. We have the following:  
<i>end_pos<sub>wa</sub>(w<sub>k</sub> • a) = end_pos<sub>w</sub>(w<sub>k</sub> • a) U { |w| + 1 } = end_pos<sub>w</sub>(ß) U {|w| + 1} = end_pos<sub>wa</sub>(ß) U {|w| + 1}</i>  
<i>end_pos<sub>w</sub>(σ) c end_pos<sub>w</sub>(ß) = end_pos<sub>w</sub>(w<sub>k</sub> • a) → end_pos<sub>wa</sub>(σ) c end_pos<sub>wa</sub>(w<sub>k</sub> • a)</i>  
From this we can conclude that the following update has to be made to the suffix chain:  
<i>slink([w<sub>k</sub> • a]<sub>wa</sub>) = slink([ß]<sub>w</sub>)</i> and <i>slink([ß]<sub>wa</sub>) = [w<sub>k</sub> • a]<sub>wa</sub></i>  
Finally we need to follow the suffix chain from <i>[w<sub>k</sub>]<sub>w</sub></i> all the way up to <i>s<sub>0</sub></i> and whenever there is a transition with the letter <i>a</i> to state <i>[ß]<sub>w</sub></i> we have to redirect it to state <i>[w<sub>k</sub> • a]<sub>wa</sub></i>. To see why this is the case consider a state <i>[α]<sub>w</sub> :  
δ<sub>w</sub>(α, a) = ß</i>. The string α is a suffix of all the strings that belong to the equivalence class [ß]<sub>w</sub> and in particular α is a suffix of <i>w<sub>k</sub> • a</i>. This implies <i>end_pos<sub>w</sub>(αa) = end_pos<sub>w</sub>(w<sub>k</sub> • a)</i>. After extending <i>w</i> with the letter <i>a</i> we have <i>end_pos<sub>wa</sub>(αa) = end_pos<sub>w</sub>(αa) U {|w| + 1} = end_pos<sub>wa</sub>(w<sub>k</sub> • a)</i> and thus <i>δ<sub>wa</sub>(α, a) = w<sub>k</sub> • a</i>  
<b><i>Lemma:</i></b> No other transitions need to be modified.  

<pre>
ModifyTree(p, q<sub>wa</sub>, a) { // p is the result from the function FindStem
	if p is not defined:
		slink(q<sub>wa</sub>) = s<sub>0</sub>
		return NULL
	suf = δ(p, a)
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
	for a c Σ: δ(source, a) is defined:
		δ(dest, a) = δ(source, a)
}
</pre>

<pre>
RedirectTransitions(p, clone ,a) {
	if p is not defined || clone is not defined:
		return
	suf = δ(p, a)
	while p is defined && δ(p, a) = suf:
		δ(p, a) = clone
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
		len(q<sub>wa</sub> = i
		p = FindStem(q, q<sub>wa</sub>, w[i])
		clone = ModifyTree(p, q<sub>wa</sub>, w[i])
		RedirectTransitions(p, clone, w[i])
		q = q<sub>wa</sub>

	while q is defined:
		mark q as final
		q = slink(q)
}
</pre>

## Complexity ##
### Linearity of the number of states ###
To show that the number of states is <b><i>O(n)</i></b> we will use the following statement:
<b><i>Lemma:</i></b> Let <i>Φ</i> be a set of subsets of the set <i>{1, 2, 3,..., n}</i>. For every <i>S<sub>1</sub> , S<sub>2</sub> c Φ</i> we have either <i>S<sub>1</sub> ∩ S<sub>2</sub> = Ø</i> or <i>S<sub>1</sub> c S<sub>2</sub></i> . Then <i>|Φ|</i> ≤ n.

### Linearity of the number of transitions ###
We will show that the number of transitions is <i>|δ| ≤ 3n - 4</i>


### Linearity of the alorithm ###
Proving the complexity is linear ....








