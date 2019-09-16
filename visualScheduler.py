

class TimelineDrawer:
    def __init__(self, schedule,colors):
        self.schedule =  schedule
        self.colors =[]
        for i in range(colors):
            self.colors += [color(random(125), random(125), random(125))]
        
    
    def drawTimeLine(self,x,y,sc):
        timeline = self.schedule.timeLine
        for i in range(len(timeline)):
            moment = timeline[i]
            fill(self.colors[moment.process.pid])
            #print(self.colors[moment.process.pid])
            text("P" + str(moment.process.pid),x + moment.simTime*sc,y-15)
            rect(x + moment.simTime*sc,y-10,moment.process.duration*sc,20)
            text(str(moment.simTime)+"ms",x + moment.simTime*sc,y+20)    
    
    def drawMisses(self,x,y,sc):
        fill(240,40,40)
        stroke(240,40,40)
        misses = self.schedule.missesLine
        for i in range(len(misses)):
            moment = misses[i]
            line(x + moment.simTime*sc,y-50,x + moment.simTime*sc,y)
            #fill(self.colors[moment.process.pid])
            text("P" + str(moment.process.pid),x + moment.simTime*sc,y)

    def drawScaleLines(self,x,y,sc,duration):
        stroke(150)
        fill(0)
        lHeight = 200
        for i in range((duration)/100 + 1):
            text(str(i*100)+"ms",x+i*100*sc,y-lHeight/2)
            line(x+i*100*sc,y-lHeight/2,x+i*100*sc,y+lHeight/2)
            
    def setSchedule(self, schedule):
        self.schedule = schedule
    

class Button:
    def __init__(self,x,y,pWidth,pHeight,buttonText,callback):
        self.x = x
        self.y = y
        self.w = pWidth
        self.h = pHeight
        self.buttonText = buttonText
        self.callback = callback
    
    def drawSelf(self):
        if(self.mouseOver()):
            fill(220)
        else:
            fill(180)
            
        stroke(0)
        rect(self.x,self.y,self.w,self.h)
        fill(0)
        text(self.buttonText,self.x +5,self.y +self.h/2 +5)
    
    def mouseOver(self):
        return (self.x <= mouseX and self.x + self.w >= mouseX and self.y <= mouseY and self.y + self.h >= mouseY)
        
    def click(self):
        if(self.mouseOver()):
            self.callback();
