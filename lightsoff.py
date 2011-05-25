#!/usr/bin/env python

import sys, binascii
from puzzle import *
from scheduler import *
from terminal import *

size = 5

def showHelp():
    term = TerminalController()
    helptext = '''
${BOLD}NAME${NORMAL}
    lightsoff - level generator
    
${BOLD}SYNOPSIS${NORMAL}
    lightsoff command [options]
    
${BOLD}COMMANDS${NORMAL}
    gen [-s|-l|-b] [-o ${UNDERLINE}file${NORMAL}] [-t ${UNDERLINE}threads${NORMAL}] [${UNDERLINE}count${NORMAL}] - Generates puzzles

${BOLD}OPTIONS${NORMAL}
        -s
            short form (one line per puzzle)
        -l
            long form
        -b
            binary form${NORMAL}
        -o ${UNDERLINE}files${NORMAL}
            save output in file
        -t ${UNDERLINE}hreadss${NORMAL}
            number of threads (defaults to number of CPU cores)
        ${UNDERLINE}count${NORMAL}
            number of puzzles
'''
    if term.BOLD and term.UNDERLINE:
        print term.render(helptext)
    else:
        print term.strip(helptext)
    

def generate(count=1, form=None, path=None, threads=None):
    if form == None:
        if count == 1:
            form = "long"
        else:
            form = "short"
    scheduler = Scheduler(threads)
    for i in range(count):
        scheduler.schedule(randomGrid,form)
    scheduler.run()
    if path:
        out = open(path, "wb")
        out.write(scheduler.output)
        out.close()
    else:
        print scheduler.output

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
    if len(args) == 0:
        showHelp()
    elif args[0] in ['gen', 'generate']:
        count = 1
        form = None
        path = None
        threads = None
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
            elif arg == "-t":
                if i < len(args):
                    threads = args[i]
                    i += 1
                else:
                    threads = 1
            else:
                count = int(arg)
        generate(count, form, path, threads)
    else:
         showHelp()

handleArguments(sys.argv[1:])
