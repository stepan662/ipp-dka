# -- coding: utf-8 --
__author__ = 'stepan'

import automat

class Token:
    def __init__(self, type, string):
        self.type = type
        self.string = string


class Parser:
    def __init__(self, input):
        self.index = 0
        self.str = input
        self.line = 1

        self.aut = automat.Automat()

        #token = self.getToken()
        #while token.type != '':
        #    print("token: '" + token.type + "'")
        #    token = self.getToken()

        #exit()

        # cekame dve oteveraci slozene zavorky
        token = self.getToken()
        self.tShould(token, ['('])
        token = self.getToken()
        self.tShould(token, ['{'])

        # nacteme stavy do automatu
        self.states()

        # cekame carku a oteviraci zavorku
        token = self.getToken()
        self.tShould(token, [','])
        token = self.getToken()
        self.tShould(token, ['{'])

        # nacteme abecedu
        self.alphabet()

        # cekame carku a oteviraci zavorku
        token = self.getToken()
        self.tShould(token, [','])
        token = self.getToken()
        self.tShould(token, ['{'])

        # nacteme pravidla
        self.rules()

        # cekame carku a startovaci stav
        token = self.getToken()
        self.tShould(token, [','])
        token = self.getToken()
        if token.type != 'id':
            raise ValueError("Missing start state", 40)
        else:
            self.aut.setStart(token.string)

        #cekame carku a oteviraci zavorku
        token = self.getToken()
        self.tShould(token, [','])
        token = self.getToken()
        self.tShould(token, ['{'])

        self.terminating()

        # cekame konec oteviraci zavorky a konec
        token = self.getToken()
        self.tShould(token, [')'])
        token = self.getToken()
        self.tShould(token, [''])

        #print(self.aut)

    def getAutomat(self):
        return self.aut



    def states(self):
        token = self.getToken()
        if token.type == '}':
            return
        while token.type != '':
            self.tShould(token, ['id'])
            self.aut.addState(token.string)
            token = self.getToken()
            self.tShould(token, [',', '}'])
            if token.type == ',':
                token = self.getToken()
            else:
                return

    def alphabet(self):
        token = self.getToken()
        if token.type == '}':
            return
        while token.type != '':
            self.tShould(token, ['str'])
            self.aut.addAlpha(token.string)
            token = self.getToken()
            self.tShould(token, [',', '}'])
            if token.type == ',':
                token = self.getToken()
            else:
                return

    def rules(self):
        token = self.getToken()
        if token.type == '}':
            return
        while token.type != '':
            self.tShould(token, ['id'])
            state = token.string

            token = self.getToken()
            self.tShould(token, ['str'])
            char = token.string

            token = self.getToken()
            self.tShould(token, ['->'])

            token = self.getToken()
            self.tShould(token, ['id'])
            target = token.string

            self.aut.addRule(state, char, target)

            token = self.getToken()
            self.tShould(token, [',', '}'])
            if token.type == ',':
                token = self.getToken()
            else:
                return

    def terminating(self):
        token = self.getToken()
        if token.type == '}':
            return
        while token.type != '':
            self.tShould(token, ['id'])
            self.aut.setTerminating(token.string)
            token = self.getToken()
            self.tShould(token, [',', '}'])
            if token.type == ',':
                token = self.getToken()
            else:
                return



    def tShould(self, token, types):
        for ch in types:
            if ch == token.type:
                return
        raise ValueError("Syntax error: unexpected token type: '" + token.type + "', expecting "+types.__str__()+" on line " + self.line.__str__(), 40)

    def getToken(self):
        ch = self.getChar()
        state = 'begin'
        str = ''
        while ch != False:
            #print(self.line.__str__() + ": " + state + " '" + ch + "'")

            if state == 'begin':
                if ch.isspace():
                    if ch == '\n':
                        self.line += 1
                elif ch == '#':
                    state = 'comment'
                elif ch == '-':
                    state = 'arrow'
                elif ch == "'":
                    state = 'string'
                elif ch == '{':
                    return Token('{', '')
                elif ch == '}':
                    return Token('}', '')
                elif ch == '(':
                    return Token('(', '')
                elif ch == ')':
                    return Token(')', '')
                elif ch == ',':
                    return Token(',', '')
                elif self.isIdBegin(ch):
                    str += ch
                    state = 'id'
                else:
                    raise ValueError("Unexpected character '" + ch + "'", 40)

            elif state == 'arrow':
                if ch == '>':
                    return Token('->', '')
                else:
                    raise ValueError("Unexpected character", 40)

            elif state == 'string':
                if ch != "'":
                    str += ch
                else:
                    state = 'gotApostrof'

            elif state == 'gotApostrof':
                if ch != "'":
                    self.ungetChar()
                    return Token('str', str)
                else:
                    str+= "'"
                    state = 'string'

            elif state == 'id':
                if self.isIdBegin(ch) or (ord('0') <= ord(ch) <= ord('9')):
                    str += ch
                else:
                    self.ungetChar()
                    return Token('id', str)

            elif state == 'comment':
                if ch == '\n':
                    state = 'begin'

            ch = self.getChar()

        return Token('', '')

    def ungetChar(self):
        if self.index > 0:
            self.index -= 1
        else:
            raise ValueError("Nothing to unget", 40)

    def getChar(self):
        if self.index < len(self.str):
            ch = self.str[self.index]
            self.index += 1
            return ch
        else:
            return False

    def isIdBegin(self, ch):
        if ord('a') <= ord(ch) <= ord('z'):
            return True
        elif ord('A') <= ord(ch) <= ord('Z'):
            return True
        else:
            return False







