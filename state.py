# -- coding: utf-8 --
__author__ = 'stepan'
#DKA:xgrana02

import copy

# reprezentuje jeden stav - obsahuje odkazy na dalsi pravidla a info, jestli je ukoncujici
class State:

    # inicializace a pojmenovani stavu
    def __init__(self, name):
        self._term = False
        self._rules = {}

    # prida do stavu odkaz na dalsi stav
    def addRule(self, char, state):
        if char in self._rules:
            if state not in self._rules[char]:
                self._rules[char].append(state)
        else:
            self._rules[char] = [state]

    # nastavi, ukoncujici stav
    def setTerm(self, value):
        self._term = value

    # vraci informaci, jestli je ukoncujici
    def isTerm(self):
        return self._term

    # vrati asociativni pole poli prechodu
    def getAllRules(self):
        return self._rules;

    # vrati pravidla pro urcity znak
    def getRules(self, char):
        if char in self._rules:
            return self._rules[char]
        else:
            return []

    # prida do pravidla, ktera nejsou epsilonova
    def addNonERules(self, rules):
        rules = copy.deepcopy(rules)
        for char in rules:
            if char != '':
                for target in rules[char]:
                    self.addRule(char, target)

    # odstrani epsilon pravidla
    def dropERules(self):
        if '' in self._rules: del self._rules['']