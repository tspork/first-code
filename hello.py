# HOWTO:
#
# Python program files are named SOMETHING.scm.
#
# Run w/ 0 arguments:
# $ python3 hello.py
#
# Run w/ 1 argument:
# $ python3 hello.py Tau

import sys

def main(argv):
    if len(argv) == 2:
        print(f"Hello, " + argv[1] + "!")
    else:
        print("Hello, STRANGER!")
    sys.exit(0)

main(sys.argv)
