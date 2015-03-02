__author__ = 'stepan'


import arguments,sys

def main():
    try:
        args = arguments.Arguments("--input=dka.py".split(" "))

    except ValueError as e:
        sys.stderr.write(e.args[0] + "\n")
        sys.exit(e.args[1])

    if args.help:
        print("napoveda\n")
        sys.exit(0)

    args.__str__()

main()