# -- coding: utf-8 --
__author__ = 'stepan'


import sys
import arguments
import parser


def main():
    try:
        args = arguments.Arguments(sys.argv)

    except ValueError as e:
        sys.stderr.write(e.args[0] + "\n")
        sys.exit(e.args[1])


    if args.help:
        print("napoveda\n")
        sys.exit(0)

    file = args.input.read()
    if args.i:
        file = file.lower()

    try:
        par = parser.Parser(file)
        automat = par.getAutomat()

    except ValueError as e:
        sys.stderr.write(e.args[0] + "\n")
        sys.exit(e.args[1])

    if len(automat.getAlphabet()) == 0:
        sys.stderr.write("Alphabet is empty.\n")
        sys.exit(41)

    if args.analyze == False:
        if args.e:
            automat.dropERules()
        elif args.d:
            automat.dropERules()
            automat.determinate()
        args.output.write(automat.__str__())

    else:
        if args.i:
            args.analyze = args.analyze.lower()
            
        automat.dropERules()
        automat.determinate()
        try:
            args.output.write(automat.analyzeString(args.analyze).__str__())
        except ValueError as e:
            sys.stderr.write(e.args[0] + "\n")
            sys.exit(e.args[1])
    sys.exit(0)




main()