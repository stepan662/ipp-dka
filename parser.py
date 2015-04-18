# -- coding: utf-8 --
__author__ = 'stepan'
#DKA:xgrana02

import automat

# struktura token - obsahuje typ tokenu a string (vyuziva se u identifikatoru)
class Token:
    def __init__(self, type, string):
        self.type = type
        self.string = string


class Parser:
    def __init__(self, input):
        self.index = 0
        self.str = input
        self.line = 1

        # vytvorime prazdny automat
        self.aut = automat.Automat()

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

    # vraci vytvoreny automat
    def getAutomat(self):
        return self.aut


    # nacte vsechny stavy do automatu
    def states(self):
        token = self.getToken()
        if token.type == '}':
            return  # stavy jsou prazdne
        while token.type != '':
            self.tShould(token, ['id'])
            self.aut.addState(token.string)
            token = self.getToken()
            self.tShould(token, [',', '}'])
            if token.type == ',':
                token = self.getToken()
            else:
                return

    # nacte abecedu do automatu
    def alphabet(self):
        token = self.getToken()
        if token.type == '}':
            return  # abeceda je prazdna
        while token.type != '':
            self.tShould(token, ['str'])
            self.aut.addAlpha(token.string)
            token = self.getToken()
            self.tShould(token, [',', '}'])
            if token.type == ',':
                token = self.getToken()
            else:
                return

    # nacte vsechny pravidla do automatu
    def rules(self):
        token = self.getToken()
        if token.type == '}':
            return  # pravidla jsou prazdna

        while token.type != '':
            # ocekavame id zdrojoveho stavu
            self.tShould(token, ['id'])
            state = token.string

            # ocekavame znak
            token = self.getToken()
            self.tShould(token, ['str'])
            char = token.string

            # ocekavame sipku
            token = self.getToken()
            self.tShould(token, ['->'])

            # ocekavame id ciloveho stavu
            token = self.getToken()
            self.tShould(token, ['id'])
            target = token.string

            self.aut.addRule(state, char, target)

            # ocekavame carku nebo zavorku - pak koncime nebo jedeme znovu
            token = self.getToken()
            self.tShould(token, [',', '}'])
            if token.type == ',':
                token = self.getToken()
            else:
                return

    # nacte vsechny ukoncujici stavy
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


    # pomocna funkce, ktera kontrojuje, jestli byl token ocekavaneho typu
    # v pripade ze ne, rovnou vypisuje chybu
    def tShould(self, token, types):
        for ch in types:
            if ch == token.type:
                return
        raise ValueError("Syntax error: unexpected token type: '" + token.type
                         + "', expecting " + types.__str__()
                         + " on line " + self.line.__str__(), 40)

    # nacte dalsi token
    def getToken(self):
        ch = self.getChar()
        state = 'begin'
        str = ''
        while ch != False:

            # pocatecni stav automatu, preskakujeme bile znaky
            if state == 'begin':
                if ch.isspace():
                    if ch == '\n':
                        self.line += 1      # pocitame radky, abychom mohli lepe vypisovat chyby
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
                    raise ValueError("Unexpected character '" + ch + "' (line " + self.line.__str__() + ")", 40)

            # ocekavame dokonceni sipky znakem >
            elif state == 'arrow':
                if ch == '>':
                    return Token('->', '')
                else:
                    raise ValueError("Unexpected character '" + ch + "' (line " + self.line.__str__() + ")", 40)

            # ocekavame vnitrek retezce
            elif state == 'string':
                if ch != "'":
                    str += ch
                else:
                    state = 'gotApostrof'

            # nacetli jsme apostrof uprostred retezce
            elif state == 'gotApostrof':
                if ch != "'":
                    self.ungetChar()
                    return Token('str', str)
                else:
                    str += "'"
                    state = 'string'

            # ocekavame c like id
            elif state == 'id':
                if self.isIdBegin(ch) or (ord('0') <= ord(ch) <= ord('9')):
                    str += ch
                else:
                    self.ungetChar()
                    return Token('id', str)

            # komentar - preskakujeme do konce radku
            elif state == 'comment':
                if ch == '\n':
                    state = 'begin'

            ch = self.getChar()

        # vracime prazdny token, v pripade, ze soubor skoncil
        return Token('', '')

    # vrati znak zpatky na vstup
    def ungetChar(self):
        if self.index > 0:
            self.index -= 1
        else:
            raise ValueError("Nothing to unget", 40)

    # nacte jeden znak ze vstupu
    def getChar(self):
        if self.index < len(self.str):
            ch = self.str[self.index]
            self.index += 1
            return ch
        else:
            return False

    # kontroluje, jestli jde o znak, ktery se muze vyskytovat na zactaku c like id
    def isIdBegin(self, ch):
        if ord('a') <= ord(ch) <= ord('z'):
            return True
        elif ord('A') <= ord(ch) <= ord('Z'):
            return True
        else:
            return False







