# -- coding: utf-8 --
__author__ = 'stepan'
#DKA:xgrana02

import copy
import state


# reprezentuje automat se vsemi komponentami
class Automat:
    def __init__(self):
        self._states = {}
        self._alphabet = {}
        self._start = False

    # prida znak do abecedy
    def addAlpha(self, char):
        if len(char) != 1:
            raise ValueError("String '" + char + "' is not character", 40)

        self._alphabet[char] = True

    # prida stav, nepridava duplicity
    def addState(self, name):
        if name not in self._states:
            self._states[name] = state.State()

    # prida pravidlo, konroluje, jestli stavy existuji a jestli je znak v abecede
    def addRule(self, state, char, target):
        try:
            st = self._states[state]
        except:
            raise ValueError("Undefined state '" + state + "'", 41)
        try:
            self._states[target]
        except:
            raise ValueError("Undefined state '" + target + "'", 41)

        if char == '':
            st.addRule(char, target)
        else:
            try:
                self._alphabet[char]
            except:
                raise ValueError("Undefined character '" + char + "'", 41)
            st.addRule(char, target)

    # nastavi pocatecni stav, kontroluje, jestli stav existuje a jestli jiz neni nastaven
    def setStart(self, name):
        if not self._start:
            try:
                self._states[name]
                self._start = name
            except:
                raise ValueError("Setting start to undefined state'" + name + "'", 41)
        else:
            raise ValueError("Double setting start state", 41)

    # nastavi stav jako ukoncujici, kontroluje, jestli stav existuje
    def setTerminating(self, name):
        try:
            state = self._states[name]
        except:
            raise ValueError("Undefined terminating state '" + name + "'", 41)

        #print("Setting state '" + name + "' to terminating")
        state.setTerm(True)

    # ziska epsilon uzaver daneho stavu
    def getEClose(self, state):
        Q = {state: False}                   # zasobnik e prechodu, pridame zdrojovy stav
        Qbefore = copy.deepcopy(Q)              # zasobnik predchozi iterace
        while True:
            for st in Qbefore:               # prochazime stavy na zasobniku z predchozi iterace
                if Q[st] == False:           # prechod jeste nebyl prozkouman
                    for tran in self._states[st].getRules(''):
                        if tran not in Q:
                            Q[tran] = False  # pridame nove stavy do zasobniku a oznacime je jako neprozkoumane
                    Q[st] = True             # oznacime aktualni stav jako prozkoumany

            if len(Qbefore) == len(Q):       # koncime v pripade, ze nebyly pridany zadne nove stavy
                break
            else:
                Qbefore = copy.deepcopy(Q)
        return Q

    # odstrani epsilon pravidla
    def dropERules(self):
        for p in self._states:
            for eRule in self.getEClose(p):
                rTrans = self._states[eRule].getAllRules()
                self._states[p].addNonERules(rTrans)
                if self._states[eRule].isTerm():
                    self._states[p].setTerm(True)
            self._states[p].dropERules()

    # provede determinizaci (pred tim musi byt odstraneny epsilon pravidla)
    def determinate(self):
        Qnew = {}
        Qnew[self._start] = True
        aut = Automat()
        aut._alphabet = copy.deepcopy(self._alphabet)
        aut._start = self._start
        aut.addState(self._start)

        while True:
            #vezmeme stav z fronty
            state, value = Qnew.popitem()
            origStates = state.split("_")
            origRules = {}
            for origState in origStates:
                #prochazime originalni stavy, ze kterych je tento slozeny
                orgChars = self._states[origState].getAllRules()
                for char in orgChars:
                    if char not in origRules:
                        origRules[char] = []
                    for target in orgChars[char]:
                        #ziskaveme vsechna pravidla z puvodnich stavu
                        if target not in origRules[char]:
                            origRules[char].append(target)


            for char in origRules:
                targets = origRules[char]
                #vytvorime jmeno noveho stavu
                newState = '_'.join(sorted(targets))
                if newState not in aut._states:
                    #pridame novy stav do automatu a do zasobniku, pokud tam neni
                    aut.addState(newState)
                    Qnew[newState] = True

                #pridame pravidlo, ktere ukazuje na novy stav
                aut.addRule(state, char, newState)
                isTerm = False
                for target in targets:
                    if self._states[target].isTerm():
                        isTerm = True

                if isTerm:
                    #pokud byl nektery stav finalni, tak i novy je finalni
                    aut.setTerminating(newState)

            if len(Qnew) == 0:
                #zasobnik je prazdny, vyskocime z cyklu
                break

        self._states = aut._states

    # analyzuje retezec, vraci 1 nebo 0
    def analyzeString(self, string):
        state = self._start

        for char in string:
            rules = self._states[state].getRules(char)
            if len(rules) == 1:
                state = rules[0]
            else:
                if char in self._alphabet:
                    return 0
                else:
                    raise ValueError("Character '" + char + "' is not acceptable", 1)

        if self._states[state].isTerm():
            return 1
        else:
            return 0

    # vraci abecedu - dict
    def getAlphabet(self):
        return self._alphabet



    # vraci automat jako retezec
    def __str__(self):
        ret = '(\n'

        states = sorted(self._states.items(), key=lambda t: t[0])
        alphabet = sorted(self._alphabet.items(), key=lambda t: t[0])

        ret += "{"
        i = 0

        for state in states:
            if i != 0:
                ret += ", "
            ret += state[0]
            i+=1


        ret += "},\n{"
        i=0

        for char in alphabet:
            if i != 0:
                ret += ", "

            if char[0] == "'":
                ch = "''"
            else:
                ch = char[0]

            ret += "'" + ch + "'"
            i+=1

        ret += "},\n{"
        i=0

        for state in states:
            keys = state[1].getAllRules()
            keys = sorted(keys.items(), key=lambda t: t[0])
            for key in keys:
                rules = sorted(key[1])
                for rule in rules:
                    if i != 0:
                        ret+= ",\n"
                    else:
                        ret+= "\n"

                    if key[0] == "'":
                        k = "''"
                    else:
                        k = key[0]

                    ret+= state[0] + " '" + k + "' -> " + rule
                    i+=1

        ret += "\n},\n"
        ret += self._start + ",\n"

        ret += "{"
        i=0
        for state in states:
            if state[1].isTerm():
                if i != 0:
                    ret += ", "
                ret += state[0]
                i+=1
        ret += "}\n"

        return ret + ")"