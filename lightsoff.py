import sys
from puzzle import *

size = 5

def showHelp():
    print 'Usage: lightsoff command [options]'
    print
    print 'Commands:'
    print '\tgen [-s|-l] [count] - Generates puzzles'
    print '\t\t-s: short form (one line per puzzle)'
    print '\t\t-l: long form'
    print '\t\tcount: number of puzzles'

def generate(count=1, short=None):
    if short == None:
        short = count != 1
    for i in range(count):
        print randomGrid(short)

def randomGrid(short=False):
    grid = RandomPuzzle(size)
    if short:
        return grid.export()
    else:
        return grid.display()
    

def handleArguments(args):
    if len(args) == 0 or args[0] in ['-h', 'help', '--help']:
        showHelp()
    elif args[0] in ['gen', 'generate']:
        count = 1
        short = None
        for arg in args[1:]:
            if arg == '-s':
                short = True
            elif arg == '-l':
                short = False
            else:
                count = int(arg)
        generate(count, short)

handleArguments(sys.argv[1:])
