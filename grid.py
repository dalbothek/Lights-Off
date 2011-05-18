import random

class Grid:
    def __init__(self, size=5, **args):
        self.size = size
        self.gen(args)

    def gen(self, args):
        self.build(lambda x,y:0)

    def build(self, func):
        self.grid = []
        for x in range(self.size):
            self.grid.append([])
            for y in range(self.size):
                self.grid[x].append(func(x,y))

    def get(self, x, y):
        return self.grid[x][y]

    def set(self, x, y, v):
        self.grid[x][y] = v

    def display(self):
        display = ""
        display += "+" + "-+"*self.size + "\n"
        for x in range(self.size):
            for y in range(self.size):
                display += "|"
                if self.grid[x][y] == 1:
                    display += "x"
                else:
                    display += " "
            display += "|\n"
            display += "+" + "-+"*self.size + "\n"
        return display

    def string(self):
        string = ''
        for x in range(5):
            for y in range(5):
                string += str(self.get(x,y))
        return string

    def toggle(self, x, y):
        if x >= 0 and x < self.size and y >= 0 and y < self.size:
            self.set(x,y, self.get(x,y) ^ 1)

    def clone(self):
        return GridGrid(grid=self)

    def rotate(self):
        copy = self.clone()
        m = self.size - 1
        for x in range(self.size):
            for y in range(self.size):
                self.set(m-y, x, copy.get(x,y))



    def sum(self):
        n = 0
        for row in self.grid:
            for field in row:
                n += field
        return n

class RandomGrid(Grid):
    def gen(self, args):
        jump = random.random()*0.5 - 0.25
        self.build(lambda x,y:int(random.random()+jump+0.5))

class GridGrid(Grid):
    def gen(self, args):
        assert args.has_key('grid')
        grid = args['grid']
        self.build(lambda x,y:grid.get(x,y))

class StringGrid(Grid):
    def gen(self, args):
        assert args.has_key('string')
        string = args['string']
        self.build(lambda x,y:string[x*self.size+y])

