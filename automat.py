__author__ = 'stepan'

import node


class Automat:
    def __init__(self):
        self.states = {}
        self.alphabet = {}
        self.start = False
        self.term = False

    def addAlpha(self, char):
        if len(char) != 1:
            raise ValueError("String '" + char + "' is not character", 40)

        print("Adding char to alphabet: '" + char + "'")
        self.alphabet[char] = True

    def addState(self, name):
        self.states[name] = node.Node(name)
        print("Adding state to automat: '" + name + "'")

    def addRule(self, state, char, target):
        try:
            st = self.states[state]
        except:
            raise ValueError("Undefined state '" + state + "'", 40)
        try:
            tar = self.states[target]
        except:
            raise ValueError("Undefined state '" + target + "'", 40)
        try:
            self.alphabet[char]
        except:
            raise ValueError("Undefined character '" + char + "'", 40)
        print("Adding rule to state '" + state + "': '" + char + "' -> '" + target + "'")
        st.addTrans(char, tar)

    def setStart(self, name):
        if not self.start:
            try:
                self.start = self.states[name]
            except:
                raise ValueError("Setting start to undefined state'" + name + "'", 40)
        else:
            raise ValueError("Double setting start state", 40)

        print("Setting start state to '" + name + "'")

    def setTerminating(self, name):
        try:
            state = self.states[name]
        except:
            raise ValueError("Undefined terminating state '" + name + "'", 40)

        print("Setting state '" + name + "' to terminating")
        state.term = True


