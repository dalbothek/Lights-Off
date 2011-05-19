import random
from grid import *

class Puzzle:
    def __init__(self, size=5, **args):
        self.size = size
        self.gen(args)


    def gen(self, args):
        self.state = Grid(self.size)
        self.taps = Grid(self.size)
        

    def tapGrid(self, grid, changestate=True):
        for y in range(self.size):
            for x in range(self.size):
                if grid.get(x,y) == 1:
                    self.tap(x,y, changestate)
                    

    def tap(self, x, y, changestate=True):
        if changestate:
            self.state.toggle(x,y)
            self.state.toggle(x,y+1)
            self.state.toggle(x,y-1)
            self.state.toggle(x+1,y)
            self.state.toggle(x-1,y)
        self.taps.toggle(x,y)

        
    def par(self):
        best = self.taps.sum()
        if best == 0:
            best = 26
        for i in range(4):
            self.state.rotate()
            assert self.solve()
            newsum = self.taps.sum()
            if best > newsum:
                best = newsum
        return best


    def solve(self):
        statecache = self.state.clone()
        self.taps = Grid()
        for x in range(1, self.size):
            for y in range(self.size):
                if self.state.get(x-1,y) == 1:
                    self.tap(x,y)
        lastline = ""
        for y in range(self.size):
            lastline += str(self.state.get(self.size-1,y))
            
        self.state = statecache
        
        if not SOLUTIONS.has_key(lastline):
            print lastline
            return False
        
        self.tapGrid(StringGrid(string=SOLUTIONS[lastline]), False)
        return True                
    

    def export(self, par=True):
        export = self.state.string()
        if par:
            export += str(self.par())
        return export

    def int(self, par=True):
        grid = self.state.int()
        if not par:
            return grid
        else:
            par = self.par()
            return grid | (par << 25)
            

        
    def display(self, par=True):
        display = self.state.display()
        if par:
            display += "Par: " + str(self.par()) + "\n"
        return display


class RandomPuzzle(Puzzle):
    def gen(self, args):
        self.taps = RandomGrid()
        self.state = Grid()
        self.tapGrid(self.taps)

SOLUTIONS = {
    '11100':'0100011100000101101100010',
    '00111':'0001000111010001101101000',
    '11011':'0010001110100011010100100',
    '10001':'1100000100101110101000011',
    '01010':'1110001010001110000000111',
    '00000':'0000000000000000000000000',
    '10110':'0000100011001010111010000',
    '01101':'1000011000101000111000001'
    }
