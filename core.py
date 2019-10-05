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

    def toString(self,duration):
        result = "------Timeline------ \n"
        result += "Process \tStart \t\tEnd \n"
        for i in range(len(self.timeLine)):
            result += self.timeLine[i].toString() +  "\n"

        result += "\n------Missed Deathlines------ \n"
        result += "Process \tTime \n"
        for i in range(len(self.missesLine)):
            result += self.missesLine[i].toPartString() +  "\n"
        
        result += self.generateReport(duration)
        result += self.generateMissesReport(duration)

        return result
    
    def generateReport(self, duration):
        res = {}
        proc = {}
        for stamp in self.timeLine:
            key = stamp.process.pid
            if(not key in res.keys()):
                res[key] = 0
                proc[key] = stamp.process
            res[key] += 1

        formated = "\nExecuted---------------- \n"
        for key in res:
            formated +=  "P"+ str(key) + ": " + str(res[key]) + "---"+ str(res[key]/(duration/ proc[key].period)*100)+"%\n"
        
        
        return formated
    
    def generateMissesReport(self, duration):
        res = {}
        for stamp in self.missesLine:
            key = stamp.process.pid
            if(not key in res.keys()):
                res[key] = 0
            res[key] += 1

        formated = "\nMissed---------------- \n"
        for key in res:
            formated +=  "P"+ str(key) + ": " + str(res[key]) + "\n"
        
        return formated
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
	
    def getCurrentTime(self, simTime):
        newPeriod = math.floor(float(simTime)/self.period)
        return newPeriod * self.period
	
    def getNextTime(self, simTime):
        newPeriod = math.floor(float(simTime)/self.period + 1) #time of next deathline
        return newPeriod * self.period
    
    def getTakeoverTime(self,simTime):
        newPeriod = math.ceil(simTime/self.period + 1) #time of next deathline
        return newPeriod * self.period
		
    def isExecuted(self, simTime):
        print("last period: " + str(self.lastPeriod) + "-----time: " + str(math.floor(simTime/self.period)) + "----sim time: " +  str(simTime) + "--- period: " + str(self.period))
        return self.lastPeriod >= math.floor(simTime/self.period)

    #executes current process, returns missed periods
    def execute(self, simTime):
        missed = []
        newPeriod = math.floor(simTime/self.period + 1)
        self.lastPeriod += 1
        while(self.lastPeriod < newPeriod):
            missed += [TimeStamp(self.lastPeriod*self.period,self,self.duration)]
            self.lastPeriod += 1
        self.lastPeriod = newPeriod

        #if current period misses add it too
        if(newPeriod*self.period < simTime + self.duration):
            #print(str(simTime) + " got extra miss " +str(newPeriod*self.period) + "----" + str(simTime + self.duration) )
            missed += [TimeStamp(self.lastPeriod*self.period,self,self.duration)]

        return missed

    def executePartial(self,simTime,remaining):
        missed = []
        newPeriod = math.floor(simTime/self.period + 1)
        self.lastPeriod += 1
        while(self.lastPeriod < newPeriod):
            missed += [TimeStamp(self.lastPeriod*self.period,self,self.duration)]
            self.lastPeriod += 1
        self.lastPeriod = newPeriod

        #if current period misses add it too
        if(newPeriod*self.period < simTime + remaining):
            #print(str(simTime) + " got extra miss " +str(newPeriod*self.period) + "----" + str(simTime + self.duration) )
            missed += [TimeStamp(self.lastPeriod*self.period,self,self.duration)]

        return missed
	
    def miss(self, simTime,start):
        return [TimeStamp(start,self,self.duration)]
	
    #executes current process but does not modify stat
    def validateExecution(self, simTime,time):
        newPeriod = math.floor(simTime/self.period + 1)
        nextStart = (self.lastPeriod + 1)*duration 

        #checks if executions happens before deathline
        if(simTime + time <= nextStart): 
            return True
        return False

    def reset(self):
        self.lastPeriod = 0 
    

class Execution:
    def __init__(self,process):
        self.executed = 0
        self.process = process
        if(process is not None):
            self.total = process.duration
        else:
            self.total = 0
        

    #return a TimeStamp with procces execution
    def executeTime(self,simTime,time):
        self.executed += time
        #print(simTime)
        #print(time)
        return TimeStamp(simTime,self.process,time)

    def isFinished(self):
        return self.executed >= self.total

    def remaining(self):
        return max(0,self.total-self.executed)
    
    def canExecute(self,simTime):
        if(self.process is None ):
            return False
        return ( simTime - self.executed + self.total ) < self.process.getNextTime(simTime) 

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

        #store procces in a queue while 
        pending = []
        #print(processes)
        while(simTime < self.simTime):
            pending += [ Execution (self.getNext(processes,simTime))]
            while(len(pending) > 0):

                #finish simulation if needed
                if(simTime >= self.simTime):
                    break
                
                #takes out last element inside of list
                nextExecution = pending.pop(-1)
                
                

                if(nextExecution.process is not None):
                   
                    nextProcess = nextExecution.process
                    #print("found procces" +  " P" + str(nextProcess.pid))
                    

                    
                    
                    #add takeover simulation
                    takeover = self.getTakeOverProcess(processes,nextProcess,simTime,nextExecution)
                    if(takeover is not None):
                        #print("takeover by P" + str(takeover.pid) + " to P" + str(nextProcess.pid) + " on " + str(simTime))
                        if(not nextExecution.isFinished()):
                            #print("time stamp")
                            #executes in next period or in current period
                            execution = 0
                            #if procces has not started keep executing current process
                            if(takeover.getNextPeriodStartTime() >= simTime):
                                if(nextExecution.canExecute(simTime)):
                                    execution = min(takeover.getNextPeriodStartTime() - simTime,nextExecution.remaining())
                                    timeline += [nextExecution.executeTime(simTime,execution)]
                                else:
                                    #if procces cannot execute start on next execution
                                    simTime = takeover.getNextPeriodStartTime()
                            #print("add current execution back to queue")
                            #print("st:  " + str(simTime))
                            #print("exec: " + str(execution))
							#check again if in this iteration execution finished
                            if(not nextExecution.isFinished() and nextExecution.canExecute(simTime)):
                                pending += [nextExecution]

                            simTime += execution
                        #print("add takeover on top of queue")
                        pending += [Execution(takeover)]

                        #simulate after takeover calculation to preserve current procces deathline
                        missed = nextProcess.executePartial(simTime, nextExecution.remaining())
                        lostDeathLines += missed
                    else:
                        #print("not takeover "+ str(simTime))
                        #print("start " + str(nextProcess.getNextPeriodStartTime()) + "---end: " + str(nextProcess.getNextPeriodEndTime()))
                        #add execution to timeline
                        #verify if process can execute before deahtline
                        if(simTime + nextExecution.remaining() < nextProcess.getNextTime(simTime)):
                            timeline += [TimeStamp(simTime,nextProcess,nextExecution.remaining())]
                            #simulate after takeover calculation to preserve current procces deathline
                            missed = nextProcess.executePartial(simTime,nextExecution.remaining())
                            lostDeathLines += missed
                            #modify sim time after simulated execution
                            simTime += nextExecution.remaining()
                        else:
                            #simulate after takeover calculation to preserve current procces deathline
                            missed = nextProcess.execute(simTime)
                            lostDeathLines += missed
                            

                    

                else:
                    #print("np")
                    simTime = self.getNextTime(processes, simTime)
                    #print("no process "+ str(simTime))

                
            #nextProcess = self.getNext(processes,simTime)
        #print("pending " + str(len(pending)))
        #get all ines that were remaining
        for i in range(len(processes)):
            lostDeathLines += processes[i].execute(self.simTime)

        #printTList(timeline)
        #print("missed")
        #printMList(lostDeathLines)
        
        return ScheduleResult(timeline,lostDeathLines)

    #must have executed current procces
    def getNext(self,processes,simTime):
        nextProcess = None
        #print("n")
        #print("---" + str(len(processes)) + "---")
        for index in range(len(processes)):
            #print(str(index))
            process = processes[index]
            #if process has not executed
            #print("-----------------")
            #print(simTime)
            #print(process.getNextPeriodStartTime())
            #print(process.getNextPeriodEndTime())
            #print(process.getTakeoverTime(simTime))
            #print("<--------------->")
            if(process.getNextPeriodStartTime() <= simTime and process.duration + simTime < process.getNextTime(simTime)):
                #print("gn")
                #print("nt P" +str(process.pid) +"---"+str(process.getNextPeriodEndTime()))
                #if process is the firt process to be iterated store as best solution
                #nextProcess.printSelf();
                #process.printSelf()
                
                if(nextProcess is None):
                    #print("None")
                    nextProcess = process
                #if process is executed before stored best process select the current proces
                elif(nextProcess.getNextTime(simTime) > process.getNextTime(simTime)):
                    #print("found one")
                    nextProcess = process

        #print(nextProcess is None)
        return nextProcess


    def getTakeOverProcess(self,processes,currentProcces,simTime,currentExecution):
        takeover = None
        bestTime = sys.maxsize
        for index in range(len(processes)):
            process = processes[index]
            #print("getting takeover")
            takeoverTime = process.getNextPeriodEndTime()
            #if this procces had calculete nexttime
            if(takeoverTime <= simTime):
                takeoverTime =  process.getTakeoverTime(simTime)
				
            if(takeoverTime < process.getNextPeriodEndTime()):
                takeoverTime = process.getNextPeriodEndTime()

            #print( str(simTime) + " P" + str(process.pid)+"// -tk-" +str(takeoverTime) +  "- P" + str(currentProcces.pid)+"-cu-" + str(currentProcces.getNextPeriodEndTime()))
            if(takeoverTime < currentProcces.getNextPeriodEndTime() and takeoverTime < bestTime and simTime + currentExecution.remaining() > process.getNextPeriodStartTime()):
                #print("bt " + str(bestTime) + "-----tk " + str(takeoverTime) )
                bestTime = takeoverTime
                takeover = process
            
        if(takeover == currentProcces):
            return None

        return takeover
    
    #gets the closest start simTime of a process 
    def getNextTime(self,processes,simTime):
        nextTime = sys.maxsize
        for index in range(len(processes)):
            process = processes[index]
            nextTime = min(nextTime, process.getNextTime(simTime))
        return nextTime


class RateMonotonicScheduler2:
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

        #store procces in a queue while 
        pending = []
        #print(processes)
        while(simTime < self.simTime):
            pending += [ Execution (self.getNext(processes,simTime))]
            while(len(pending) > 0):

                #finish simulation if needed
                if(simTime >= self.simTime):
                    break
                
                #takes out last element inside of list
                nextExecution = pending.pop(-1)
                
                

                if(nextExecution.process is not None):
                   
                    nextProcess = nextExecution.process
                    #print("found procces" +  " P" + str(nextProcess.pid))
                    

                    
                    
                    #add takeover simulation
                    takeover = self.getTakeOverProcess(processes,nextExecution,simTime)
                    if(takeover is not None):
                        #print(str(simTime) + "  takeover by P" + str(takeover.pid) + " to P" + str(nextProcess.pid))
                        if(not nextExecution.isFinished()):
                            #print("time stamp")
                            #executes in next period or in current period
                            execution = 0
                            #if procces has not started keep executing current process
                            if(takeover.getNextPeriodStartTime() >= simTime):
                                if(nextExecution.canExecute(simTime)):
                                    execution = min(takeover.getNextPeriodStartTime() - simTime,nextExecution.remaining())
                                    timeline += [nextExecution.executeTime(simTime,execution)]
                                else:
                                    #if procces cannot execute start on next execution
                                    simTime = takeover.getNextPeriodStartTime()
                            #print("add current execution back to queue")
                            #check again if in this iteration execution finished
                            if(not nextExecution.isFinished() and nextExecution.canExecute(simTime)):
                                pending += [nextExecution]
                            simTime += execution
                        #print("add takeover on top of queue")
                        pending += [Execution(takeover)]

                        #simulate after takeover calculation to preserve current procces deathline
                        missed = nextProcess.executePartial(simTime, nextExecution.remaining())
                        lostDeathLines += missed
                    else:
                        #print("not takeover")
                        #add execution to timeline
                        #verify if process can execute before deahtline
                        if(simTime + nextExecution.remaining() < nextProcess.getNextTime(simTime)):
                            timeline += [TimeStamp(simTime,nextProcess,nextExecution.remaining())]
                            #simulate after takeover calculation to preserve current procces deathline
                            missed = nextProcess.executePartial(simTime,nextExecution.remaining())
                            lostDeathLines += missed
                            #modify sim time after simulated execution
                            simTime += nextExecution.remaining()
                        else:
                            #simulate after takeover calculation to preserve current procces deathline
                            missed = nextProcess.execute(simTime)
                            lostDeathLines += missed
                            

                    

                else:
                    #print("np")
                    simTime = self.getNextTime(processes, simTime)
                    #print("no process "+ str(simTime))

                
            #nextProcess = self.getNext(processes,simTime)
			
        
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
            if(process.getNextPeriodStartTime() <= simTime and process.duration + simTime < process.getNextTime(simTime)):
                #if process is the firt process to be iterated store as best solution
                if(nextProcess is None):
                    nextProcess = process
                #choose next execution acording to shortest duration
                elif(nextProcess.duration > process.duration):
                    #print("P"+str(procces.pid))
                    nextProcess = process
        
        return nextProcess
    

    def getTakeOverProcess(self,processes,currentExecution,simTime):
        takeover = None
        bestTime = sys.maxsize
        currentProcces = currentExecution.process
        for index in range(len(processes)):
            process = processes[index]
            #print("getting takeover")
            takeoverTime = process.getNextPeriodStartTime()
            #if this procces had calculete nexttime
            if(takeoverTime <= simTime):
                takeoverTime =  process.getNextTime(simTime)

            #print( str(simTime) + " P" + str(process.pid)+"// -tk-" +str(takeoverTime) +  "- P" + str(currentProcces.pid)+"-cu-" + str(currentProcces.getNextPeriodEndTime()))
            if(takeoverTime < simTime + currentExecution.remaining() and takeoverTime <= bestTime and process.duration < currentProcces.duration):
                #print("bt " + str(bestTime) + "-----tk " + str(takeoverTime) + "-----" +  str(currentProcces.getNextPeriodEndTime()) )
                bestTime = takeoverTime
                takeover = process
            
        if(takeover == currentProcces):
            return None

        return takeover
    
    #gets the closest start simTime of a process 
    def getNextTime(self,processes,simTime):
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
