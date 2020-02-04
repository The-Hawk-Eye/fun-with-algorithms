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
<i>Suffix(w) = {ß ε Σ* | exists α: αß = w}</i>  
  
A suffix automaton is a minimal DFA over the language <i>L = Suffix(w)</i>. From Nerode's theorem it follows that the number of states of the minimal DFA is equal to the number of equivalence classes in the relation <i>R<sub>L</sub></i>, where:  
<i>{α,ß} ε R<sub>L</sub> (α ≡<sub>L</sub> ß) ↔ for every z ε Σ*: αz ε L ↔ ßz ε L</i>