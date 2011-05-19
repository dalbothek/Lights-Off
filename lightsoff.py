import sys, binascii
from puzzle import *

size = 5

def showHelp():
    print 'Usage: lightsoff command [options]'
    print
    print 'Commands:'
    print '\tgen [-s|-l|-b] [-o file] [count] - Generates puzzles'
    print '\t\t-s: short form (one line per puzzle)'
    print '\t\t-l: long form'
    print '\t\t-b: binary form'
    print '\t\tcount: number of puzzles'

def generate(count=1, form=None, path=None):
    if form == None:
        if count == 1:
            form = "long"
        else:
            form = "short"
    if path:
        out = open(path, "wb")
    for i in range(count):
        string = randomGrid(form)
        if path:
            out.write(string)
        else:
            print string
    if path:
       out.close()

def randomGrid(form="long"):
    grid = RandomPuzzle(size)
    if form == "short":
        return grid.export()
    elif form == "long":
        return grid.display()
    else:
        h = hex(grid.int())
        h = "0"*(10-len(h)) + h[2:]
        return binascii.a2b_hex(h)
    

def handleArguments(args):
    if len(args) == 0 or args[0] in ['-h', 'help', '--help']:
        showHelp()
    elif args[0] in ['gen', 'generate']:
        count = 1
        form = None
        path = None
        i = 1
        while i < len(args):
            arg = args[i]
            i += 1
            if arg == "-s":
                form = "short"
            elif arg == "-l":
                form = "long"
            elif arg == "-b":
                form = "int"
            elif arg == "-o":
                if i < len(args):
                    path = args[i]
                    i += 1
                else:
                    path = "puzzles"
            else:
                count = int(arg)
        generate(count, form, path)

handleArguments(sys.argv[1:])
#handleArguments(['gen', "-b", 20, "-o"])
