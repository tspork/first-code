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

def length(blah):
    return len(blah)

def main(words):
    if length(words) == 2:     # why 2?
        print("Hello, " + words[1] + "!")
    else:
        print("Hello, STRANGER!")
    sys.exit(0)

main(sys.argv)
