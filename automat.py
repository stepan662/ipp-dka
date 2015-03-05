__author__ = 'stepan'

import state
import copy

class Automat:
    def __init__(self):
        self._states = {}
        self._alphabet = {}
        self._start = False
        self._term = False

    def addAlpha(self, char):
        if len(char) != 1:
            raise ValueError("String '" + char + "' is not character", 40)

        #print("Adding char to alphabet: '" + char + "'")
        self._alphabet[char] = True

    def addState(self, name):
        if name not in self._states:
            self._states[name] = state.State(name)
        #    print("Adding state to automat: '" + name + "'")

    def addRule(self, state, char, target):
        try:
            st = self._states[state]
        except:
            raise ValueError("Undefined state '" + state + "'", 40)
        try:
            self._states[target]
        except:
            raise ValueError("Undefined state '" + target + "'", 40)

        #print("Adding rule to state '" + state + "': '" + char + "' -> '" + target + "'")
        if char == '':
            st.addRule(char, target)
        else:
            try:
                self._alphabet[char]
            except:
                raise ValueError("Undefined character '" + char + "'", 40)
            st.addRule(char, target)

    def setStart(self, name):
        if not self._start:
            try:
                self._start = self._states[name]
            except:
                raise ValueError("Setting start to undefined state'" + name + "'", 40)
        else:
            raise ValueError("Double setting start state", 40)

        #print("Setting start state to '" + name + "'")

    def setTerminating(self, name):
        try:
            state = self._states[name]
        except:
            raise ValueError("Undefined terminating state '" + name + "'", 40)

        #print("Setting state '" + name + "' to terminating")
        state.setTerm(True)

    def getEClose(self, state):
        Q = {}
        Q[state] = False
        Qtmp = copy.deepcopy(Q)
        while True:
            for st in Qtmp:
                if Q[st] is False:
                    for tran in self._states[st].getRules(''):
                        Q[tran] = False
                    Q[st] = True

            if len(Qtmp) == len(Q):
                break
            else:
                Qtmp = copy.deepcopy(Q)
        return Q

    def dropERules(self):
        for p in self._states:
            for eRule in self.getEClose(p):
                rTrans = self._states[eRule].getAllRules()
                self._states[p].addNonERules(rTrans)
                if self._states[eRule].isTerm():
                    self._states[p].setTerm(True)
            self._states[p].dropERules()

    def __str__(self):

        ret = ''

        #dict = sorted(self._states.items(), key=lambda t: t[0])
        #for w in dict:
        #    ret += w[0] + "\n"

        for state in sorted(self._states.items(), key=lambda t: t[0]):
            if state[1].isTerm():
                ret += "\t"+state[0] + "(terminating)\n"
            else:
                ret += "\t"+state[0] + "\n"

            rChars = state[1].getAllRules()
            for rules in rChars:
                for rule in rChars[rules]:
                    ret += "\t\t'"+rules+"'\t-> "+ rule + "\n"
        return ret



