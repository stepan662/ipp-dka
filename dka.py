__author__ = 'stepan'


import sys
import arguments
import parser


def main():
    try:
        args = arguments.Arguments("--input=dka.py".split(" "))

    except ValueError as e:
        sys.stderr.write(e.args[0] + "\n")
        sys.exit(e.args[1])

    if args.help:
        print("napoveda\n")
        sys.exit(0)

    try:
        par = parser.Parser()

    except ValueError as e:
        sys.stderr.write(e.args[0] + "\n")
        sys.exit(e.args[1])

main()