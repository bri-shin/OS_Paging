import sys, os
import math
import specs

''' Initial Variables Provided '''
# The program is invoked with 6 command line arguments:

M = 0   # Machine size in words
P = 0   # Page size in words.
S = 0   # Size of each process, i.e., the references are to virtual addresses 0..S-1.
J = 0   # Job mix, which determines A, B, and C, as described below.
N = 0   # Number of references for each process.
R = ""  # Replacement algorithm, LIFO (NOT FIFO), RANDOM, or LRU.
filepath = 'random-numbers.txt'     # Random Text

''' Helper Functions Implemented (From Lab 2) '''

### Random OS Object is created to generate random number when requested
class randomOSObject():
    def __init__(self, filepath):
        self.randomFile = open(filepath, 'r')

    def stripFile(self):
        return int(self.randomFile.readline().strip())

    def randomOS(self, u):
        randomInt = self.stripFile()
        return 1 + randomInt % u

    # 2147469841 was found through a python script as the maximum value in the random-number file
    def randomFraction(self):
        return self.stripFile() / 2147469842

    def restart(self):
        self.__init__(filepath)

### Counter Object is the overarching time counter for the program
class TimeCounter():
    def __init__(self):
        self.currentTimeCount = 0

    def getTimeCount(self):
        return self.currentTimeCount

    def updateTimeCount(self):
        self.currentTimeCount += 1

# Process Class (simulating a process and its necessary functions) - Modified from Lab 2

class Process():
    def __init__(self, A, B, C, processID):
        super(Process, self).__init__()
        self.A = A              # Probability of sequential memory reference
        self.B = B              # Probability of backward branch
        self.C = C              # Probability of jump around a “then” or “else” block
        self.processID = processID  # The process ID given upon input read (order)

        self.ref = 0            # number of references
        self.res = 0            # nuber of page residency
        self.faults = 0         # number of page faults
        self.evicts = 0         # number of page evictions

        self.word = (111*processID) % S # Beginning of referemce
        self.pageList = []
        self.start()
        
    # When printing process
    def __str__(self):
        return "Process {}".format(self.processID)

    # Most recent word returned
    def getCurrentWord(self):
        return self.word

    # Next word that will be referenced
    def getNextWord(self):
        frac = specs.rand.randomFraction()

        if frac < self.A:
            self.word = (self.word + 1) % S
        elif frac < self.A + self.B:
            self.word = (self.word - 5 + S) % S
        elif frac < self.A + self.B + self.C:
            self.word = (self.word + 4) % S
        else:
            self.word = specs.rand.stripFile() % S

        return self.word

    def getCurrentPage(self):
        pageIndex = int(math.floor(self.word / P))
        return self.pageList[pageIndex]
    
    def referenceUp(self):
        self.ref += 1

    def residencyUp(self):
        self.res += 1

    def boolTerminate(self):
        if self.ref < N:
            return False
        else:
            return True

    def start(self):
        pageLim = int(math.ceil(S/P))
        for i in range(pageLim):
            self.pageList.append(Page(self, i, self.processID))

# ProcessSummary class iterates through the processes for complete summary - Modified from Lab 2

class ProcessSummary(list):
    def __init__(self):
        super(ProcessSummary, self).__init__()
    
    def start(self, J):
        # One Process, Sequential
        if J == 1:
            self.append(Process(1,0,0,1))
        
        # Four Processes, Sequential
        elif J == 2:
            self.append(Process(1,0,0,1))
            self.append(Process(1,0,0,2))
            self.append(Process(1,0,0,3))
            self.append(Process(1,0,0,4))

        # Four Processes, Random
        elif J == 3:
            self.append(Process(0,0,0,1))
            self.append(Process(0,0,0,2))
            self.append(Process(0,0,0,3))
            self.append(Process(0,0,0,4))
        
        # Four Processes, multiple combinations
        elif J == 4:
            self.append(Process(0.75, 0.25, 0, 1))
            self.append(Process(0.75, 0, 0.25, 2))
            self.append(Process(0.75, 0.125, 0.125, 3))
            self.append(Process(0.5, 0.125, 0.125, 4))

        return self

    def printSum(self):
        res = 0
        faults = 0
        evicts = 0

        for process in self:
            res += process.res
            faults += process.faults
            evicts += process.evicts

            # print("@@@@@", process.evicts)

            if process.evicts == 0:
                print("Process {} had {} faults.\n     With no evictions, the average residence is undefined.". format(process.processID, process.faults))
            else:
                print("Process {} had {} faults and {} average residency.\n".format(process.processID, process.faults, process.res/process.evicts))
        
        if evicts == 0:
            print("The total number of faults is {}.\n      With no evictions, the overall average residence is undefined.".format(faults))
        else:
            print("The total number of faults is {} and the overall average residency is {}.".format(faults, res/evicts))
    
    def boolTerminate(self):
        # checked
        for process in self:
            if process.boolTerminate() == False:
                return False
        return True

# Class that models individual pages 

class Page():
    def __init__(self, process, num, pageID):
        self.owner = process
        self.num = num
        self.pageID = pageID
        self.res = 0

    def refer(self):
        self.owner.referenceUp()
    
    def residencyUp(self):
        self.res += 1
    


# Class that models individual frames in memory
class Frame():
    def __init__(self, frameID):
        self.frameID = frameID 
        self.firstRef = 2147469842
        self.finalRef = -1
    
        self.page = None

    def __str__(self):
        if self.page is None:
            return "Frame {} is Empty".format(self.frameID)
        else:
            return "Frame {}: Page {} of Process {}".format(self.frameID, self.page.num, self.page.pageID)

    def refer(self):
        if self.page is None:
            raise Exception("Referred frame is empty")
        
        # Retrieving current time when referred
        time = specs.time.getTimeCount()
        if time < self.firstRef:
            self.firstRef = time
        if time > self.finalRef:
            self.finalRef = time

        self.page.refer()

    # def link(self, page):
    #     self.page = page

    def restart(self):
        self.__init__(self.frameID)

# List class that contains and manages all of the frames
class FrameTable(list):
    def __init__(self):
        super(FrameTable, self).__init__()

    def start(self, numFrames):
        for f in range(numFrames):
            self.append(Frame(f))
        return self
    
    def getFrameID(self, page):
        for f in self:
            
            if f.page is not None and (f.page.pageID, f.page.num) == (page.pageID, page.num):
                return f
        return None

    def updateRes(self):
        for f in self:
            if f.page is not None:
                f.page.residencyUp()

    def evictLIFO(self):
        frameT = sorted(self, key = lambda frame: frame.firstRef)[-1]
        page = frameT.page
        process = page.owner
        process.res += page.res
        page.res = 0
        process.evicts += 1
        frameT.restart()
        return frameT
        
    def evictRand(self):
        totalFrame = int(math.ceil(M/P))
        random = specs.rand.stripFile()
        frameIndex = random % totalFrame
        frameT = sorted(self, key = lambda frame: frame.frameID)[frameIndex]
        page = frameT.page
        process = page.owner
        process.res += page.res
        page.res = 0
        process.evicts += 1
        frameT.restart()
        return frameT

    def evictLRU(self):
        frameT = sorted(self, key = lambda frame: frame.finalRef)[0]
        page = frameT.page
        process = page.owner
        process.res += page.res
        page.res = 0
        process.evicts += 1
        frameT.restart()
        return frameT

    def manage(self, page):
        # Maintaining Consistency - decreasing order
        self.sort(key=lambda f: -f.frameID)

        for f in self:
            if f.page is None:
                f.page = page
                return f

        # Evict if full
        if R == "lifo":
            f = self.evictLIFO()
            # f.page = page
        elif R == "random":
            f = self.evictRand()
            # f.page = page
        elif R == "lru":
            f = self.evictLRU()
            # f.page = page
        else:
            raise Exception("Replacement Algo {} does not exist or is not written properly.".format(R))
        
        f.page = page
        return f

def finalPrint(M,P,S,J,N,R,_):
    print("The machine size is {}.".format(M))
    print("The page size is {}.".format(P))
    print("The process size is {}.".format(S))
    print("The job mix number is {}.".format(J))
    print("The number of references per process is {}.".format(N))
    print("The replacement algorithm is {}.".format(R))
    print("The level of debugging output is {}".format(_))
    print()


def main():
    
    numFrames = int(math.ceil(M/P))
    frameTable = FrameTable().start(numFrames)
    processSummary = ProcessSummary().start(J)

    # Run while the processes are not termianted
    while processSummary.boolTerminate() == False:
        
        for process in processSummary:
            q = 3   # provided
            for i in range(q):
                if process.boolTerminate():
                    break
                # References Page
                currentPage = process.getCurrentPage()
                currentFrame = frameTable.getFrameID(currentPage)
                specs.time.updateTimeCount()

                # Checking for page fault
                if currentFrame is None:
                    process.faults += 1     # increment number of page faults
                    currentFrame = frameTable.manage(currentPage)
                
                # Referencing Page
                currentFrame.refer()
                frameTable.updateRes()
                process.getNextWord()
    processSummary.printSum()

if __name__ == "__main__":
    args = sys.argv[1:]
    for i in range(len(args)):
        if args[i].isnumeric():
            args[i] = int(args[i])
    
    M,P,S,J,N,R,_ = args

    specs.time.currentTimeCount = 0
    specs.rand.restart()
    finalPrint(M,P,S,J,N,R,_)
    main()

