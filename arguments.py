__author__ = 'stepan'

import getopt, sys


class Arguments():
    def __init__(self, args_in):
        self.help = False
        self.input = False
        self.output = False
        self.e = False
        self.d = False
        self.i = False

        arguments = dict()
        longArgs = {"help": "help", "input": "input", "output": "output", "no-epsilon-rules": "e",
                    "determinization": "d",
                    "case-insensitive": "i"}
        try:
            opts, args = getopt.getopt(args_in, "edi",
                                       ["help", "input=", "output=", "no-epsilon-rules", "determinization",
                                        "case-insensitive"])
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

        if "help" in arguments:
            if len(arguments) == 1:
                self.help = True
            else:
                raise ValueError("Bad arguments combination", 1)

        if "input" in arguments:
            fileName = arguments["input"]
            try:
                self.input = open(fileName, "r")
            except IOError as e:
                raise ValueError("Can't open input file", 2)
        else:
            self.input = sys.stdin

        if "output" in arguments:
            fileName = arguments["output"]
            try:
                self.output = open(fileName, "w")
            except IOError as e:
                raise ValueError("Can't open output file", 2)
        else:
            self.output = sys.stdout

        if "e" in arguments:
            self.e = True

        if "d" in arguments:
            if self.e:
                raise ValueError("Combination of -e and -d is not allowed", 1)
            else:
                self.d = True

        if "i" in arguments:
            self.i = True

    def __str__(self):
        print('<Arguments\n', self.help, "\n", self.input, '\n', self.output, "\n", self.e, "\n", self.d, "\n", self.i, "\n>")