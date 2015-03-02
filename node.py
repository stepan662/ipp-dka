__author__ = 'stepan'

class Node:

    def __init__(self, name):
        # inicializace a pojmenovani stavu
        self.trans = {}
        self.term = False

    def addTrans(self, char, state):
        # pridani noveho prechodu
        self.trans[char] = state

    def getTrans(self):
        # vrati asociativni pole prechodu
        return self.trans;

    def setTerm(self):
        self.term = True

    def getTerm(self):
        return self.term