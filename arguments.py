# -- coding: utf-8 --
__author__ = 'stepan'
#DKA:xgrana02

import getopt
import sys


# reprezentuje argumenty skriptu
class Arguments():
    def __init__(self, args_in):
        self.help = False
        self.input = False
        self.output = False
        self.e = False
        self.d = False
        self.i = False
        self.analyze = False

        del args_in[0]

        arguments = dict()
        longArgs = {"help": "help", "input": "input", "output": "output", "no-epsilon-rules": "e",
                    "determinization": "d", "case-insensitive": "i", "analyze-string": "analyze"}
        try:
            opts, args = getopt.getopt(args_in, "edi",
                                       ["help", "input=", "output=", "no-epsilon-rules", "determinization",
                                        "case-insensitive", "analyze-string="])
        except getopt.GetoptError as err:
            raise ValueError("Unknown option", 1)

        for o, a in opts:
            if o[2:] in longArgs:
                # long param
                o = longArgs[o[2:]]
            else:
                # short param
                o = o[1:]

            if o not in arguments:
                arguments[o] = a
            else:
                raise ValueError("Double option " + o, 1)

        # kotrola, jestli je argument help osamoceny
        if "help" in arguments:
            if len(arguments) == 1:
                self.help = True
            else:
                raise ValueError("Bad arguments combination", 1)

        # kontrola, jestli soubor input existuje a lze otevrit
        if "input" in arguments:
            fileName = arguments["input"]
            try:
                self.input = open(fileName, "r", encoding="utf-8")
            except IOError as e:
                raise ValueError("Can't open input file", 2)
        else:
            self.input = sys.stdin

        # kontrola, jestli soubor output lze otevrit
        if "output" in arguments:
            fileName = arguments["output"]
            try:
                self.output = open(fileName, "w", encoding="utf-8")
            except IOError as e:
                raise ValueError("Can't open output file", 2)
        else:
            self.output = sys.stdout

        if "e" in arguments:
            self.e = True

        # kontrola, jestli se nekombinuji argumenty -e a -d
        if "d" in arguments:
            if self.e:
                raise ValueError("Combination of -e and -d is not allowed", 1)
            else:
                self.d = True

        # kontrola, jestli se nekombinuji argumenty -e, -d a --analyze-string
        if "analyze" in arguments:
            if self.e or self.d:
                raise ValueError("Combination of -e or -d with --analyze-string is not allowed", 1)
            else:
                self.analyze = arguments["analyze"]

        if "i" in arguments:
            self.i = True

    # vraci argumenty jako retezec
    def __str__(self):
        return '<Arguments\n' + self.help.__str__() + "\n" \
               + self.input.__str__() + '\n' \
               + self.output.__str__() + "\n" \
               + self.e.__str__() + "\n" \
               + self.d.__str__() + "\n" \
               + self.i.__str__() + "\n>"