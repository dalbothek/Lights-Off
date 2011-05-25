import threading, os
from multiprocessing import cpu_count

class Scheduler:
    def __init__(self, threads=None):
        self.output = ""
        self.queue = []
        self.termlock = threading.Condition()
        self.outputlock = threading.Lock()
        self.joblock = threading.Lock()
        if threads == None:
            self.number = cpu_count()
        else:
            self.number = threads
        

    def schedule(self, func, arg=None):
        self.queue.insert(0, [func,arg])

    def run(self):
        self.termlock.acquire()
        for i in range(self.number):
            threading.Thread(target=self.thread).start()

        while self.number > 0:
            self.termlock.wait()
            
        return self.output

    def thread(self):
        while True:
            job = self.next()
            if not job:
                break
            output = job[0](job[1])
            self.appendOutput(output)
        self.termlock.acquire()
        self.number -= 1
        self.termlock.notify()
        self.termlock.release()

    def next(self):
        self.joblock.acquire()
        if len(self.queue) == 0:
            job = False
        else:
            job = self.queue.pop()
        self.joblock.release()
        return job

    def appendOutput(self, output):
        self.outputlock.acquire()
        self.output += output
        self.outputlock.release()
