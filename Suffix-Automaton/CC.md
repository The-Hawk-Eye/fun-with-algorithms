# Correctness and Complexity
## Suffix Automaton ##

### Introduction ###
A suffix automaton for a given string <i>w</i> is a minimal <b>DFA</b> (deterministic finite automaton) that accpets all the suffixes of the string <i>w</i>. For a string of length <b>n</b> it only requires <b><i>O(n)</i></b> memory and it can also be built in <b><i>O(n)</i></b> time. The algorithm was discovered in 1983 by <i>Blumer, Blumer, Haussler, Ehrenfeucht, Chen and Seiferas</i> and was presented in their paper <i>The smallest automaton recognizing the subwords of a text</i>. An important property of a suffix automaton is, that it contains information about all substrings of the string <i>w</i>. This is due to the following theorem:  
<i>Theorem: Given two strings w and x, <b>x is a substring of w</b> if and only if <b>x is a prefix of a suffix of w</b>.</i>  
Any path starting at the initial state <b><i>s<sub>0</sub></i></b> fors a substring of <i>w</i>. And coversely every substring of <i>w</i> corresponds to a certain path starting at <b><i>s<sub>0</sub></i></b>.

### Notation ###
<i>Σ</i> - nonempty alphabet  
<i>ε</i> - the empty word  
<i>Σ*</i> - the set of all words over <i>Σ</i>  
<i>Suffix(w) = { ß ε Σ* | exists α: αß = w }</i>  
  
A suffix automaton is a minimal DFA over the language <i>L = Suffix(w)</i>. From Nerode's theorem it follows that the number of states of the minimal DFA is equal to the number of equivalence classes in the relation <i>R<sub>L</sub></i>, where:  
<i>{α, ß} ε R<sub>L</sub> (α ≡<sub>L</sub> ß) ↔ for every z ε Σ*: αz ε L ↔ ßz ε L</i>  

#### End positions <b><i>end_pos</b></i> ####
Let <i>w</i> = a<sub>1</sub>a<sub>2</sub>...a<sub>n</sub> <i>(a<sub>i</sub> ε Σ)</i> and <i>y╪ε ε Σ*</i>  
define: <i><b>end_pos<sub>w</sub>(y)</b> = { i | y = a<sub>i-|y|+1</sub>...a<sub>i</sub> }</i>  
<i>end_pos<sub>w</sub>(y)</i> is the set of all positions in the string <i>w</i>, in which the occurrences of <i>y</i> end  
<i>end_pos<sub>w</sub>(ε) = { 0, 1, 2, ..., |w| }</i>

two strings <i>x, y ε Σ*</i> are <b>end-equivalent on w</b> if and only if <i>end_pos<sub>w</sub>(x) = end_pos<sub>w</sub>(y)</i>  
end-equivalence will be denoted by <i>≡<sub>w</sub></i> , i.e. <i>x ≡<sub>w</sub> y ↔ end_pos<sub>w</sub>(x) = end_pos<sub>w</sub>(y)</i>  

<b><i>Corollary:</i></b> The end-equivalence relation is equivalent to Nerode's relation <i>R<sub>L</sub></i> for the language <i>L = Suffix(w)</i>:  
<i>x ≡<sub>w</sub> y ↔ x ≡<sub>Suffix(w)</sub> y</i>  
<b><i>Proof:</i></b> Let <i>w = a<sub>1</sub>a<sub>2</sub>...a<sub>n</sub> (a<sub>i</sub> ε Σ) and x, y, z ε Σ*</i>. Then <i>xz ε Suffix(w) ↔ xz = a<sub>n-|xz|+1</sub>...a<sub>n</sub>  
→ x = a<sub>n-|xz|+1</sub>...a<sub>n-|z|</sub> and z = a<sub>n-|z|+1</sub>...a<sub>n</sub>  
→ x = a<sub>i-|x|+1</sub>...a<sub>i</sub> and i = n - |z|</i>  
But <i> x ≡<sub>Suffix(w)</sub> y ↔ for every z ε Σ*: xz ε Suffix(w) ↔ yz ε Suffix(w)  
↔ for every i: x = a<sub>i-|x|+1</sub>...a<sub>i</sub> ↔ y = a<sub>i-|y|+1</sub>...a<sub>i</sub>  
↔ end_pos<sub>w</sub>(x) = end_pos<sub>w</sub>(y)</i>

<b><i>Example:</b></i>
<pre>	<i>w = a b c b c</i>  
	<i>   0 1 2 3 4 5</i>  
    	<i>end_pos<sub>w</sub>(bc) = end_pos<sub>w</sub>(c) = {3, 5}</i>  
    	<i>bc ≡<sub>w</sub> c</i></pre>  
<b><i>Properties:</i></b>  
Let <i>x, y ε Σ*</i> be subwords of <i>w</i> with |x| ≤ |y|, then:
1. <i>end_pos<sub>w</sub>(x) ∩ end_pos<sub>w</sub>(y) ╪ Ø</i> → x is a suffix of y  
2. <i>x is a suffix of y → <i>end_pos<sub>w</sub>(x) = end_pos<sub>w</sub>(y)</i>  
3. We have either <i>end_pos<sub>w</sub>(x) c end_pos<sub>w</sub>(y)</i> or <i>end_pos<sub>w</sub>(x) ∩ end_pos<sub>w</sub>(y) = Ø</i>  

#### Equivalence classes <b><i>[x]<sub>w</sub></i></b> and Representatives <b><i>r(x)</i></b> ####
Let x be an infix of <i>w</i>. Denote by <i>[x]<sub>w</sub></i> the equivalence class of x with respect to the relation ≡<sub>w</sub> and denote by <b><i>r(x)</i></b> the longes word in the equivalence class <i>[x]<sub>w</sub></i>. We say that <i>r(x)</i> canonically represents the equivalence class <i>[x]<sub>w</sub></i>  
<p></p>  

<b><i>Lemma:</i></b>  
Let x be an infix of <i>w</i>, then:  
1. If there is a letter <i>a ε Σ</i>, such that every occurance of x in <i>w</i> is preceeded by <i>a</i>, then x does not represent the equivalence class <i>[x]<sub>w</sub></i>  
2. If x is a prefix of <i>w</i>, then x is the longest word in <i>[x]<sub>w</sub></i>  
3. If there are letters <i>b,c ε Σ, b ╪ c</i> and both <i>bx</i> and <i>cx</i> are infixes of <i>w</i>, then x canonically represents the equivalence class <i>[x]<sub>w</sub></i>  
4. <i>x = r(x)</i> ↔ x is a prefix of <i>w</i> or it occurs in two distinct left contexts  

<b><i>Proof:</i></b>
1. Let <i>a</i> preceed every occurance of x in <i>w</i>. Then for every <i>i c end_pos(x)</i> we have <i>w<sub>i-|x|</sub> = a</i>  
<i>→ i c end_pos(ax)</i>  
<i>→ end_pos(x) c end_pos(ax)</i>  
And since x is a suffix of <i>ax</i> we have that <i>end_pos(ax) c end_pos(x) → end_pos(x) = end_pos(ax)</i>
It follows that <i>x ≡<sub>w</sub> ax</i> and <i>|x| < |ax| → x ╪ r(x)</i>













