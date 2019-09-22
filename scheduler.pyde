import visualScheduler as vs
import core

#TODO
#add usage of timeline duration in gui
inputFilePath = None
outputFilePath = None
schedule = None
processes = None
drawer = None
drawScale = 4.0
time = -50
simulationTime = 300
previousX = 0
dragSpeed = 0.3
edf = True

BUTTONS = []


#processing function to setup graphical interface
def setup():
    global BUTTONS
    global saveTimeline
    global loadProcess
    global increaseDuration
    global decreaseDuration
    global switchAlgorithm
    size(720, 480)
    
    
    
    #create buttons
    BUTTONS += [vs.Button(20,20,100,30, "Load",loadProcess)]
    BUTTONS += [vs.Button(140,20,100,30, "Save",saveTimeline)]
    BUTTONS += [vs.Button(width -100,20,30,30, "  +",increaseDuration)]
    BUTTONS += [vs.Button(width -50,20,30,30, "  -",decreaseDuration)]
    BUTTONS += [vs.Button(width -400,20,100,30, "Algorithm",switchAlgorithm)]
    
    #frameRate(1)

#procesing function to draw on canvas usually executed 30 times per second
def draw():
    global drawer
    global drawScale
    global time
    global simulationTime
    global BUTTONS
    global edf
    background(255)
    #draw simulation time text
    fill(0)
    stroke(0)
    
    current = ""
    if(edf):
        current = "Earliest Deathline First"
    else:
        current = "Rate Monotonic"
    text(current,width -400,65)
    
    text("Duration: " + str(simulationTime)+"ms",width -230,40)
    #buttons should be drawn before translating
    for button in BUTTONS:
        button.drawSelf()
    
    translate(time*drawScale  + width/2 ,0)
    
    #print(schedule)
    if(drawer is not None):
        fill(0)
        stroke(180)
        drawer.drawTimeLine(0,height/2,drawScale)
        drawer.drawMisses(0,height/2 + 40 ,drawScale)
        drawer.drawScaleLines(0,height/2 ,drawScale,simulationTime)
    
    

def mouseWheel(event): 
    global drawScale
    e = event.getCount()
    drawScale += event.getCount()/10.0
    drawScale = max(drawScale,1)
    #print(drawScale)
    # keep value in range
def mouseDragged(event): 
    global previousX 
    global dragSpeed 
    global time
    global simulationTime
    if(previousX < mouseX):
        time += dragSpeed
    elif(previousX > mouseX):
        time -= dragSpeed
    
    #set bounds of time
    #time = min(-20,time)
    #time = max((-simulationTime+50)*drawScale,time)
    #print(time)
    previousX = mouseX

def mousePressed():
    global BUTTONS
    #update all buttons with click event
    for button in BUTTONS:
        button.click()

def inputSelected(file):
    global inputFilePath
    global processes
    global updateTimeline
    global schedule
    global drawer
    global simulationTime
    global getScheduler

    inputFilePath = file.getAbsolutePath()
    iFile = open(inputFilePath,"r")

    decoder = core.FileDecoder()
    processes = decoder.decodeFile(iFile)
    
    try:
        totalProcess = len(processes)
        scheduler = getScheduler()
        schedule = scheduler.schedule(processes)
        #print("creating drawed")
      
        drawer = vs.TimelineDrawer(schedule,totalProcess)
        if(drawer is not None):
            drawer.setSchedule(schedule)
        #print("drawed created")
    except:
        print("failed to update timeline")
    
    
def getScheduler():
    global simulationTime
    global edf
    if(edf):
        return core.EdfScheduler(simulationTime)
    else:
        return core.RateMonotonicScheduler2(simulationTime)
           
def updateTimeline():
    global processes
    global schedule
    global drawer
    global simulationTime
    global getScheduler
    try:
        totalProcess = len(processes)
        scheduler = getScheduler()
            
        schedule = scheduler.schedule(processes)
        #print("creating drawed")
        if(drawer is not None):
            drawer.setSchedule(schedule)
        #print("drawed created")
    except:
        print("failed to update timeline")
        
    #print(file)

def outputSelected(file):
    global schedule
    global outputFilePath
    outputFilePath = file.getAbsolutePath();
    try:
        #print()
        oFile = open(outputFilePath,"w+")
        oFile.write(schedule.toString())
        oFile.close()
    except:
        print("failed to create output file")
        
#Button functions
def loadProcess():
    selectInput("Select a file to process:", "inputSelected")

def saveTimeline():
    global schedule
    if(schedule is None):
        return
    selectOutput("Select a file to process:", "outputSelected")

def switchAlgorithm():
    global edf
    global updateTimeline
    edf = not edf

    #reflect changes on interfaz
    updateTimeline()

def increaseDuration():
    global simulationTime
    global updateTimeline
    
    simulationTime += 50
    
    #reflect changes on interfaz
    updateTimeline()

def decreaseDuration():
    global simulationTime
    global updateTimeline
    
    simulationTime = max(50,simulationTime - 50)
    
    #reflect changes on interfaz
    updateTimeline()
