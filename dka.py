# -- coding: utf-8 --
__author__ = 'stepan'
#DKA:xgrana02

import sys
import parser
import arguments


def main():

    # zpracovani argumentu skriptu
    try:
        args = arguments.Arguments(sys.argv)

    except ValueError as e:
        sys.stderr.write(e.args[0] + "\n")
        sys.exit(e.args[1])

    # tisk napovedy
    if args.help:
        print("napoveda\n")
        sys.exit(0)

    # v pripade, ze mame nastaven prepinac -i prevedeme vsechny znaky v souboru na male
    file = args.input.read()
    if args.i:
        file = file.lower()

    # parsovani souboru a vytvoreni automatu
    try:
        par = parser.Parser(file)
        automat = par.getAutomat()

    except ValueError as e:
        sys.stderr.write(e.args[0] + "\n")
        sys.exit(e.args[1])


    # chyba v pripade, ze vstupni abeceda je prazdna
    if len(automat.getAlphabet()) == 0:
        sys.stderr.write("Alphabet is empty.\n")
        sys.exit(41)


    if args.analyze == False:
        if args.e:
            # je nastaven prepinac -e: odstranime epsilon pravidla
            automat.dropERules()

        elif args.d:
            # je nasteven prepinac -d: provedeme determinizaci
            automat.dropERules()
            automat.determinate()

        # tisk automatu
        args.output.write(automat.__str__())

    else:
        # analyzujeme retezec

        if args.i:
            # nastavime znaky na male v pripade, ze je nastaven prepinac -i
            args.analyze = args.analyze.lower()

        # provedeme determinizaci
        automat.dropERules()
        automat.determinate()

        # analyzujeme retezec
        try:
            args.output.write(automat.analyzeString(args.analyze).__str__())
        except ValueError as e:
            sys.stderr.write(e.args[0] + "\n")
            sys.exit(e.args[1])

    sys.exit(0)



main()