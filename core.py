import math
import sys
#TODO
#add takeover of execution when a higher priority algorithm starts



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
    def __init__(self, simTime, process,duration):
        self.simTime = simTime
        self.process = process
        self.duration = duration
    
    def printSelf(self):
        print(str(self.simTime) + "---"+str(self.simTime+self.duration)+": P" + str(self.process.pid))

    def printSelfPart(self):
        print(str(self.simTime) +": P" + str(self.process.pid))

    def toString(self):
        return  "P" + str(self.process.pid) +"\t\t\t"+ str(int(self.simTime)) + "\t\t\t"+ str(int(self.simTime+self.duration))
    
    def toPartString(self):
        return "P" + str(self.process.pid) + "\t\t\t"+str(int(self.simTime))

class ScheduleResult:
    def __init__(self, timeLine, missesLine):
        self.timeLine = timeLine
        self.missesLine = missesLine

    def toString(self):
        result = "------Timeline------ \n"
        result += "Process \tStart \t\tEnd \n"
        for i in range(len(self.timeLine)):
            result += self.timeLine[i].toString() +  "\n"

        result += "\n------Missed Deathlines------ \n"
        result += "Process \tTime \n"
        for i in range(len(self.missesLine)):
            result += self.missesLine[i].toPartString() +  "\n"
        
        return result

class Process:
    def __init__(self,period, duration,pid):
        self.period = period
        self.duration = duration
        #this variable stores last period this node executed
        self.lastPeriod = 0 
        self.pid = pid
    
    def printSelf(self):
        print("P" +str(self.pid)+"    " + "period:" +str(self.period)+"   -   duration:"+ str(self.duration))
    
    #returns next simTime in wich this should execute
    def getNextPeriodStartTime(self):
        return self.period*self.lastPeriod
    def getNextPeriodEndTime(self):
        return self.period*(self.lastPeriod+1)
    def getNextTime(self, simTime):
        return int(math.ceil(float(simTime)/self.period))*self.period
    
    #executes current process, returns missed periods
    def execute(self, simTime):
        missed = []
        newPeriod = math.floor(simTime/self.period + 1)
        self.lastPeriod += 1
        while(self.lastPeriod < newPeriod):
            missed += [TimeStamp(self.lastPeriod*self.period,self,self.duration)]
            self.lastPeriod += 1
        self.lastPeriod = newPeriod
        return missed

    

    def reset(self):
        self.lastPeriod = 0 
    



class FileDecoder:
    
    #recibes a list of lines
    #returns an array of process objects
    def decodeFile(self,pfile):
        processes = []
        lines = pfile.readlines()	
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
    # a simulation simTime
    # returns a Timeline result
    def schedule(self, processes):
        #reset procces current period to restart n
        for process in processes:
            process.reset()
        
        simTime = 0
        lostDeathLines = []
        timeline = []
        #print(processes)
        while(simTime < self.simTime):
            nextProcess = self.getNext(processes,simTime)
            #print("time "+ str(simTime))
            if(nextProcess is not None):
                #print("found process")
                #nextProcess.printSelf()
                missed = nextProcess.execute(simTime)
                lostDeathLines += missed
                #add execution to timeline
                timeline += [TimeStamp(simTime,nextProcess,nextProcess.duration)]
                simTime += nextProcess.duration
            else:
                simTime = self.getNextTime(simTime, processes)

        
        #get all ines that were remaining
        for i in range(len(processes)):
            lostDeathLines += processes[i].execute(self.simTime)

        #printTList(timeline)
        #print("missed")
        #printMList(lostDeathLines)
        
        return ScheduleResult(timeline,lostDeathLines)

    def getNext(self,processes,simTime):
        nextProcess = None
        for index in range(len(processes)):
            process = processes[index]
            #if process has not executed
            if(process.getNextPeriodStartTime() <= simTime and process.duration + simTime < process.getNextPeriodEndTime()):
                #if process is the firt process to be iterated store as best solution
                if(nextProcess is None):
                    nextProcess = process
                #if process is executed before stored best process select the current proces
                elif(nextProcess.getNextPeriodEndTime() > process.getNextPeriodEndTime()):
                    nextProcess = process
        return nextProcess
    
    #gets the closest start simTime of a process 
    def getNextTime(self,simTime,processes):
        nextTime = sys.maxsize
        for index in range(len(processes)):
            process = processes[index]
            nextTime = min(nextTime, process.getNextTime(simTime))
        return nextTime
            
class RateMonotonicScheduler:
    def __init__(self, simulationTime):
        self.simTime = simulationTime 
    #recibes :
    # a list of proceses
    # a simulation simTime
    # returns a Timeline result
    def schedule(self, processes):
        #reset procces current period to restart simulation
        for process in processes:
            process.reset()
        simTime = 0
        lostDeathLines = []
        timeline = []
        while(simTime < self.simTime):
            nextProcess = self.getNext(processes,simTime)
            if(nextProcess is not None):
               
                #nextProcess.printSelf()
                missed = nextProcess.execute(simTime)
                lostDeathLines += missed
                #add execution to timeline
                timeline += [TimeStamp(simTime,nextProcess,nextProcess.duration)]
                simTime += nextProcess.duration
            else:
                simTime = self.getNextTime(simTime, processes)

        #get all ines that were remaining
        for i in range(len(processes)):
            lostDeathLines += processes[i].execute(self.simTime)

        printTList(timeline)
        print("missed")
        printMList(lostDeathLines)
        
        return ScheduleResult(timeline,lostDeathLines)

    def getNext(self,processes,simTime):
        nextProcess = None
        for index in range(len(processes)):
            process = processes[index]
            #if process has not executed
            if(process.getNextPeriodStartTime() <= simTime and procces.duration + simTime < process.getNextPeriodEndTime()):
                #if process is the firt process to be iterated store as best solution
                if(nextProcess is None):
                    nextProcess = process
                #choose next execution acording to shortest duration
                elif(nextProcess.duration > process.duration):
                    nextProcess = process
        
        return nextProcess
    
    #gets the closest start simTime of a process 
    def getNextTime(self,simTime,processes):
        nextTime = sys.maxsize
        for index in range(len(processes)):
            process = processes[index]
            nextTime = min(nextTime, process.getNextTime(simTime))
        return nextTime

'''
pFile = open("test","r")
decoder = FileDecoder()
decoded = decoder.decodeFile(pFile)
scheduler = RateMonotonicScheduler(300)
scheduler.schedule(decoded)
pFile.close() 
'''
