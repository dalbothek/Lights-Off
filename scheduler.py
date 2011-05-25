import threading
from multiprocessing import cpu_count
from terminal import *

class Scheduler:
    def __init__(self, threads=None):
        self.output = ""
        self.queue = []
        self.total = 0
        self.termlock = threading.Condition()
        self.outputlock = threading.Lock()
        self.joblock = threading.Lock()
        if threads == None:
            self.threads = cpu_count()
        else:
            self.threads = threads
        

    def schedule(self, func, arg=None):
        self.queue.insert(0, [func,arg])

    def run(self):
        self.initProgress()
        self.termlock.acquire()
        for i in range(self.threads):
            threading.Thread(target=self.thread).start()

        while self.threads > 0:
            self.termlock.wait(0.2)
            self.updateProgress()

        self.hideProgress()
            
        return self.output

    def thread(self):
        while True:
            job = self.next()
            if not job:
                break
            output = job[0](job[1])
            self.appendOutput(output)
        self.termlock.acquire()
        self.threads -= 1
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

    def initProgress(self):
        terminal = TerminalController()
        try:
            self.progress = ProgressBar(terminal, "Generating levels")
        except:
            return
        self.total = len(self.queue)
        self.updateProgress()

    def updateProgress(self):
        if self.total > 0:
            left = len(self.queue)
            done = self.total - left
            self.progress.update(float(done)/self.total, str(done) + " of " + str(self.total))

    def hideProgress(self):
        if self.total > 0:
            self.progress.clear()
