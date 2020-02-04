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
    <i>w = a b c b c</i>  
    <i>   0 1 2 3 4 5</i>  
    <i>end_pos<sub>w</sub>(bc) = end_pos<sub>w</sub>(c) = { 3, 5 }</i>  
    <i>bc ≡<sub>w</sub> c</i>  
