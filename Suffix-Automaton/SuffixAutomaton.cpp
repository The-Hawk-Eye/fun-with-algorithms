#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <map>
#include <iostream>

/*
 Representation of a state:
   * q.len - gives the length of the word
   * q.index - gives the starting index of the word (q.index = w[i])
   * q.slink - points to the state with the longest suffix of q, which does not belong to the equivalence class of q (s(q))
   * q.delta - is the set of all transitions from the qurrent state q
   * q.final = true if the state is final
*/
struct State {
	int len;
	int index;
	State* slink;
	std::unordered_map<char, State* > delta;
	bool final;
};


State* FindStem(State* q_w, State* q_wa, char a);
State* ModifyTree(State* p, State* q_epsi, State* q_wa, char a);
void CopyTransitions(State* source, State* dest);
void RedirectTransitions(State* p, State* suf_prime, char a);
void BuildSuffixAutomaton(const std::string& w, std::unordered_set<State*>& Qw);
void DeleteAutomaton(std::unordered_set<State*>& Qw);


/*
 Given a state q_w and a letter 'a'
 Finds q_wk which has a transitiion with letter a
 q_wi is the slink of q_w(i-1)
 Adds a transition with letter a to all states q_w0, q_w1, ... , q_w(k-1)
 All transitions are toward state q_wa
 Returns state q_wk
*/
State* FindStem(State* q_w, State* q_wa, char a) {
	State* q = q_w;
	while ((q != NULL) && (q->delta.find(a) == q->delta.end())) { /* q is defined AND delta(q)(a) in not defined */
		q->delta[a] = q_wa;
		q = q->slink;
	}

	return q;
}



/*
 Given p = q_wk - the k-th slink of q_w
 and a letter 'a'
 Checks if a new state (s(wa)) has to be created and modifies the subword tree if needed
 Assigns the correct state to q_wa->slink (s(wa))
*/
State* ModifyTree(State* p, State* q_epsi, State* q_wa, char a) {
	if (p == NULL) {
		q_wa->slink = q_epsi;
		return NULL;
	}

	State* suf = p->delta[a]; /* transition delta(p)(a) exists, see function FindStem */
	if (suf->len == (p->len + 1) && suf->len != 0) { /* check if suf is the representative of its equivalence class */
		q_wa->slink = suf;
		return NULL;
	}

	/* if suf was not the representative then a new class is created */
	State* suf_prime = new State;
	suf_prime->len = p->len + 1;
	suf_prime->final = false;
	CopyTransitions(suf, suf_prime);

	/* modification of the subword tree */
	suf_prime->slink = suf->slink;
	suf->slink = suf_prime;
	q_wa->slink = suf_prime;

	return suf_prime;
}



/*
 Given a source state and a destination state
 Copies all existing transitions starting from the source state
 and replicates them as transitions starting from the dest state
*/
void CopyTransitions(State* source, State* dest) {
	std::unordered_map<char, State*>::iterator it;
	for (it = (source->delta).begin(); it != (source->delta).end(); it++) {
		dest->delta[it->first] = it->second;
	}
	// dest->delta = source->delta;
}



void RedirectTransitions(State* p, State* suf_prime, char a) {
	if (p == NULL || suf_prime == NULL)
		return;

	State* temp = p;
	State* suf = p->delta[a];
	while ((temp != NULL) && (temp->delta[a] == suf)) {
		temp->delta[a] = suf_prime;
		temp = temp->slink;
	}
}



/*
 Given a string w and an empty set of states Qw
 Builds a suffix automaton for the string w
 The new states are dynamically alocated on the heap
 The states are input in the set Qw
*/
void BuildSuffixAutomaton(const std::string& w, std::unordered_set<State*>& Qw) {
	/* initial state of the automaton is the empty word */
	State* q_epsi = new State;
	q_epsi->len = 0;
	q_epsi->index = 0;
	q_epsi->slink = NULL;
	q_epsi->final = true; /* recognizing the empty word as a suffix */
	Qw.insert(q_epsi);

	/* build the automaton online */
	State* q_w = q_epsi; /* current state */
	for (int i = 0; i < w.length(); i++) {
			State* q_wa = new State; /* next state */
			q_wa->len = i + 1;
			q_wa->index = 0;
			q_wa->final = false;
			State* p = FindStem(q_w, q_wa, w[i]); /* Finds q_wk which has a transitiion with letter a */
			State* suf_prime = ModifyTree(p, q_epsi, q_wa, w[i]);
			RedirectTransitions(p, suf_prime, w[i]);
			if (suf_prime != NULL) {
				suf_prime->index = (i - suf_prime->len) + 1;
				Qw.insert(suf_prime);
			}
			Qw.insert(q_wa);
			q_w = q_wa;
	}

	/* mark final states */
	while (q_w != NULL) {
		q_w->final = true;
		q_w = q_w->slink;
	}
}



/*
 Given a set of states
 Deletes the states from memory
*/
void DeleteAutomaton(std::unordered_set<State*>& Qw) {
	for (State* q: Qw) {
		delete q;
	}
}