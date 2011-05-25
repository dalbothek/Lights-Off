#!/usr/bin/env python

import sys, binascii
from puzzle import *
from scheduler import *

size = 5

def showHelp():
    print 'Usage: lightsoff command [options]'
    print
    print 'Commands:'
    print '\tgen [-s|-l|-b] [-o file] [-t threads] [count] - Generates puzzles'
    print '\t\t-s: short form (one line per puzzle)'
    print '\t\t-l: long form'
    print '\t\t-b: binary form'
    print '\t\t-o file: save output in file'
    print '\t\t-t threads: number of threads (defaults to number of CPU cores)'
    print '\t\tcount: number of puzzles'

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
