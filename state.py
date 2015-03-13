# -- coding: utf-8 --
__author__ = 'stepan'

import copy

class State:

    def __init__(self, name):
        # inicializace a pojmenovani stavu
        self._term = False
        self._rules = {}

    def addRule(self, char, state):
        if char in self._rules:
            if state not in self._rules[char]:
                self._rules[char].append(state)
        else:
            self._rules[char] = [state]

    def setTerm(self, value):
        self._term = value

    def isTerm(self):
        return self._term

    def getAllRules(self):
        # vrati asociativni pole poli prechodu
        return self._rules;

    def getRules(self, char):
        # vrati pravidla pro urcity znak
        if char in self._rules:
            return self._rules[char]
        else:
            return []

    def addNonERules(self, rules):
        # prida do pravidla, ktera nejsou epsilonova
        rules = copy.deepcopy(rules)
        for char in rules:
            if char != '':
                for target in rules[char]:
                    self.addRule(char, target)

    def dropERules(self):
        if '' in self._rules: del self._rules['']

