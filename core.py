import math
import sys


#utility fuinctions
#print a list of TimeStamps
def printTList(tlist):
    for i in range(len(tlist)):
        timeStamp = tlist[i]
        timeStamp.printSelf() 

def printMList(tlist):
    for i in range(len(tlist)):
        timeStamp = tlist[i]
        timeStamp.printSelfPart() 

class TimeStamp:
    def __init__(self, time, process):
        self.time = time
        self.process = process
    
    def printSelf(self):
        print(str(self.time) + "---"+str(self.time+self.process.duration)+": P" + str(self.process.pid))

    def printSelfPart(self):
        print(str(self.time) +": P" + str(self.process.pid))

class ScheduleResult:
    def __init__(self, timeLine, missesLine):
        self.timeLine = timeLine
        self.missesLine = missesLine

class Process:
    def __init__(self,period, duration,pid):
        self.period = period
        self.duration = duration
        #this variable stores last period this node executed
        self.lastPeriod = 0 
        self.pid = pid
    
    def printSelf(self):
        print("P" +str(self.pid)+"    " + "period:" +str(self.period)+"   -   duration:"+ str(self.duration))

    #returns next time in wich this should execute
    def getNextPeriodStartTime(self):
        return self.period*self.lastPeriod
    def getNextPeriodEndTime(self):
        return self.period*(self.lastPeriod+1)
    
    #executes current process, returns missed periods
    def execute(self, time):
        missed = []
        newPeriod = math.floor(time/self.period + 1)
        self.lastPeriod += 1
        while(self.lastPeriod < newPeriod):
            missed += [TimeStamp(self.lastPeriod*self.period,self)]
            self.lastPeriod += 1
        self.lastPeriod = newPeriod
        return missed




class FileDecoder:
    
    #recibes a list of lines
    #returns an array of process objects
    def decodeFile(self,pfile):
        processes = []
        lines = pFile.readlines()	
        for i in range(len(lines)):
            pieces = lines[i].split(' ')
            period = int(pieces[0])
            duration = int(pieces[1])
            process = Process(period,duration,int(i))
            processes += [process]
            #process.printSelf()
        #print(proceses)
        return processes



class EdfScheduler:
    def __init__(self, simulationTime):
        self.simTime = simulationTime 
    #recibes :
    # a list of proceses
    # a simulation time
    # returns a Timeline result
    def schedule(self, processes):
        time = 0
        lostDeathLines = []
        timeline = []
        while(time < self.simTime):
            nextProcess = self.getNext(processes,time)
            if(nextProcess is not None):
                #nextProcess.printSelf()
                missed = nextProcess.execute(time)
                lostDeathLines += missed
                #add execution to timeline
                timeline += [TimeStamp(time,nextProcess)]
                time += nextProcess.duration
            else:
                time += self.getNextTime(time, processes)

        #get all ines that were remaining
        for i in range(len(processes)):
            lostDeathLines += processes[i].execute(time)

        printTList(timeline)
        print("missed")
        printMList(lostDeathLines)
        
        return ScheduleResult(timeline,lostDeathLines)

    def getNext(self,processes,time):
        nextProcess = None
        for index in range(len(processes)):
            process = processes[index]
            #if process has not executed
            if(process.getNextPeriodStartTime() <= time ):
                #if process is the firt process to be iterated store as best solution
                if(nextProcess is None):
                    nextProcess = process
                #if process is executed before stored best process select the current proces
                elif(nextProcess.getNextPeriodEndTime() > process.getNextPeriodEndTime()):
                    nextProcess = process
        
        return nextProcess
    
    #gets the closest start time of a process 
    def getNextTime(self,time,processes):
        nextTime = sys.maxsize
        for index in range(len(processes)):
            process = processes[index]
            nextTime = min(nextTime, process.getNextPeriodStartTime())
        return nextTime
            
class RateMonotonicScheduler:
    def __init__(self, simulationTime):
        self.simTime = simulationTime 
    #recibes :
    # a list of proceses
    # a simulation time
    # returns a Timeline result
    def schedule(self, processes):
        time = 0
        lostDeathLines = []
        timeline = []
        while(time < self.simTime):
            nextProcess = self.getNext(processes,time)
            if(nextProcess is not None):
                #nextProcess.printSelf()
                missed = nextProcess.execute(time)
                lostDeathLines += missed
                #add execution to timeline
                timeline += [TimeStamp(time,nextProcess)]
                time += nextProcess.duration
            else:
                time += self.getNextTime(time, processes)

        #get all ines that were remaining
        for i in range(len(processes)):
            lostDeathLines += processes[i].execute(time)

        printTList(timeline)
        print("missed")
        printMList(lostDeathLines)
        
        return ScheduleResult(timeline,lostDeathLines)

    def getNext(self,processes,time):
        nextProcess = None
        for index in range(len(processes)):
            process = processes[index]
            #if process has not executed
            if(process.getNextPeriodStartTime() <= time ):
                #if process is the firt process to be iterated store as best solution
                if(nextProcess is None):
                    nextProcess = process
                #choose next execution acording to shortest duration
                elif(nextProcess.duration > process.duration):
                    nextProcess = process
        
        return nextProcess
    
    #gets the closest start time of a process 
    def getNextTime(self,time,processes):
        nextTime = sys.maxsize
        for index in range(len(processes)):
            process = processes[index]
            nextTime = min(nextTime, process.getNextPeriodStartTime())
        return nextTime


pFile = open("test","r")
decoder = FileDecoder()
decoded = decoder.decodeFile(pFile)	
scheduler = RateMonotonicScheduler(300)
scheduler.schedule(decoded)
pFile.close() 