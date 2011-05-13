import random

class Grid:
    def __init__(self, size, state=None):
        self.size = size
        if state == None:
            self.state = self.nullGrid(size)
        else:
            self.state = state
        self.taps = self.nullGrid(size)

    def genRandom(self):
        tapgrid = self.randomGrid(self.size)
        self.tapGrid(tapgrid)
        return self

    def genFromString(self, save, state=True):
        if state == True:
            var = self.state
        else:
            var = self.nullGrid(self.size)
            
        for x in range(self.size):
            for y in range(self.size):
                var[x][y] = int(save[x*self.size+y])

        return var

    def tapGrid(self, grid, changestate=True):
        for y in range(self.size):
            for x in range(self.size):
                if grid[x][y] == 1:
                    self.tap(x,y, changestate)

    def tap(self, x, y, changestate=True):
        if changestate:
            self.toggle(x,y)
            self.toggle(x,y+1)
            self.toggle(x,y-1)
            self.toggle(x+1,y)
            self.toggle(x-1,y)
        self.taps[x][y] = self.taps[x][y] ^ 1
        
    def toggle(self, x, y):
        if x >= 0 and x < self.size and y >= 0 and y < self.size:
            self.state[x][y] = self.state[x][y] ^ 1

    def par(self):
        best = self.tapCount()
        for i in range(4):
            self.rotate()
            self.solve()
            if best > self.tapCount():
                best = self.tapCount()
        return best

    def rotate(self):
        newgrid = self.nullGrid(self.size)
        m = self.size - 1
        for x in range(self.size):
            for y in range(self.size):
                newgrid[m-y][x] = self.state[x][y]
        self.state = newgrid

    def solve(self):
        statecache = self.export(False)
        self.taps = self.nullGrid(self.size)
        for x in range(1, self.size):
            for y in range(self.size):
                if self.state[x-1][y] == 1:
                    self.tap(x,y)
        lastline = ""
        for y in range(self.size):
            lastline += str(self.state[self.size-1][y])
        self.genFromString(statecache)
        
        if not SOLUTIONS.has_key(lastline):
            return False
        
        self.tapGrid(self.genFromString(SOLUTIONS[lastline], False), False)
        return True                

    def clone(self):
        return Grid(self.size, self.state[::])

    def tapCount(self):
        par = 0
        for row in self.taps:
            for tap in row:
                par += tap
        return par


    def export(self, par=True):
        line = ""
        for x in range(self.size):
            for y in range(self.size):
                line += str(self.state[x][y])
        if par:
            line += str(self.par())
        return line

    def display(self, par=True):
        display = ""
        display += "+" + "-+"*self.size + "\n"
        for x in range(self.size):
            for y in range(self.size):
                display += "|"
                if self.state[x][y] == 1:
                    display += "x"
                else:
                    display += " "
            display += "|\n"
            display += "+" + "-+"*self.size + "\n"
        if par:
            display += "Par: " + str(self.par()) + "\n"
        return display
            

    # static
    def nullGrid(self, size):
        return self.grid(size, lambda x,y:0)

    def randomGrid(self, size):
        jump = random.random()*0.5 - 0.25
        return self.grid(size, lambda x,y:int(random.random()+jump+0.5))

    def grid(self, size, func):
        grid  = []
        for x in range(size):
            grid.append([])
            for y in range(size):
                grid[x].append(func(x,y))
        return grid


SOLUTIONS = {
    '11100':'0100011100000101101100010',
    '11011':'0010001110100011010100100',
    '10001':'1100000100101110101000011',
    '01010':'1110001010001110000000111',
    '10110':'0000100011001010111010000',
    '01101':'1000011000101000111000001'
    }
